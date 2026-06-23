"""Unit tests for core/quota.py QuotaStore and trackers (Issue #24)."""

from __future__ import annotations

import pytest

from ai_control_plane.core.quota import (
    InMemoryQuotaStore,
    QuotaTracker,
    RateLimiter,
    RedisQuotaStore,
    TokenBudget,
)


def test_in_memory_quota_store_get_set_increment_reset() -> None:
    store = InMemoryQuotaStore()
    assert store.get("missing") == 0.0
    store.set("k", 10.0)
    assert store.get("k") == 10.0
    assert store.increment("k", 5.0) == 15.0
    store.reset("k")
    assert store.get("k") == 0.0


def test_quota_tracker_consume_within_limit() -> None:
    store = InMemoryQuotaStore()
    tracker = QuotaTracker(store, daily_limits={"agent2": 100.0})
    assert tracker.consume("agent2", 40) is True
    assert tracker.consume("agent2", 50) is True
    assert tracker.remaining("agent2") == 10.0


def test_quota_tracker_consume_exceeds_limit() -> None:
    store = InMemoryQuotaStore()
    tracker = QuotaTracker(store, daily_limits={"agent2": 100.0})
    assert tracker.consume("agent2", 90) is True
    assert tracker.consume("agent2", 20) is False
    assert tracker.remaining("agent2") == 10.0


def test_quota_tracker_unlimited_agent() -> None:
    store = InMemoryQuotaStore()
    tracker = QuotaTracker(store, daily_limits={})
    assert tracker.consume("agent9", 1_000_000) is True
    assert tracker.remaining("agent9") == float("inf")


def test_quota_tracker_rejects_negative_tokens() -> None:
    store = InMemoryQuotaStore()
    tracker = QuotaTracker(store, daily_limits={"agent2": 100.0})
    with pytest.raises(ValueError, match="non-negative"):
        tracker.consume("agent2", -1)


def test_token_budget_deduct_and_remaining() -> None:
    store = InMemoryQuotaStore()
    budget = TokenBudget(store, project_limits={"rust-gateway": 1_000.0})
    assert budget.deduct("rust-gateway", 400) is True
    assert budget.remaining("rust-gateway") == 600.0
    assert budget.deduct("rust-gateway", 700) is False


def test_rate_limiter_allows_within_capacity() -> None:
    limiter = RateLimiter(capacity=5.0, refill_rate=1.0)
    assert limiter.check("client-a", cost=1.0) is True
    assert limiter.check("client-a", cost=4.0) is True
    assert limiter.check("client-a", cost=1.0) is False


def test_rate_limiter_rejects_invalid_capacity() -> None:
    with pytest.raises(ValueError, match="capacity"):
        RateLimiter(capacity=0.0, refill_rate=1.0)


def test_redis_quota_store_roundtrip(monkeypatch: pytest.MonkeyPatch) -> None:
    import sys
    from types import ModuleType
    from unittest.mock import MagicMock

    fake_client = MagicMock()
    fake_client.get.return_value = "15.0"
    fake_client.incrbyfloat.return_value = 25.0
    module = ModuleType("redis")
    redis_cls = MagicMock()
    redis_cls.from_url.return_value = fake_client
    module.Redis = redis_cls
    monkeypatch.setitem(sys.modules, "redis", module)

    store = RedisQuotaStore("redis://localhost:6379/0")
    assert store.get("quota:test") == 15.0
    assert store.increment("quota:test", 10.0) == 25.0
    store.reset("quota:test")
    fake_client.delete.assert_called_with("quota:test")
