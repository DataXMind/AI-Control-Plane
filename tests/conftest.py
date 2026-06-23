"""Shared pytest fixtures for ai-control-plane tests."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from ai_control_plane.config.loader import load_policies
from ai_control_plane.core.models import AgentIdentity, ProjectConfig
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


@pytest.fixture
def mock_policy_engine(sample_project_config: ProjectConfig) -> PolicyEngine:
    """PolicyEngine loaded from tests/fixtures/config/policies.yml."""
    _ = sample_project_config
    rules = load_policies(FIXTURES_DIR / "policies.yml")
    return PolicyEngine(rules=rules)


@pytest.fixture
def app():
    """FastAPI application with fixture config (ACP_CONFIG_DIR from autouse)."""
    from ai_control_plane.api.server import create_app

    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    """FastAPI TestClient with fixture config (ACP_CONFIG_DIR from autouse)."""
    return TestClient(app)


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
