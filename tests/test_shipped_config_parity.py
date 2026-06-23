"""Shipped config/ parity — CI validates repo config/, not only fixtures.

Uses @pytest.mark.shipped_config to override conftest autouse fixture dir.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app
from ai_control_plane.config.loader import load_policies
from ai_control_plane.core.models import AgentIdentity
from ai_control_plane.core.policies import PolicyEngine

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_CONFIG_DIR = REPO_ROOT / "config"

pytestmark = pytest.mark.shipped_config


@pytest.fixture
def shipped_acp_config(monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point ACP_CONFIG_DIR at shipped config/ (overrides conftest autouse)."""
    monkeypatch.setenv("ACP_CONFIG_DIR", str(SHIPPED_CONFIG_DIR))
    return SHIPPED_CONFIG_DIR


def test_shipped_policies_load_non_empty(shipped_acp_config: Path) -> None:
    _ = shipped_acp_config
    rules = load_policies(SHIPPED_CONFIG_DIR / "policies.yml")
    rbac = [r for r in rules if r.conditions.get("rule_type") == "rbac"]
    assert len(rbac) >= 3


def test_shipped_backend_git_read_allowed(shipped_acp_config: Path) -> None:
    _ = shipped_acp_config
    rules = load_policies(SHIPPED_CONFIG_DIR / "policies.yml")
    engine = PolicyEngine(rules=rules)
    identity = AgentIdentity(
        agent_id="agent2",
        project_id="rust-gateway",
        role="backend",
        jwt_claims={},
        did=None,
    )
    decision = engine.evaluate(identity, "git_read", {}, "rust-gateway")
    assert decision.allowed is True


def test_shipped_health_wire_proof(shipped_acp_config: Path) -> None:
    _ = shipped_acp_config
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["config_loaded"] is True
    assert body["policy_rules_count"] >= 3
    assert "agent2" in body["agents_loaded"]
    assert "rust-gateway" in body["projects_loaded"]


def test_shipped_policy_evaluate_dot_notation(shipped_acp_config: Path) -> None:
    _ = shipped_acp_config
    client = TestClient(create_app())
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "agent2",
            "project_id": "rust-gateway",
            "tool_name": "git.read",
            "role": "backend",
        },
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is True
