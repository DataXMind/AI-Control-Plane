"""Load and validate projects.yml, agents.yml, policies.yml from config/."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from ai_control_plane.core.models import AgentConfig, ProjectConfig

_CONFIG_FILENAMES = ("projects.yml", "agents.yml", "policies.yml")


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
