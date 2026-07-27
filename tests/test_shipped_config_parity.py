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
    assert "claude-pro-backend" in body["model_profiles_loaded"]


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


def test_shipped_restrict_pii_role_not_in_exemption(shipped_acp_config: Path) -> None:
    """Shipped Restrict-PII must honor role_not_in reviewer exemption (GAP-ABAC-2)."""
    _ = shipped_acp_config
    rules = load_policies(SHIPPED_CONFIG_DIR / "policies.yml")
    engine = PolicyEngine(rules=rules)
    backend = AgentIdentity(
        agent_id="agent2",
        project_id="rust-gateway",
        role="backend",
        jwt_claims={},
        did=None,
    )
    reviewer = AgentIdentity(
        agent_id="agent3",
        project_id="rust-gateway",
        role="reviewer",
        jwt_claims={},
        did=None,
    )
    pii_context = {"data_category": "PII"}

    deny = engine.evaluate(backend, "git_read", pii_context, "rust-gateway")
    assert deny.allowed is False
    assert deny.policy_id == "Restrict-PII"

    allow = engine.evaluate(reviewer, "git_read", pii_context, "rust-gateway")
    assert allow.allowed is True


def test_shipped_deny_prod_k8s_blocks_k8s_apply_multi_action_rule(
    shipped_acp_config: Path,
) -> None:
    """F-01 regression: shipped Deny-prod-k8s has 3 actions (multi-action ABAC
    'actions' key) — the fixture-only test suite used a 1-action rule that maps
    to the singular 'action' key and masked this. 'infra' is RBAC-allowed
    k8s.apply in general; ABAC must still block it in prod without approval.
    """
    _ = shipped_acp_config
    rules = load_policies(SHIPPED_CONFIG_DIR / "policies.yml")
    engine = PolicyEngine(rules=rules)
    infra = AgentIdentity(
        agent_id="agent1",
        project_id="rust-gateway",
        role="infra",
        jwt_claims={},
        did=None,
    )
    prod_unapproved = {"environment": "prod", "approval_status": "not_approved"}

    deny_apply = engine.evaluate(infra, "k8s_apply", prod_unapproved, "rust-gateway")
    assert deny_apply.allowed is False
    assert deny_apply.policy_id == "Deny-prod-k8s"
    assert deny_apply.evaluation_path == "abac"

    # Same rule's helm.upgrade action (RBAC-allowed for infra, same as k8s.apply)
    # was already correctly denied before this fix (no wildcard substitution
    # applied to it, since only "k8s_apply" triggers that in the loader) — lock
    # in as regression cover so the fix doesn't accidentally narrow this path.
    deny_helm = engine.evaluate(infra, "helm_upgrade", prod_unapproved, "rust-gateway")
    assert deny_helm.allowed is False
    assert deny_helm.policy_id == "Deny-prod-k8s"

    # Same role/action outside prod, or approved, must remain allowed — the fix
    # must not turn this into an unconditional deny.
    allow_dev = engine.evaluate(
        infra, "k8s_apply", {"environment": "dev"}, "rust-gateway"
    )
    assert allow_dev.allowed is True

    allow_approved = engine.evaluate(
        infra,
        "k8s_apply",
        {"environment": "prod", "approval_status": "approved"},
        "rust-gateway",
    )
    assert allow_approved.allowed is True
