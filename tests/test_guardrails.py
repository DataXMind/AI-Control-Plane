"""Guardrails + kill_switch loading and runtime enforcement (MB-S1-1)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from fastapi.testclient import TestClient

from ai_control_plane.api.server import build_default_app_state, create_app
from ai_control_plane.config.loader import (
    get_config_dir,
    load_guardrails,
    load_kill_switch,
    load_policies,
)
from ai_control_plane.core.models import KillSwitch
from ai_control_plane.core.policies import PolicyEngine

from .conftest import FIXTURES_DIR, evaluate_tool

FIXTURE_POLICIES = FIXTURES_DIR / "policies.yml"


def test_kill_switch_denies_all_evaluate(backend_identity) -> None:
    engine = PolicyEngine(rules=[], kill_switch=KillSwitch(active=True, reason="maintenance"))
    decision = engine.evaluate(backend_identity, "git_read", {}, "rust-gateway")
    assert decision.allowed is False
    assert "kill_switch_active" in decision.reason
    assert "maintenance" in decision.reason


def test_kill_switch_inactive_passes_through(backend_identity) -> None:
    sample_rules = load_policies(FIXTURE_POLICIES)
    engine = PolicyEngine(rules=sample_rules, kill_switch=KillSwitch(active=False))
    decision = evaluate_tool(engine, backend_identity, "git_read")
    assert decision.allowed is True


def test_load_guardrails_from_yml() -> None:
    rules = load_guardrails(FIXTURE_POLICIES)
    guardrail_names = [rule.name for rule in rules]
    assert "Require-plan-before-code" in guardrail_names
    assert "No-direct-merge-to-main" in guardrail_names


def _app_state_with_kill_switch(*, active: bool, reason: str = "maintenance"):
    state = build_default_app_state()
    policies_path = get_config_dir() / "policies.yml"
    all_rules = load_policies(policies_path) + load_guardrails(policies_path)
    engine = PolicyEngine(
        rules=all_rules,
        kill_switch=KillSwitch(active=active, reason=reason),
    )
    return replace(state, policy_engine=engine)


def test_health_not_blocked_by_kill_switch() -> None:
    state = _app_state_with_kill_switch(active=True)
    client = TestClient(create_app(state=state))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_policy_evaluate_blocked_by_kill_switch() -> None:
    state = _app_state_with_kill_switch(active=True)
    client = TestClient(create_app(state=state))
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
    body = response.json()
    assert body["allowed"] is False
    assert "kill_switch_active" in body["reason"]


def test_load_kill_switch_enabled_alias(tmp_path: Path) -> None:
    """Shipped config uses enabled:; loader accepts active or enabled."""
    policies = tmp_path / "policies.yml"
    policies.write_text(
        "kill_switch:\n  enabled: true\n  reason: drill\n",
        encoding="utf-8",
    )
    ks = load_kill_switch(policies)
    assert ks.active is True
    assert ks.reason == "drill"
