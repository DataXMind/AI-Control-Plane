"""PolicyEngine unit tests — RBAC, ABAC, fail-closed behavior."""

from __future__ import annotations

import pytest

from ai_control_plane.config.loader import load_policies
from ai_control_plane.core.models import AgentIdentity, PolicyRule
from ai_control_plane.core.policies import PolicyEngine

from .conftest import FIXTURES_DIR, evaluate_tool

FIXTURE_POLICIES = FIXTURES_DIR / "policies.yml"


@pytest.fixture
def abac_full_policy_engine() -> PolicyEngine:
    """PolicyEngine with Restrict-PII honoring role_not_in privileged roles."""
    rules = load_policies(FIXTURE_POLICIES)
    without_pii = [rule for rule in rules if rule.name != "Restrict-PII"]
    pii_rule = PolicyRule(
        name="Restrict-PII",
        description="Deny read/write on PII-tagged paths outside reviewer role",
        effect="deny",
        conditions={
            "rule_type": "abac",
            "data_category": "PII",
            "role_not_in": ["reviewer"],
            "actions": ["git_read", "git_commit"],
        },
    )
    return PolicyEngine(rules=without_pii + [pii_rule])


def test_backend_cannot_k8s_apply(
    mock_policy_engine: PolicyEngine,
    backend_identity: AgentIdentity,
) -> None:
    decision = evaluate_tool(mock_policy_engine, backend_identity, "k8s_apply_prod")

    assert decision.allowed is False
    assert decision.requires_approval is False


def test_reviewer_read_only(
    mock_policy_engine: PolicyEngine,
    reviewer_identity: AgentIdentity,
) -> None:
    deny = evaluate_tool(mock_policy_engine, reviewer_identity, "git_commit")
    assert deny.allowed is False

    allow = evaluate_tool(mock_policy_engine, reviewer_identity, "git_read")
    assert allow.allowed is True
    assert allow.requires_approval is False


def test_prod_k8s_requires_approval(
    mock_policy_engine: PolicyEngine,
    infra_identity: AgentIdentity,
) -> None:
    decision = evaluate_tool(
        mock_policy_engine,
        infra_identity,
        "k8s_apply_prod",
        {"environment": "prod"},
    )

    assert decision.allowed is True
    assert decision.requires_approval is True
    assert decision.policy_id == "prod-k8s-approval"


def test_backend_can_create_pr(
    mock_policy_engine: PolicyEngine,
    backend_identity: AgentIdentity,
) -> None:
    decision = evaluate_tool(mock_policy_engine, backend_identity, "create_pr")

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_deny_pii_access(
    mock_policy_engine: PolicyEngine,
    backend_identity: AgentIdentity,
    infra_identity: AgentIdentity,
    reviewer_identity: AgentIdentity,
) -> None:
    cases = [
        (backend_identity, "create_pr"),
        (infra_identity, "git_read"),
        (reviewer_identity, "git_read"),
    ]
    for identity, tool_name in cases:
        decision = evaluate_tool(
            mock_policy_engine,
            identity,
            tool_name,
            {"data_category": "PII"},
        )
        assert decision.allowed is False
        assert decision.policy_id == "Restrict-PII"


def test_pii_denies_non_privileged_role(
    abac_full_policy_engine: PolicyEngine,
    backend_identity: AgentIdentity,
    reviewer_identity: AgentIdentity,
) -> None:
    deny = evaluate_tool(
        abac_full_policy_engine,
        backend_identity,
        "git_read",
        {"data_category": "PII"},
    )
    assert deny.allowed is False
    assert deny.policy_id == "Restrict-PII"

    allow = evaluate_tool(
        abac_full_policy_engine,
        reviewer_identity,
        "git_read",
        {"data_category": "PII"},
    )
    assert allow.allowed is True


def test_reviewer_write_denied(
    mock_policy_engine: PolicyEngine,
    reviewer_identity: AgentIdentity,
) -> None:
    deny = evaluate_tool(mock_policy_engine, reviewer_identity, "write_repo")
    assert deny.allowed is False

    allow = evaluate_tool(mock_policy_engine, reviewer_identity, "git_read")
    assert allow.allowed is True


def test_approval_status_blocks_without_approval(
    mock_policy_engine: PolicyEngine,
    infra_identity: AgentIdentity,
) -> None:
    decision = evaluate_tool(
        mock_policy_engine,
        infra_identity,
        "k8s_apply",
        {"environment": "prod", "approval_status": "not_approved"},
    )
    assert decision.allowed is False
    assert decision.policy_id == "Deny-prod-k8s-unapproved"
    assert decision.evaluation_path == "abac"


def test_evaluation_path_layers(
    mock_policy_engine: PolicyEngine,
    backend_identity: AgentIdentity,
) -> None:
    allow = evaluate_tool(mock_policy_engine, backend_identity, "git_read")
    assert allow.evaluation_path == "default_allow"

    deny = evaluate_tool(mock_policy_engine, backend_identity, "k8s_apply_prod")
    assert deny.evaluation_path == "rbac"
