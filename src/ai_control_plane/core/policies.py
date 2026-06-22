"""PolicyEngine — sole policy evaluation layer. No OSS, no I/O."""

from __future__ import annotations

from typing import Any

from .models import (
    AgentIdentity,
    ApprovalDecision,
    ApprovalRequest,
    PolicyDecision,
    PolicyRule,
    Task,
)

# Default RBAC tool sets used when no explicit rbac PolicyRule is supplied.
_DEFAULT_RBAC: dict[str, dict[str, list[str]]] = {
    "backend": {
        "allowed_actions": [
            "git_read",
            "git_commit",
            "git_push",
            "git_diff",
            "test_run",
            "build_rust",
        ],
        "denied_patterns": ["k8s_apply_*"],
    },
    "reviewer": {
        "allowed_actions": ["read_repo", "read_pr", "comment_pr"],
        "denied_patterns": [],
    },
    "infra": {
        "allowed_actions": [
            "git_read",
            "git_commit",
            "git_push",
            "k8s_apply_*",
            "k8s_diff",
            "helm_upgrade",
            "plan_generate",
        ],
        "denied_patterns": [],
    },
}

_DEFAULT_ABAC: list[PolicyRule] = [
    PolicyRule(
        name="prod-k8s-approval",
        description="production k8s apply requires approval",
        conditions={
            "rule_type": "abac",
            "environment": "prod",
            "action": "k8s_apply_prod",
            "requires_approval": True,
        },
        effect="allow",
    ),
]


def _matches_pattern(value: str, pattern: str) -> bool:
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return value == pattern


def _matches_any_pattern(value: str, patterns: list[str]) -> bool:
    return any(_matches_pattern(value, pattern) for pattern in patterns)


def _matches_any_action(value: str, actions: list[str]) -> bool:
    return value in actions or _matches_any_pattern(value, actions)


class ConditionEvaluator:
    """Evaluate ABAC condition dicts against a runtime context."""

    _SUPPORTED_KEYS = frozenset(
        {"environment", "action", "role", "path", "data_category"},
    )

    _SKIP_KEYS = frozenset(
        {
            "rule_type",
            "requires_approval",
            "allowed_actions",
            "denied_actions",
            "denied_patterns",
            "allowed_patterns",
            "check",
            "forbidden_branches",
            "test_required_prefixes",
            "plan_field",
            "actions",
            "roles",
        },
    )

    def evaluate(self, condition: dict[str, Any], context: dict[str, Any]) -> bool:
        """Return True when every supported condition key matches *context*."""
        for key, expected in condition.items():
            if key in self._SKIP_KEYS:
                continue

            if key not in self._SUPPORTED_KEYS:
                continue

            actual = context.get(key)
            if key == "path" and actual is not None and isinstance(expected, str):
                if not str(actual).startswith(expected):
                    return False
                continue

            if key == "action" and isinstance(expected, str):
                if not _matches_pattern(str(context.get("action", "")), expected):
                    return False
                continue

            if actual != expected:
                return False
        return True


class ApprovalGate:
    """In-memory human-in-the-loop approval workflow."""

    def __init__(self) -> None:
        self._pending: dict[str, ApprovalRequest] = {}

    def request(self, event_type: str, context: dict[str, Any]) -> ApprovalRequest:
        """Create and store a pending approval request."""
        approval = ApprovalRequest(event_type=event_type, context=context)
        self._pending[str(approval.id)] = approval
        return approval

    def resolve(
        self,
        approval_id: str,
        approved: bool,
        approver: str,
    ) -> ApprovalDecision:
        """Resolve a pending approval by ID."""
        pending = self._pending.pop(approval_id, None)
        if pending is None:
            msg = f"unknown approval_id '{approval_id}'"
            raise KeyError(msg)
        return ApprovalDecision(
            request_id=pending.id,
            approved=approved,
            approver=approver,
        )


