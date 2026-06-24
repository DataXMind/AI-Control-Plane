"""Canonical action registry for policy evaluation and MCP tool binding."""

from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Protocol, runtime_checkable

from ai_control_plane.core.models import (
    Guardrail,
    PolicyRule,
    RbacConfig,
    RegisteredAction,
)


@runtime_checkable
class ActionRegistryLike(Protocol):
    """Storage contract — swap in-memory for Redis in Milestone B (#33)."""

    @property
    def actions(self) -> frozenset[str]:
        ...

    def register(self, action: str) -> None:
        ...

    def register_many(self, actions: Iterable[str]) -> None:
        ...

    def is_known(self, action: str) -> bool:
        ...

    def validate(self, action: str) -> bool:
        ...

    def list_actions(self) -> list[str]:
        ...

    def to_registered(self) -> list[RegisteredAction]:
        ...


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


_REDIS_REGISTRY_KEY = "registry:actions"


class RedisActionRegistry:
    """Redis SET-backed registry — activated when ``ACP_REDIS_URL`` is set (#33)."""

    def __init__(self, url: str, actions: Iterable[str] | None = None) -> None:
        try:
            import redis  # type: ignore[import-not-found]
        except ImportError as exc:
            msg = "redis package required (pip install ai-control-plane[redis])"
            raise RuntimeError(msg) from exc
        self._client = redis.Redis.from_url(url, decode_responses=True)
        if actions is not None:
            self.register_many(actions)

    @property
    def actions(self) -> frozenset[str]:
        members = self._client.smembers(_REDIS_REGISTRY_KEY)
        return frozenset(str(member) for member in members)

    def register(self, action: str) -> None:
        self._client.sadd(_REDIS_REGISTRY_KEY, action)

    def register_many(self, actions: Iterable[str]) -> None:
        batch = list(actions)
        if batch:
            self._client.sadd(_REDIS_REGISTRY_KEY, *batch)

    def is_known(self, action: str) -> bool:
        return bool(self._client.sismember(_REDIS_REGISTRY_KEY, action))

    def validate(self, action: str) -> bool:
        return self.is_known(action)

    def list_actions(self) -> list[str]:
        return sorted(self.actions)

    def to_registered(self) -> list[RegisteredAction]:
        return [RegisteredAction(name=name) for name in self.list_actions()]

    @classmethod
    def from_rbac(cls, url: str, rbac: RbacConfig) -> RedisActionRegistry:
        seed = ActionRegistry.from_rbac(rbac)
        return cls(url, seed.actions)

    @classmethod
    def from_policies(
        cls,
        url: str,
        rbac: RbacConfig,
        abac_rules: Iterable[PolicyRule],
        guardrails: Iterable[Guardrail],
    ) -> RedisActionRegistry:
        seed = ActionRegistry.from_policies(rbac, abac_rules, guardrails)
        return cls(url, seed.actions)


def create_action_registry(actions: Iterable[str] | None = None) -> ActionRegistryLike:
    """Redis registry when ``ACP_REDIS_URL`` set; else in-memory."""
    redis_url = os.environ.get("ACP_REDIS_URL")
    if redis_url:
        return RedisActionRegistry(redis_url, actions)
    return ActionRegistry(actions)


def seed_registry_from_rules(registry: ActionRegistryLike, rules: Iterable[PolicyRule]) -> None:
    """Register action names referenced in loaded policy rules."""
    for rule in rules:
        actions = rule.conditions.get("actions")
        if isinstance(actions, list):
            registry.register_many(str(action) for action in actions)


__all__ = [
    "ActionRegistry",
    "ActionRegistryLike",
    "RedisActionRegistry",
    "create_action_registry",
    "seed_registry_from_rules",
]
