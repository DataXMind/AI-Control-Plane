"""Load and validate projects.yml, agents.yml, policies.yml from config/."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import yaml  # type: ignore[import-untyped]

from ai_control_plane.core.models import AgentConfig, PolicyRule, ProjectConfig

_CONFIG_FILENAMES = ("projects.yml", "agents.yml", "policies.yml")

_UNSUPPORTED_ABAC_KEYS = frozenset({"role_not_in", "approval_status", "read_only"})


def normalize_tool_name(name: str) -> str:
    """Convert config dot notation to engine snake_case (git.read → git_read)."""
    return name.replace(".", "_").replace("-", "_")


def derive_denied_patterns(denied_actions: list[str]) -> list[str]:
    """Derive wildcard deny patterns from normalized denied action names."""
    patterns: list[str] = []
    for raw in denied_actions:
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
        effect=effect,  # type: ignore[arg-type]
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
                },
            ),
        )
    return rules


def _map_abac_entry(entry: dict[str, Any]) -> PolicyRule | None:
    """Map one production abac.rules[] entry to engine PolicyRule (Milestone A subset)."""
    name = str(entry.get("id") or entry.get("name", "abac-rule"))
    description = str(entry.get("description", ""))
    effect_raw = entry.get("effect", "allow")
    if effect_raw not in ("allow", "deny"):
        return None
    effect: Literal["allow", "deny"] = effect_raw

    conditions = entry.get("conditions", {})
    if not isinstance(conditions, dict):
        return None

    data_class = conditions.get("data_class")
    if data_class is not None:
        category = str(data_class).upper()
        if category == "PII":
            return PolicyRule(
                name=name,
                description=description,
                effect="deny",
                conditions={"rule_type": "abac", "data_category": "PII"},
            )

    if _UNSUPPORTED_ABAC_KEYS.intersection(conditions.keys()):
        return None

    mapped: dict[str, Any] = {"rule_type": "abac"}
    for key in ("environment", "role", "path"):
        if key in conditions:
            mapped[key] = conditions[key]

    if "requires_approval" in conditions:
        mapped["requires_approval"] = bool(conditions["requires_approval"])

    actions = entry.get("actions", [])
    if isinstance(actions, list) and len(actions) == 1:
        mapped["action"] = normalize_tool_name(str(actions[0]))
    elif "action" in conditions:
        mapped["action"] = normalize_tool_name(str(conditions["action"]))

    supported = {
        "rule_type",
        "environment",
        "role",
        "path",
        "action",
        "data_category",
        "requires_approval",
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
