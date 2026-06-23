"""Tests for config/loader.py — policies.yml → PolicyRule adapter (NEW-5)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_control_plane.config.loader import (
    derive_denied_patterns,
    load_policies,
    normalize_tool_name,
)
from ai_control_plane.core.models import AgentIdentity
from ai_control_plane.core.policies import PolicyEngine

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_POLICIES = REPO_ROOT / "config" / "policies.yml"
FIXTURE_POLICIES = Path(__file__).resolve().parent / "fixtures" / "config" / "policies.yml"


@pytest.fixture
def backend_identity() -> AgentIdentity:
    return AgentIdentity(
        agent_id="agent2",
        project_id="rust-gateway",
        role="backend",
        jwt_claims={},
        did=None,
    )


def test_normalize_tool_name_dot_to_snake() -> None:
    assert normalize_tool_name("git.read") == "git_read"
    assert normalize_tool_name("k8s.apply") == "k8s_apply"
    assert normalize_tool_name("git_read") == "git_read"


def test_derive_denied_patterns_k8s_apply() -> None:
    patterns = derive_denied_patterns(["k8s.apply"])
    assert "k8s_apply_*" in patterns


def test_load_policies_shipped_config_not_empty() -> None:
    rules = load_policies(SHIPPED_POLICIES)
    assert len(rules) >= 3
    rbac_rules = [rule for rule in rules if rule.conditions.get("rule_type") == "rbac"]
    assert len(rbac_rules) >= 3


def test_load_policies_fixture_pass_through() -> None:
    rules = load_policies(FIXTURE_POLICIES)
    names = {rule.name for rule in rules}
    assert "rbac-backend" in names
    assert "deny-pii" in names


def test_load_policies_rbac_backend_conditions() -> None:
    rules = load_policies(SHIPPED_POLICIES)
    backend = next(rule for rule in rules if rule.name == "rbac-backend")
    allowed = backend.conditions["allowed_actions"]
    assert "git_read" in allowed
    assert "git.read" not in allowed
    assert "k8s_apply_*" in backend.conditions["denied_patterns"]


def test_load_policies_maps_pii_abac_rule() -> None:
    rules = load_policies(SHIPPED_POLICIES)
    pii_rules = [
        rule
        for rule in rules
        if rule.effect == "deny" and rule.conditions.get("data_category") == "PII"
    ]
    assert len(pii_rules) >= 1


def test_p0_2_adapter_verify_gate(backend_identity: AgentIdentity) -> None:
    """Verify gate: production YAML governs PolicyEngine (not empty rules)."""
    rules = load_policies(SHIPPED_POLICIES)
    engine = PolicyEngine(rules=rules)

    allow = engine.evaluate(backend_identity, "git_read", {}, "rust-gateway")
    assert allow.allowed is True

    deny = engine.evaluate(backend_identity, "k8s_apply_prod", {}, "rust-gateway")
    assert deny.allowed is False


def test_fixture_engine_matches_existing_policy_tests(backend_identity: AgentIdentity) -> None:
    """Fixture pass-through rules still drive same backend RBAC behavior."""
    rules = load_policies(FIXTURE_POLICIES)
    engine = PolicyEngine(rules=rules)

    assert engine.evaluate(backend_identity, "git_read", {}, "rust-gateway").allowed is True
    assert engine.evaluate(backend_identity, "k8s_apply_prod", {}, "rust-gateway").allowed is False


def test_load_policies_empty_yaml_raises(tmp_path: Path) -> None:
    empty_policies = tmp_path / "policies.yml"
    empty_policies.write_text("version: 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no policy rules"):
        load_policies(empty_policies)
