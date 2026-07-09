"""Trust-model hardening — A1 role verification, A3 evaluate audit-trail,
A5 schema-conflict warning, A6 dropped-ABAC warning.

Each test reproduces the gap it guards, so a regression re-opens a real hole.
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from structlog.testing import capture_logs

from ai_control_plane.config.loader import load_policies_from_dict
from ai_control_plane.core.models import PolicyRule


def _evaluate(client: TestClient, agent_id: str, tool: str, role: str | None, **args):
    body: dict = {
        "agent_id": agent_id,
        "project_id": "rust-gateway",
        "tool_name": tool,
        "args": args,
    }
    if role is not None:
        body["role"] = role
    return client.post("/policy/evaluate", json=body)


# ── A1 — client-supplied role must match the registry ────────────────────────

def test_a1_claimed_role_not_registered_is_denied(client: TestClient) -> None:
    """agent2 is registered `backend`; claiming `infra` must be rejected."""
    resp = _evaluate(client, "agent2", "k8s_apply", role="infra", plan_submitted=True)
    body = resp.json()
    assert body["allowed"] is False
    assert "claimed role 'infra' not authorized" in body["reason"]


def test_a1_matching_claimed_role_still_works(client: TestClient) -> None:
    """agent2 claiming its real role `backend` is unaffected by the fix."""
    resp = _evaluate(client, "agent2", "git_read", role="backend")
    assert resp.json()["allowed"] is True


def test_a1_no_claimed_role_uses_registry(client: TestClient) -> None:
    """Omitting role falls back to the registered role (backend)."""
    resp = _evaluate(client, "agent2", "git_read", role=None)
    assert resp.json()["allowed"] is True


# ── A3 — every /policy/evaluate decision is written to the audit chain ────────

def test_a3_allow_decision_is_audited(client: TestClient) -> None:
    _evaluate(client, "agent2", "git_read", role="backend")
    events = client.get("/telemetry/events").json()
    evals = [e for e in events if e["event_type"] == "policy.evaluate"]
    assert len(evals) == 1
    assert evals[0]["payload"]["allowed"] is True
    assert evals[0]["payload"]["tool_name"] == "git_read"


def test_a3_deny_decision_is_audited(client: TestClient) -> None:
    _evaluate(client, "agent2", "k8s_apply", role="infra")  # A1 deny
    events = client.get("/telemetry/events").json()
    evals = [e for e in events if e["event_type"] == "policy.evaluate"]
    assert len(evals) == 1
    assert evals[0]["payload"]["allowed"] is False


def test_a3_audit_chain_stays_valid_after_evaluate(client: TestClient) -> None:
    _evaluate(client, "agent2", "git_read", role="backend")
    _evaluate(client, "agent2", "git_push", role="backend")
    assert client.get("/apex/status").json()["telemetry_chain_valid"] is True


# ── A5 — mixing `rules:` and `rbac:`/`abac:` warns instead of silent discard ──

def test_a5_schema_conflict_warns() -> None:
    raw = {
        "rules": [
            {"name": "r1", "conditions": {"rule_type": "rbac", "role": "x"}},
        ],
        "rbac": {"roles": {"backend": {"allowed_actions": ["git.read"]}}},
    }
    with capture_logs() as logs:
        result = load_policies_from_dict(raw)
    assert any(log["event"] == "policies_schema_conflict" for log in logs)
    # pass-through still wins (documented precedence, unchanged)
    assert [r.name for r in result] == ["r1"]


def test_a5_no_conflict_no_warning() -> None:
    raw = {"rbac": {"roles": {"backend": {"allowed_actions": ["git.read"]}}}}
    with capture_logs() as logs:
        load_policies_from_dict(raw)
    assert not any(log["event"] == "policies_schema_conflict" for log in logs)


# ── A6 — an unmappable ABAC entry is dropped WITH a warning, not silently ─────

def test_a6_dropped_abac_entry_warns() -> None:
    raw = {
        "abac": {
            "rules": [
                # 'enviroment' is a typo — no supported key matches → dropped
                {"id": "typo-rule", "effect": "deny", "conditions": {"enviroment": "prod"}},
            ],
        },
    }
    with capture_logs() as logs:
        result = load_policies_from_dict(raw)
    dropped = [log for log in logs if log["event"] == "abac_rule_dropped"]
    assert len(dropped) == 1
    assert dropped[0]["rule_id"] == "typo-rule"
    assert all(isinstance(r, PolicyRule) for r in result)


def test_a6_valid_abac_entry_not_dropped() -> None:
    raw = {
        "abac": {
            "rules": [
                {"id": "ok-rule", "effect": "deny", "conditions": {"environment": "prod"}},
            ],
        },
    }
    with capture_logs() as logs:
        result = load_policies_from_dict(raw)
    assert not any(log["event"] == "abac_rule_dropped" for log in logs)
    assert [r.name for r in result] == ["ok-rule"]
