"""Unit tests for core/registry.py ActionRegistry (Issue #22)."""

from __future__ import annotations

from ai_control_plane.core.models import (
    Guardrail,
    GuardrailTarget,
    PolicyRule,
    RbacConfig,
    RbacRolePolicy,
)
from ai_control_plane.core.registry import ActionRegistry


def _sample_rbac() -> RbacConfig:
    return RbacConfig(
        roles={
            "backend": RbacRolePolicy(
                allowed_actions=["git_read", "create_pr"],
                denied_actions=["k8s_apply_prod"],
            ),
            "reviewer": RbacRolePolicy(
                allowed_actions=["git_read", "comment.post"],
                denied_actions=["git.commit"],
            ),
        },
    )


def test_register_and_is_known() -> None:
    registry = ActionRegistry()
    registry.register("git_read")
    assert registry.is_known("git_read") is True
    assert registry.validate("git_read") is True
    assert registry.is_known("unknown_tool") is False


def test_register_many_and_list_actions_sorted() -> None:
    registry = ActionRegistry(["z_action", "a_action"])
    registry.register_many(["m_action", "a_action"])
    assert registry.list_actions() == ["a_action", "m_action", "z_action"]


def test_to_registered_maps_names() -> None:
    registry = ActionRegistry(["git_read", "create_pr"])
    registered = registry.to_registered()
    assert {item.name for item in registered} == {"git_read", "create_pr"}


def test_from_rbac_collects_role_actions() -> None:
    registry = ActionRegistry.from_rbac(_sample_rbac())
    actions = registry.actions
    assert "git_read" in actions
    assert "create_pr" in actions
    assert "k8s_apply_prod" in actions
    assert "comment.post" in actions


def test_from_policies_includes_abac_and_guardrails() -> None:
    rbac = _sample_rbac()
    abac = [
        PolicyRule(
            name="prod-k8s",
            description="",
            conditions={"actions": ["k8s_apply_stage"], "environment": "stage"},
            effect="allow",
        ),
    ]
    guardrails = [
        Guardrail(
            id="pii-block",
            description="",
            applies_to=GuardrailTarget(roles=["backend"], actions=["read_pii"]),
        ),
    ]
    registry = ActionRegistry.from_policies(rbac, abac, guardrails)
    assert registry.is_known("k8s_apply_stage")
    assert registry.is_known("read_pii")


def test_from_action_map_keys() -> None:
    from ai_control_plane.core.models import RegisteredAction

    registry = ActionRegistry.from_action_map(
        {
            "git_read": RegisteredAction(name="git_read"),
            "create_pr": RegisteredAction(name="create_pr"),
        },
    )
    assert registry.validate("create_pr") is True
