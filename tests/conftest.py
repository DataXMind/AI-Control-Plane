"""Shared pytest fixtures for ai-control-plane tests."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml  # type: ignore[import-untyped]

from ai_control_plane.core.models import AgentIdentity, PolicyRule, ProjectConfig
from ai_control_plane.core.policies import PolicyEngine

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "config"


@pytest.fixture
def sample_project_config() -> ProjectConfig:
    """rust-gateway with infra, backend, and reviewer roles."""
    return ProjectConfig(
        id="rust-gateway",
        repo="git@github.com:DataXMind/Hybrid-AI-Gateway.git",
        default_branch="main",
        environments={
            "dev": {"k8s_cluster": "test-dev"},
            "stage": {"k8s_cluster": "test-stage"},
            "prod": {"k8s_cluster": "test-prod"},
        },
        roles={
            "infra": {
                "allowed_paths": ["infra/"],
                "environments": ["dev", "stage"],
            },
            "backend": {
                "allowed_paths": ["src/"],
                "environments": ["dev", "stage"],
            },
            "reviewer": {
                "allowed_paths": ["**"],
                "environments": ["dev", "stage", "prod"],
            },
        },
        docs={},
    )


@pytest.fixture
def backend_identity() -> AgentIdentity:
    """agent2 on rust-gateway with backend role."""
    return AgentIdentity(
        agent_id="agent2",
        project_id="rust-gateway",
        role="backend",
        jwt_claims={},
        did=None,
    )


@pytest.fixture
def infra_identity() -> AgentIdentity:
    """agent1 on rust-gateway with infra role."""
    return AgentIdentity(
        agent_id="agent1",
        project_id="rust-gateway",
        role="infra",
        jwt_claims={},
        did=None,
    )


@pytest.fixture
def reviewer_identity() -> AgentIdentity:
    """agent3 on rust-gateway with reviewer role."""
    return AgentIdentity(
        agent_id="agent3",
        project_id="rust-gateway",
        role="reviewer",
        jwt_claims={},
        did=None,
    )


def load_policy_rules_from_dir(config_dir: Path) -> list[PolicyRule]:
    """Load PolicyRule objects from tests/fixtures/config/policies.yml."""
    policies_path = config_dir / "policies.yml"
    raw = yaml.safe_load(policies_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"invalid policies root in {policies_path}"
        raise ValueError(msg)

    rules: list[PolicyRule] = []
    for entry in raw.get("rules", []):
        if not isinstance(entry, dict):
            continue
        rules.append(
            PolicyRule(
                name=str(entry["name"]),
                description=str(entry.get("description", "")),
                conditions=dict(entry["conditions"]),
                effect=entry["effect"],
            ),
        )
    return rules


@pytest.fixture
def mock_policy_engine(sample_project_config: ProjectConfig) -> PolicyEngine:
    """PolicyEngine loaded from tests/fixtures/config/policies.yml."""
    _ = sample_project_config
    rules = load_policy_rules_from_dir(FIXTURES_DIR)
    return PolicyEngine(rules=rules)


@pytest.fixture(autouse=True)
def set_acp_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Copy test YAML configs into an isolated ACP_CONFIG_DIR."""
    for filename in ("projects.yml", "agents.yml", "policies.yml"):
        shutil.copy2(FIXTURES_DIR / filename, tmp_path / filename)
    monkeypatch.setenv("ACP_CONFIG_DIR", str(tmp_path))
    return tmp_path


def evaluate_tool(
    engine: PolicyEngine,
    identity: AgentIdentity,
    tool_name: str,
    args: dict[str, Any] | None = None,
):
    """Helper to evaluate a tool against the identity's project."""
    return engine.evaluate(
        identity,
        tool_name,
        args or {},
        identity.project_id,
    )