class GuardrailEvaluator:
    """Guardrail checks driven by PolicyRule configuration."""

    def __init__(self, rules: list[PolicyRule]) -> None:
        self._rules = rules

    def _guardrail_rules(self) -> list[PolicyRule]:
        return [
            rule
            for rule in self._rules
            if rule.conditions.get("rule_type") == "guardrail"
        ]

    def check_plan_required(self, task: Task) -> bool:
        """Return True when a required plan is present on *task*."""
        rules = [
            rule
            for rule in self._guardrail_rules()
            if rule.conditions.get("check") == "plan_required"
        ]
        if not rules:
            return bool(task.payload.get("plan_submitted") or task.payload.get("plan"))

        for rule in rules:
            field = str(rule.conditions.get("plan_field", "plan_submitted"))
            if not task.payload.get(field):
                return False
        return True

    def check_test_required(self, changed_paths: list[str]) -> bool:
        """Return True when no test-requiring paths were changed."""
        prefixes: list[str] = []
        for rule in self._guardrail_rules():
            if rule.conditions.get("check") != "test_required":
                continue
            rule_prefixes = rule.conditions.get("test_required_prefixes", ["src/", "crates/"])
            if isinstance(rule_prefixes, list):
                prefixes.extend(str(prefix) for prefix in rule_prefixes)

        if not prefixes:
            prefixes = ["src/", "crates/", "tests/"]

        for path in changed_paths:
            if any(path.startswith(prefix) for prefix in prefixes):
                return False
        return True

    def check_branch_allowed(self, branch: str) -> bool:
        """Return True when *branch* is not on any forbidden-branch list."""
        forbidden: set[str] = set()
        for rule in self._guardrail_rules():
            if rule.conditions.get("check") != "branch_allowed":
                continue
            rule_branches = rule.conditions.get("forbidden_branches", ["main", "master"])
            if isinstance(rule_branches, list):
                forbidden.update(str(name) for name in rule_branches)

        if not forbidden:
            forbidden = {"main", "master"}

        return branch not in forbidden


