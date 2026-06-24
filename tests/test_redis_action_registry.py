"""Redis ActionRegistry and factory wiring tests (#33)."""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock

import pytest

from ai_control_plane.core.registry import (
    ActionRegistry,
    RedisActionRegistry,
    create_action_registry,
)


def _fake_redis_module(client: MagicMock) -> ModuleType:
    module = ModuleType("redis")
    redis_cls = MagicMock()
    redis_cls.from_url.return_value = client
    module.Redis = redis_cls
    return module


def test_create_action_registry_defaults_in_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ACP_REDIS_URL", raising=False)
    registry = create_action_registry()
    assert isinstance(registry, ActionRegistry)


def test_create_action_registry_uses_redis_when_url_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ACP_REDIS_URL", "redis://localhost:6379/0")
    fake_client = MagicMock()
    fake_client.smembers.return_value = set()
    fake_client.sismember.return_value = False
    monkeypatch.setitem(sys.modules, "redis", _fake_redis_module(fake_client))
    registry = create_action_registry()
    assert isinstance(registry, RedisActionRegistry)
    registry.register("git_read")
    fake_client.sadd.assert_called_with("registry:actions", "git_read")


def test_redis_action_registry_is_known(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_client = MagicMock()
    fake_client.sismember.return_value = True
    fake_client.smembers.return_value = {"git_read"}
    monkeypatch.setitem(sys.modules, "redis", _fake_redis_module(fake_client))
    registry = RedisActionRegistry("redis://localhost:6379/0")
    assert registry.validate("git_read") is True
    assert registry.list_actions() == ["git_read"]
