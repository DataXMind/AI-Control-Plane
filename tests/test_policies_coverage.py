"""Additional PolicyEngine / ConditionEvaluator / ApprovalGate coverage (MB-S1-3)."""

from __future__ import annotations

from uuid import uuid4

import pytest

from ai_control_plane.core.models import AgentIdentity, PolicyRule, Task
from ai_control_plane.core.policies import (
    ApprovalGate,
    ConditionEvaluator,
    GuardrailEvaluator,
    PolicyEngine,
    tool_name_fallback,
)

from .conftest import evaluate_tool


def test_approval_gate_request_and_resolve() -> None:
    gate = ApprovalGate()
    req = gate.request("k8s_apply_prod", {"env": "prod"})
    assert req.id is not None
    decision = gate.resolve(str(req.id), approved=True, approver="human@dataxmind.com")
    assert decision.approved is True
    assert decision.approver == "human@dataxmind.com"


def test_approval_gate_unknown_id_raises() -> None:
    gate = ApprovalGate()
    with pytest.raises(KeyError, match="unknown approval_id"):
        gate.resolve(str(uuid4()), approved=True, approver="human")


def test_policy_engine_empty_rules_unknown_role_denies(
    backend_identity: AgentIdentity,
) -> None:
    engine = PolicyEngine(rules=[])
    unknown = backend_identity.model_copy(update={"role": "unknown-role"})
    decision = evaluate_tool(engine, unknown, "git_read")
    assert decision.allowed is False
    assert "no rbac policy" in decision.reason


def test_policy_engine_empty_rules_default_rbac_allows(
    backend_identity: AgentIdentity,
) -> None:
    engine = PolicyEngine(rules=[])
    decision = evaluate_tool(engine, backend_identity, "git_read")
    assert decision.allowed is True


def test_policy_engine_empty_rules_default_rbac_denies_pattern(
    backend_identity: AgentIdentity,
) -> None:
    engine = PolicyEngine(rules=[])
    decision = evaluate_tool(engine, backend_identity, "k8s_apply_dev")
    assert decision.allowed is False


def test_policy_engine_empty_rules_default_rbac_unknown_tool(
    infra_identity: AgentIdentity,
) -> None:
    engine = PolicyEngine(rules=[])
    decision = evaluate_tool(engine, infra_identity, "totally_unknown_tool")
    assert decision.allowed is False
    assert "not in allowed_actions" in decision.reason


def test_policy_engine_project_mismatch(backend_identity: AgentIdentity) -> None:
    engine = PolicyEngine(rules=[])
    decision = engine.evaluate(
        backend_identity,
        "git_read",
        {},
        "other-project",
    )
    assert decision.allowed is False
    assert "does not match" in decision.reason


def test_condition_evaluator_path_and_action() -> None:
    evaluator = ConditionEvaluator()
    assert evaluator.evaluate(
        {"rule_type": "abac", "path": "src/", "environment": "dev"},
        {"path": "src/main.py", "environment": "dev", "action": "git_read"},
    )
    assert not evaluator.evaluate(
        {"rule_type": "abac", "path": "src/", "environment": "dev"},
        {"path": "infra/main.py", "environment": "dev", "action": "git_read"},
    )
    assert not evaluator.evaluate(
        {"rule_type": "abac", "action": "git_read"},
        {"action": "git_commit"},
    )


def test_condition_evaluator_role_not_in_and_actions() -> None:
    evaluator = ConditionEvaluator()
    assert evaluator.evaluate(
        {
            "rule_type": "abac",
            "data_category": "PII",
            "role_not_in": ["reviewer"],
            "actions": ["git_read"],
        },
        {"role": "backend", "data_category": "PII", "action": "git_read"},
    )
    assert not evaluator.evaluate(
        {
            "rule_type": "abac",
            "data_category": "PII",
            "role_not_in": ["reviewer"],
            "actions": ["git_read"],
        },
        {"role": "reviewer", "data_category": "PII", "action": "git_read"},
    )
    assert not evaluator.evaluate(
        {"rule_type": "abac", "actions": ["git_read"]},
        {"action": "git_commit"},
    )


def test_condition_evaluator_read_only_and_custom_writes() -> None:
    evaluator = ConditionEvaluator()
    assert evaluator.eval_read_only("reviewer", "git_read") is False
    assert evaluator.eval_read_only("reviewer", "git_commit") is True
    assert evaluator.eval_read_only("reviewer", "custom_write", ["custom_write"]) is True
    assert evaluator.evaluate(
        {"rule_type": "abac", "role": "reviewer", "read_only": True},
        {"role": "reviewer", "action": "git_read"},
    )
    assert not evaluator.evaluate(
        {"rule_type": "abac", "role": "reviewer", "read_only": True},
        {"role": "reviewer", "action": "git_commit"},
    )