class PolicyEngine:
    """Evaluate tool calls: RBAC → ABAC → guardrails. Fail-closed by default."""

    def __init__(
        self,
        rules: list[PolicyRule],
        guardrail_evaluator: GuardrailEvaluator | None = None,
    ) -> None:
        self._rules = rules
        self._condition_evaluator = ConditionEvaluator()
        self._guardrails = guardrail_evaluator or GuardrailEvaluator(rules)

    def evaluate(
        self,
        identity: AgentIdentity,
        tool_name: str,
        args: dict[str, Any],
        project_id: str,
    ) -> PolicyDecision:
        """Evaluate whether *tool_name* is permitted for *identity*."""
        if identity.project_id != project_id:
            return PolicyDecision(
                allowed=False,
                reason=(
                    f"identity project '{identity.project_id}' "
                    f"does not match requested project '{project_id}'"
                ),
                requires_approval=False,
            )

        context: dict[str, Any] = {
            "agent_id": identity.agent_id,
            "project_id": project_id,
            "role": identity.role,
            "action": tool_name,
            "tool_name": tool_name,
            "environment": args.get(
                "environment",
                identity.jwt_claims.get("environment", "dev"),
            ),
            "path": args.get("path"),
            "branch": args.get("branch"),
            "data_category": args.get("data_category"),
            **args,
        }

        rbac_decision = self._evaluate_rbac(identity.role, tool_name)
        if rbac_decision is not None:
            return rbac_decision

        abac_decision = self._evaluate_abac(tool_name, context)
        if abac_decision is not None:
            return abac_decision

        guardrail_decision = self._evaluate_guardrails(tool_name, identity, args, context)
        if guardrail_decision is not None:
            return guardrail_decision

        return PolicyDecision(
            allowed=True,
            reason="action permitted",
            requires_approval=False,
        )

    def _rbac_rules_for_role(self, role: str) -> list[PolicyRule]:
        return [
            rule
            for rule in self._rules
            if rule.conditions.get("rule_type") == "rbac"
            and rule.conditions.get("role") == role
        ]

    def _evaluate_rbac(self, role: str, tool_name: str) -> PolicyDecision | None:
        rbac_rules = self._rbac_rules_for_role(role)

        if rbac_rules:
            rule = rbac_rules[0]
            denied_actions = list(rule.conditions.get("denied_actions", []))
            denied_patterns = list(rule.conditions.get("denied_patterns", []))
            allowed_actions = list(rule.conditions.get("allowed_actions", []))
            allowed_patterns = list(rule.conditions.get("allowed_patterns", []))

            if tool_name in denied_actions or _matches_any_pattern(tool_name, denied_patterns):
                return PolicyDecision(
                    allowed=False,
                    reason=f"tool '{tool_name}' denied for role '{role}'",
                    requires_approval=False,
                    policy_id=rule.name,
                )

            if _matches_any_action(tool_name, allowed_actions + allowed_patterns):
                return None

            return PolicyDecision(
                allowed=False,
                reason=f"tool '{tool_name}' not in allowed_actions for role '{role}'",
                requires_approval=False,
                policy_id=rule.name,
            )

        defaults = _DEFAULT_RBAC.get(role)
        if defaults is None:
            return PolicyDecision(
                allowed=False,
                reason=f"no rbac policy for role '{role}'",
                requires_approval=False,
            )

        if _matches_any_pattern(tool_name, defaults.get("denied_patterns", [])):
            return PolicyDecision(
                allowed=False,
                reason=f"tool '{tool_name}' denied for role '{role}'",
                requires_approval=False,
                policy_id=f"rbac-default-{role}",
            )

        if _matches_any_action(tool_name, defaults.get("allowed_actions", [])):
            return None

        return PolicyDecision(
            allowed=False,
            reason=f"tool '{tool_name}' not in allowed_actions for role '{role}'",
            requires_approval=False,
            policy_id=f"rbac-default-{role}",
        )

    def _abac_rules(self) -> list[PolicyRule]:
        explicit = [
            rule
            for rule in self._rules
            if rule.conditions.get("rule_type", "abac") == "abac"
        ]
        names = {rule.name for rule in explicit}
        return explicit + [rule for rule in _DEFAULT_ABAC if rule.name not in names]

    def _evaluate_abac(self, tool_name: str, context: dict[str, Any]) -> PolicyDecision | None:
        context = {**context, "action": tool_name}

        for rule in self._abac_rules():
            if rule.effect != "deny":
                continue
            if not self._condition_evaluator.evaluate(rule.conditions, context):
                continue
            return PolicyDecision(
                allowed=False,
                reason=rule.description or f"denied by rule '{rule.name}'",
                requires_approval=False,
                policy_id=rule.name,
            )

        for rule in self._abac_rules():
            if rule.effect != "allow":
                continue
            if not self._condition_evaluator.evaluate(rule.conditions, context):
                continue
            requires_approval = bool(rule.conditions.get("requires_approval", False))
            return PolicyDecision(
                allowed=True,
                reason=rule.description or f"allowed by rule '{rule.name}'",
                requires_approval=requires_approval,
                policy_id=rule.name,
            )

        return None

    def _evaluate_guardrails(
        self,
        tool_name: str,
        identity: AgentIdentity,
        args: dict[str, Any],
        context: dict[str, Any],
    ) -> PolicyDecision | None:
        guardrail_rules = [
            rule
            for rule in self._rules
            if rule.conditions.get("rule_type") == "guardrail"
        ]

        for rule in guardrail_rules:
            rule_actions = rule.conditions.get("actions", [])
            rule_roles = rule.conditions.get("roles", [])
            if rule_actions and tool_name not in rule_actions:
                continue
            if rule_roles and identity.role not in rule_roles:
                continue

            check = rule.conditions.get("check")
            if check == "plan_required":
                task = self._task_from_args(identity, args, project_id=context["project_id"])
                if not self._guardrails.check_plan_required(task):
                    return PolicyDecision(
                        allowed=False,
                        reason=rule.description or "plan required before action",
                        requires_approval=False,
                        policy_id=rule.name,
                    )

            if check == "test_required":
                changed_paths = list(args.get("changed_paths", []))
                if not self._guardrails.check_test_required(changed_paths):
                    if not args.get("tests_passed", False):
                        return PolicyDecision(
                            allowed=False,
                            reason=rule.description or "tests required before push",
                            requires_approval=False,
                            policy_id=rule.name,
                        )

            if check == "branch_allowed":
                branch = str(args.get("branch", ""))
                if branch and not self._guardrails.check_branch_allowed(branch):
                    return PolicyDecision(
                        allowed=False,
                        reason=rule.description or f"branch '{branch}' not allowed",
                        requires_approval=False,
                        policy_id=rule.name,
                    )

        return None

    @staticmethod
    def _task_from_args(
        identity: AgentIdentity,
        args: dict[str, Any],
        *,
        project_id: str,
    ) -> Task:
        payload = dict(args.get("task_payload", {}))
        if "plan_submitted" in args:
            payload["plan_submitted"] = args["plan_submitted"]
        if "plan" in args:
            payload["plan"] = args["plan"]
        return Task(
            project_id=project_id,
            agent_id=identity.agent_id,
            task_type=str(args.get("task_type", tool_name_fallback(args))),
            payload=payload,
        )


def tool_name_fallback(args: dict[str, Any]) -> str:
    return str(args.get("task_type", "unknown"))


__all__ = [
    "ApprovalGate",
    "ConditionEvaluator",
    "GuardrailEvaluator",
    "PolicyEngine",
]
