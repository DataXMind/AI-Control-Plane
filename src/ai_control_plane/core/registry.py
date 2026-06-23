"""Canonical action registry for policy evaluation and MCP tool binding."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from ai_control_plane.core.models import (
    Guardrail,
    PolicyRule,
    RbacConfig,
    RegisteredAction,
)


class ActionRegistry:
    """In-memory registry of known action names.

  Milestone B may add a Redis-backed implementation; this class is the
  default in-process registry used at policy evaluation time.
  """

    def __init__(self, actions: Iterable[str] | None = None) -> None:
        self._actions: set[str] = set(actions) if actions is not None else set()

    @property
    def actions(self) -> frozenset[str]:
        return frozenset(self._actions)

    def register(self, action: str) -> None:
        self._actions.add(action)

    def register_many(self, actions: Iterable[str]) -> None:
        self._actions.update(actions)

    def is_known(self, action: str) -> bool:
        return action in self._actions

    def validate(self, action: str) -> bool:
        """Return True when *action* is a registered canonical name."""
        return self.is_known(action)

    def list_actions(self) -> list[str]:
        return sorted(self._actions)

    def to_registered(self) -> list[RegisteredAction]:
        return [RegisteredAction(name=name) for name in self.list_actions()]

    @classmethod
    def from_rbac(cls, rbac: RbacConfig) -> ActionRegistry:
        actions: set[str] = set()
        for role in rbac.roles.values():
            actions.update(role.allowed_actions)
            actions.update(role.denied_actions)
        return cls(actions)

    @classmethod
    def from_policies(
        cls,
        rbac: RbacConfig,
        abac_rules: Iterable[PolicyRule],
        guardrails: Iterable[Guardrail],
    ) -> ActionRegistry:
        registry = cls.from_rbac(rbac)
        for rule in abac_rules:
            actions = rule.conditions.get("actions", [])
            if isinstance(actions, list):
                registry.register_many(str(action) for action in actions)
        for guardrail in guardrails:
            registry.register_many(guardrail.applies_to.actions)
        return registry

    @classmethod
    def from_action_map(cls, actions: Mapping[str, RegisteredAction]) -> ActionRegistry:
        return cls(actions.keys())
