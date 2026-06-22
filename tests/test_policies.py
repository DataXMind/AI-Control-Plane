"""PolicyEngine unit tests — RBAC, ABAC, fail-closed behavior."""

from __future__ import annotations

from ai_control_plane.core.models import AgentIdentity
from ai_control_plane.core.policies import PolicyEngine

from .conftest import evaluate_tool


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
    deny = evaluate_tool(mock_policy_engine, reviewer_identity, "write_repo")
    assert deny.allowed is False

    allow = evaluate_tool(mock_policy_engine, reviewer_identity, "read_repo")
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
        (reviewer_identity, "read_repo"),
    ]
    for identity, tool_name in cases:
        decision = evaluate_tool(
            mock_policy_engine,
            identity,
            tool_name,
            {"data_category": "PII"},
        )
        assert decision.allowed is False
        assert decision.policy_id == "deny-pii"