def test_guardrail_evaluator_plan_test_branch() -> None:
    plan_rule = PolicyRule(
        name="plan-check",
        description="plan required",
        effect="deny",
        conditions={"rule_type": "guardrail", "check": "plan_required", "plan_field": "plan"},
    )
    test_rule = PolicyRule(
        name="test-check",
        description="tests required",
        effect="deny",
        conditions={
            "rule_type": "guardrail",
            "check": "test_required",
            "test_required_prefixes": ["src/"],
        },
    )
    branch_rule = PolicyRule(
        name="branch-check",
        description="branch blocked",
        effect="deny",
        conditions={
            "rule_type": "guardrail",
            "check": "branch_allowed",
            "forbidden_branches": ["main"],
        },
    )
    evaluator = GuardrailEvaluator([plan_rule, test_rule, branch_rule])

    task_without_plan = Task(
        project_id="rust-gateway",
        agent_id="agent1",
        task_type="k8s_apply",
        payload={},
    )
    assert evaluator.check_plan_required(task_without_plan) is False
    task_with_plan = task_without_plan.model_copy(update={"payload": {"plan": "ok"}})
    assert evaluator.check_plan_required(task_with_plan) is True

    assert evaluator.check_test_required(["docs/readme.md"]) is True
    assert evaluator.check_test_required(["src/main.rs"]) is False

    assert evaluator.check_branch_allowed("feature/x") is True
    assert evaluator.check_branch_allowed("main") is False


def test_guardrail_evaluator_defaults_without_rules() -> None:
    evaluator = GuardrailEvaluator([])
    task = Task(
        project_id="rust-gateway",
        agent_id="agent1",
        task_type="k8s_apply",
        payload={"plan_submitted": True},
    )
    assert evaluator.check_plan_required(task) is True
    assert evaluator.check_test_required(["docs/readme.md"]) is True
    assert evaluator.check_branch_allowed("main") is False


def test_policy_engine_guardrail_checks_via_evaluate(
    infra_identity: AgentIdentity,
) -> None:
    rules = [
        PolicyRule(
            name="rbac-infra",
            description="infra rbac",
            effect="allow",
            conditions={
                "rule_type": "rbac",
                "role": "infra",
                "allowed_actions": ["k8s_apply", "git_push"],
                "denied_actions": [],
                "denied_patterns": [],
                "allowed_patterns": [],
            },
        ),
        PolicyRule(
            name="require-plan",
            description="plan required before k8s apply",
            effect="deny",
            conditions={
                "rule_type": "guardrail",
                "check": "plan_required",
                "actions": ["k8s_apply"],
                "roles": ["infra"],
            },
        ),
        PolicyRule(
            name="require-tests",
            description="tests required before push",
            effect="deny",
            conditions={
                "rule_type": "guardrail",
                "check": "test_required",
                "actions": ["git_push"],
                "roles": ["infra"],
            },
        ),
        PolicyRule(
            name="block-main",
            description="no push to main",
            effect="deny",
            conditions={
                "rule_type": "guardrail",
                "check": "branch_allowed",
                "actions": ["git_push"],
                "roles": ["infra"],
            },
        ),
    ]
    engine = PolicyEngine(rules=rules)

    deny_plan = evaluate_tool(engine, infra_identity, "k8s_apply")
    assert deny_plan.allowed is False
    assert deny_plan.policy_id == "require-plan"

    allow_plan = evaluate_tool(
        engine,
        infra_identity,
        "k8s_apply",
        {"plan_submitted": True, "task_payload": {"plan_submitted": True}},
    )
    assert allow_plan.allowed is True

    deny_tests = evaluate_tool(
        engine,
        infra_identity,
        "git_push",
        {"changed_paths": ["src/main.rs"]},
    )
    assert deny_tests.allowed is False
    assert deny_tests.policy_id == "require-tests"

    allow_tests = evaluate_tool(
        engine,
        infra_identity,
        "git_push",
        {"changed_paths": ["src/main.rs"], "tests_passed": True},
    )
    assert allow_tests.allowed is True

    deny_branch = evaluate_tool(
        engine,
        infra_identity,
        "git_push",
        {"branch": "main"},
    )
    assert deny_branch.allowed is False
    assert deny_branch.policy_id == "block-main"


def test_rbac_explicit_denied_action(backend_identity: AgentIdentity) -> None:
    rules = [
        PolicyRule(
            name="rbac-backend",
            description="backend",
            effect="allow",
            conditions={
                "rule_type": "rbac",
                "role": "backend",
                "allowed_actions": ["git_read"],
                "denied_actions": ["git_read"],
                "denied_patterns": [],
                "allowed_patterns": [],
            },
        ),
    ]
    engine = PolicyEngine(rules=rules)
    decision = evaluate_tool(engine, backend_identity, "git_read")
    assert decision.allowed is False
    assert "denied for role" in decision.reason


def test_abac_deny_uses_description_fallback(backend_identity: AgentIdentity) -> None:
    rules = [
        PolicyRule(
            name="rbac-backend",
            description="backend",
            effect="allow",
            conditions={
                "rule_type": "rbac",
                "role": "backend",
                "allowed_actions": ["git_read", "create_pr"],
                "denied_actions": [],
                "denied_patterns": [],
                "allowed_patterns": [],
            },
        ),
        PolicyRule(
            name="deny-custom",
            description="",
            effect="deny",
            conditions={"rule_type": "abac", "environment": "prod", "action": "create_pr"},
        ),
    ]
    engine = PolicyEngine(rules=rules)
    decision = evaluate_tool(
        engine,
        backend_identity,
        "create_pr",
        {"environment": "prod"},
    )
    assert decision.allowed is False
    assert decision.policy_id == "deny-custom"
    assert "denied by rule" in decision.reason


def test_tool_name_fallback() -> None:
    assert tool_name_fallback({"task_type": "git_read"}) == "git_read"
    assert tool_name_fallback({}) == "unknown"
