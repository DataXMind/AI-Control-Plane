"""Redis quota store and factory wiring tests."""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock

import pytest

from ai_control_plane.core.quota import InMemoryQuotaStore, RedisQuotaStore, create_quota_store


def _fake_redis_module(client: MagicMock) -> ModuleType:
    module = ModuleType("redis")
    redis_cls = MagicMock()
    redis_cls.from_url.return_value = client
    module.Redis = redis_cls
    return module


def test_create_quota_store_defaults_in_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ACP_REDIS_URL", raising=False)
    store = create_quota_store()
    assert isinstance(store, InMemoryQuotaStore)


def test_create_quota_store_uses_redis_when_url_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ACP_REDIS_URL", "redis://localhost:6379/0")
    fake_client = MagicMock()
    fake_client.get.return_value = None
    fake_redis = _fake_redis_module(fake_client)
    monkeypatch.setitem(sys.modules, "redis", fake_redis)
    store = create_quota_store()
    assert isinstance(store, RedisQuotaStore)
    assert store.get("quota:test") == 0.0


def test_redis_quota_store_increment(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_client = MagicMock()
    fake_client.incrbyfloat.return_value = 42.0
    fake_redis = _fake_redis_module(fake_client)
    monkeypatch.setitem(sys.modules, "redis", fake_redis)
    store = RedisQuotaStore("redis://localhost:6379/0")
    assert store.increment("quota:agent:agent2:daily_tokens", 10.0) == 42.0
