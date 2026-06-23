"""Load and validate projects.yml, agents.yml, policies.yml from config/."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import yaml  # type: ignore[import-untyped]

from ai_control_plane.core.exceptions import ConfigError
from ai_control_plane.core.models import (
    AgentConfig,
    KillSwitch,
    ModelProfile,
    PolicyRule,
    ProjectConfig,
)
from ai_control_plane.core.tool_names import normalize_tool_name

_CONFIG_FILENAMES = ("projects.yml", "agents.yml", "policies.yml")

_REQUIREMENT_CHECKS: dict[str, str] = {
    "plan_submitted": "plan_required",
    "tests_passed": "test_required",
    "branch_is_not_default": "branch_allowed",
}


def derive_denied_patterns(denied_actions: list[str]) -> list[str]:
    """Derive wildcard deny patterns from normalized denied action names."""
    patterns: list[str] = []
    for raw in denied_actions:
        normalized = normalize_tool_name(raw)
        if normalized == "k8s_apply" or normalized.startswith("k8s_apply_"):
            patterns.append("k8s_apply_*")
    return list(dict.fromkeys(patterns))


def derive_allowed_patterns(allowed_actions: list[str]) -> list[str]:
    """Derive wildcard allow patterns from normalized allowed action names."""
    patterns: list[str] = []
    for raw in allowed_actions:
        normalized = normalize_tool_name(raw)
        if normalized == "k8s_apply" or normalized.startswith("k8s_apply_"):
            patterns.append("k8s_apply_*")
    return list(dict.fromkeys(patterns))


def default_config_dir() -> Path:
    """Return shipped defaults config/ relative to the repository root."""
    repo_config = Path(__file__).resolve().parents[3] / "config"
    if repo_config.is_dir():
        return repo_config
    return Path("config")


def get_config_dir() -> Path:
    """Resolve config directory from ACP_CONFIG_DIR or shipped defaults."""
    override = os.environ.get("ACP_CONFIG_DIR")
    if override:
        return Path(override)
    return default_config_dir()


def _load_yaml(filename: str) -> dict[str, Any]:
    path = get_config_dir() / filename
    if not path.is_file():
        msg = f"config file not found: {path}"
        raise FileNotFoundError(msg)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"invalid yaml root in {path}"
        raise ValueError(msg)
    return raw


def _policy_rule_from_entry(entry: dict[str, Any]) -> PolicyRule:
    effect = entry.get("effect", "allow")
    if effect not in ("allow", "deny"):
        msg = f"invalid policy effect '{effect}'"
        raise ValueError(msg)
    return PolicyRule(
        name=str(entry["name"]),
        description=str(entry.get("description", "")),
        conditions=dict(entry["conditions"]),
        effect=effect,
    )


def _load_pass_through_rules(raw: dict[str, Any]) -> list[PolicyRule]:
    """Load explicit PolicyRule list (tests/fixtures format)."""
    rules: list[PolicyRule] = []
    for entry in raw.get("rules", []):
        if isinstance(entry, dict) and "name" in entry and "conditions" in entry:
            rules.append(_policy_rule_from_entry(entry))
    return rules


def _load_rbac_rules(raw: dict[str, Any]) -> list[PolicyRule]:
    """Map rbac.roles.* from production policies.yml to PolicyRule RBAC entries."""
    rbac_section = raw.get("rbac", {})
    if not isinstance(rbac_section, dict):
        return []

    roles = rbac_section.get("roles", {})
    if not isinstance(roles, dict):
        return []

    rules: list[PolicyRule] = []
    for role_name, role_cfg in roles.items():
        if not isinstance(role_cfg, dict):
            continue

        allowed_raw = role_cfg.get("allowed_actions", [])
        denied_raw = role_cfg.get("denied_actions", [])
        allowed_actions = [
            normalize_tool_name(str(action))
            for action in allowed_raw
            if isinstance(action, str)
        ]
        denied_actions = [
            normalize_tool_name(str(action))
            for action in denied_raw
            if isinstance(action, str)
        ]
        denied_patterns = derive_denied_patterns(
            [str(action) for action in denied_raw if isinstance(action, str)],
        )
        allowed_patterns = derive_allowed_patterns(
            [str(action) for action in allowed_raw if isinstance(action, str)],
        )

        rules.append(
            PolicyRule(
                name=f"rbac-{role_name}",
                description=str(role_cfg.get("description", f"RBAC policy for role {role_name}")),
                effect="allow",
                conditions={
                    "rule_type": "rbac",
                    "role": str(role_name),
                    "allowed_actions": allowed_actions,
                    "denied_actions": denied_actions,
                    "denied_patterns": denied_patterns,
                    "allowed_patterns": allowed_patterns,
                },
            ),
        )
    return rules


def _map_abac_entry(entry: dict[str, Any]) -> PolicyRule | None:
    """Map one production abac.rules[] entry to engine PolicyRule."""
    name = str(entry.get("id") or entry.get("name", "abac-rule"))
    description = str(entry.get("description", ""))
    effect_raw = entry.get("effect", "allow")
    if effect_raw not in ("allow", "deny"):
        return None
    effect: Literal["allow", "deny"] = effect_raw

    conditions = entry.get("conditions", {})
    if not isinstance(conditions, dict):
        return None

    mapped: dict[str, Any] = {"rule_type": "abac"}

    data_class = conditions.get("data_class")
    if data_class is not None:
        mapped["data_category"] = str(data_class).upper()

    for key in ("environment", "role", "path", "approval_status", "read_only"):
        if key in conditions:
            mapped[key] = conditions[key]

    role_not_in = conditions.get("role_not_in")
    if isinstance(role_not_in, list):
        mapped["role_not_in"] = [str(role) for role in role_not_in]

    if "requires_approval" in conditions:
        mapped["requires_approval"] = bool(conditions["requires_approval"])

    actions = entry.get("actions", [])
    if isinstance(actions, list) and actions:
        normalized: list[str] = []
        for action in actions:
            if not isinstance(action, str):
                continue
            action_norm = normalize_tool_name(action)
            normalized.append("k8s_apply_*" if action_norm == "k8s_apply" else action_norm)
        if len(normalized) == 1:
            mapped["action"] = normalized[0]
        elif normalized:
            mapped["actions"] = normalized

    if mapped.get("data_category") and "role_not_in" not in mapped:
        mapped.pop("actions", None)
        mapped.pop("action", None)
    elif "action" in conditions:
        action_norm = normalize_tool_name(str(conditions["action"]))
        mapped["action"] = "k8s_apply_*" if action_norm == "k8s_apply" else action_norm

    supported = {
        "rule_type",
        "environment",
        "role",
        "path",
        "action",
        "actions",
        "data_category",
        "requires_approval",
        "role_not_in",
        "approval_status",
        "read_only",
    }
    if not supported.intersection(set(mapped.keys()) - {"rule_type"}):
        return None

    return PolicyRule(
        name=name,
        description=description,
        effect=effect,
        conditions=mapped,
    )


def _load_abac_rules(raw: dict[str, Any]) -> list[PolicyRule]:
    """Map abac.rules[] from production policies.yml (skips unmappable entries)."""
    abac_section = raw.get("abac", {})
    if not isinstance(abac_section, dict):
        return []

    rules_raw = abac_section.get("rules", [])
    if not isinstance(rules_raw, list):
        return []

    rules: list[PolicyRule] = []
    for entry in rules_raw:
        if not isinstance(entry, dict):
            continue
        mapped = _map_abac_entry(entry)
        if mapped is not None:
            rules.append(mapped)
    return rules


def load_policies_from_dict(raw: dict[str, Any]) -> list[PolicyRule]:
    """Parse policies YAML root dict into PolicyRule list for PolicyEngine."""
    pass_through = _load_pass_through_rules(raw)
    if pass_through:
        return pass_through
    return _load_rbac_rules(raw) + _load_abac_rules(raw)


def load_policies(policies_path: Path | None = None) -> list[PolicyRule]:
    """Load policies.yml → list[PolicyRule] for PolicyEngine."""
    path = policies_path if policies_path is not None else get_config_dir() / "policies.yml"
    if not path.is_file():
        msg = f"policies file not found: {path}"
        raise FileNotFoundError(msg)

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"invalid policies root in {path}"
        raise ValueError(msg)

    rules = load_policies_from_dict(raw)
    if not rules:
        msg = f"no policy rules loaded from {path}"
        raise ValueError(msg)
    return rules


def load_projects() -> dict[str, ProjectConfig]:
    """Load all projects keyed by project id."""
    data = _load_yaml("projects.yml")
    projects: dict[str, ProjectConfig] = {}
    for project_id, entry in data.get("projects", {}).items():
        if not isinstance(entry, dict):
            continue
        projects[project_id] = ProjectConfig(
            id=project_id,
            repo=str(entry["repo"]),
            default_branch=str(entry.get("default_branch", "main")),
            environments=dict(entry.get("environments", {})),
            roles=dict(entry.get("roles", {})),
            docs=dict(entry.get("docs", {})),
        )
    return projects


def load_project(project_id: str) -> ProjectConfig:
    """Load a single project or raise KeyError."""
    projects = load_projects()
    if project_id not in projects:
        msg = f"unknown project '{project_id}'"
        raise KeyError(msg)
    return projects[project_id]


def load_agents_raw() -> dict[str, dict[str, Any]]:
    """Load raw agent entries from agents.yml."""
    data = _load_yaml("agents.yml")
    agents = data.get("agents", {})
    if not isinstance(agents, dict):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for agent_id, entry in agents.items():
        if isinstance(entry, dict):
            result[str(agent_id)] = dict(entry)
    return result


def load_model_profiles() -> dict[str, ModelProfile]:
    """Load model profile definitions from agents.yml into validated ModelProfile objects."""
    data = _load_yaml("agents.yml")
    profiles_raw = data.get("model_profiles", {})
    if not isinstance(profiles_raw, dict):
        return {}

    profiles: dict[str, ModelProfile] = {}
    for name, entry in profiles_raw.items():
        if not isinstance(entry, dict):
            continue
        profiles[str(name)] = ModelProfile(
            name=str(name),
            provider=str(entry["provider"]),
            account_type=str(entry["account_type"]),
            api_key_env=str(entry["api_key_env"]),
            max_tokens_per_day=int(entry["max_tokens_per_day"]),
            allowed_tasks=[str(task) for task in entry.get("allowed_tasks", [])],
        )
    return profiles


def load_agent(agent_id: str) -> AgentConfig:
    """Load a single agent config or raise KeyError."""
    agents = load_agents_raw()
    if agent_id not in agents:
        msg = f"unknown agent '{agent_id}'"
        raise KeyError(msg)
    entry = agents[agent_id]
    return AgentConfig(
        id=agent_id,
        name=str(entry["name"]),
        roles=[str(role) for role in entry.get("roles", [])],
        runner=str(entry["runner"]),
        model_profile=str(entry["model_profile"]),
        capabilities=[str(value) for value in entry.get("capabilities", [])],
        restrictions=[str(value) for value in entry.get("restrictions", [])],
    )


def agent_projects(agent_id: str) -> list[str]:
    """Return project ids bound to *agent_id*."""
    agents = load_agents_raw()
    if agent_id not in agents:
        msg = f"unknown agent '{agent_id}'"
        raise KeyError(msg)
    projects = agents[agent_id].get("projects", [])
    if not isinstance(projects, list):
        return []
    return [str(project_id) for project_id in projects]


def validate_agent_in_project(agent_id: str, project_id: str) -> AgentConfig:
    """Ensure *agent_id* exists and is registered for *project_id*."""
    load_project(project_id)
    agent = load_agent(agent_id)
    if project_id not in agent_projects(agent_id):
        msg = f"agent '{agent_id}' is not registered for project '{project_id}'"
        raise ValueError(msg)
    return agent


def build_agent_registry() -> dict[str, dict[str, Any]]:
    """Build API agent registry from agents.yml (role, projects, metadata)."""
    agents = load_agents_raw()
    if not agents:
        msg = "no agents loaded from agents.yml"
        raise ConfigError(msg)

    registry: dict[str, dict[str, Any]] = {}
    for agent_id, entry in agents.items():
        roles_raw = entry.get("roles", [])
        roles = [str(role) for role in roles_raw] if isinstance(roles_raw, list) else []
        projects_raw = entry.get("projects", [])
        projects = (
            [str(project_id) for project_id in projects_raw]
            if isinstance(projects_raw, list)
            else []
        )
        registry[agent_id] = {
            "role": roles[0] if roles else None,
            "roles": roles,
            "projects": projects,
            "name": str(entry.get("name", agent_id)),
            "model_profile": str(entry.get("model_profile", "")),
        }
    return registry


def load_project_token_limits() -> dict[str, float]:
    """Load per-project daily token limits from policies.yml quotas.by_project."""
    path = get_config_dir() / "policies.yml"
    if not path.is_file():
        msg = f"policies file not found: {path}"
        raise ConfigError(msg)

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"invalid policies root in {path}"
        raise ConfigError(msg)

    quotas = raw.get("quotas", {})
    if not isinstance(quotas, dict):
        return {}

    by_project = quotas.get("by_project", {})
    if not isinstance(by_project, dict):
        return {}

    limits: dict[str, float] = {}
    for project_id, entry in by_project.items():
        if not isinstance(entry, dict):
            continue
        tokens = entry.get("tokens_per_day")
        if tokens is not None:
            limits[str(project_id)] = float(tokens)
    return limits


def _normalize_guardrail_effect(effect: Any) -> Literal["allow", "deny"]:
    if effect == "allow":
        return "allow"
    if effect == "deny":
        return "deny"
    return "deny"


def load_guardrails(path: Path) -> list[PolicyRule]:
    """Load guardrails section from policies.yml → PolicyRule with rule_type='guardrail'."""
    if not path.is_file():
        return []

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return []

    guardrails_raw = raw.get("guardrails", [])
    if not isinstance(guardrails_raw, list):
        return []

    rules: list[PolicyRule] = []
    for gr in guardrails_raw:
        if not isinstance(gr, dict):
            continue

        name = str(gr.get("name") or gr.get("id", "guardrail"))
        applies_to = gr.get("applies_to", {})
        if not isinstance(applies_to, dict):
            applies_to = {}

        roles_raw = applies_to.get("roles", [])
        actions_raw = applies_to.get("actions", [])
        roles_list = [str(role) for role in roles_raw] if isinstance(roles_raw, list) else []
        actions_list = [
            normalize_tool_name(str(action))
            for action in actions_raw
            if isinstance(action, str)
        ]

        conditions: dict[str, Any] = {
            "rule_type": "guardrail",
            "applies_to": applies_to,
        }
        if roles_list:
            conditions["roles"] = roles_list
        if actions_list:
            conditions["actions"] = actions_list

        requirement = gr.get("requirement")
        if isinstance(requirement, str) and requirement in _REQUIREMENT_CHECKS:
            conditions["check"] = _REQUIREMENT_CHECKS[requirement]

        branches = applies_to.get("branches")
        if isinstance(branches, list) and branches:
            conditions["check"] = "branch_allowed"
            conditions["forbidden_branches"] = [str(branch) for branch in branches]

        raw_effect = gr.get("on_violation", gr.get("effect", "deny"))
        effect = _normalize_guardrail_effect(raw_effect)
        if raw_effect not in ("allow", "deny"):
            conditions["guardrail_effect"] = str(raw_effect)

        rules.append(
            PolicyRule(
                name=name,
                description=str(gr.get("description", "")),
                conditions=conditions,
                effect=effect,
            ),
        )
    return rules


def load_kill_switch(path: Path) -> KillSwitch:
    """Load kill_switch section → KillSwitch. Default: inactive."""
    if not path.is_file():
        return KillSwitch()

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return KillSwitch()

    ks = raw.get("kill_switch", {})
    if not isinstance(ks, dict):
        return KillSwitch()

    active = bool(ks.get("active", ks.get("enabled", False)))
    return KillSwitch(
        active=active,
        reason=str(ks.get("reason", "")),
    )
