"""Quota tracking with swappable storage backend — no hardcoded Redis."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class QuotaStore(Protocol):
    """Storage contract — swap InMemoryQuotaStore for RedisQuotaStore in Milestone B."""

    def get(self, key: str) -> float:
        """Return the current value for *key* (0.0 when unset)."""
        ...

    def set(self, key: str, value: float) -> None:
        """Persist *value* for *key*."""
        ...

    def increment(self, key: str, delta: float) -> float:
        """Atomically add *delta* and return the new value."""
        ...

    def reset(self, key: str) -> None:
        """Clear usage for *key*."""
        ...


class InMemoryQuotaStore:
    """Thread-safe in-memory store — Milestone A default; data lost on restart."""

    def __init__(self) -> None:
        self._data: dict[str, float] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> float:
        with self._lock:
            return self._data.get(key, 0.0)

    def set(self, key: str, value: float) -> None:
        with self._lock:
            self._data[key] = value

    def increment(self, key: str, delta: float) -> float:
        with self._lock:
            new_value = self._data.get(key, 0.0) + delta
            self._data[key] = new_value
            return new_value

    def reset(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)


class RedisQuotaStore:
    """Redis-backed store — Milestone B placeholder."""

    def get(self, key: str) -> float:
        raise NotImplementedError("RedisQuotaStore is planned for Milestone B")

    def set(self, key: str, value: float) -> None:
        raise NotImplementedError("RedisQuotaStore is planned for Milestone B")

    def increment(self, key: str, delta: float) -> float:
        raise NotImplementedError("RedisQuotaStore is planned for Milestone B")

    def reset(self, key: str) -> None:
        raise NotImplementedError("RedisQuotaStore is planned for Milestone B")


def _agent_usage_key(agent_id: str) -> str:
    return f"quota:agent:{agent_id}:daily_tokens"


def _project_usage_key(project_id: str) -> str:
    return f"quota:project:{project_id}:tokens"


class QuotaTracker:
    """Agent-level daily token quota backed by a QuotaStore."""

    def __init__(self, store: QuotaStore, daily_limits: dict[str, float]) -> None:
        self._store = store
        self._daily_limits = daily_limits

    def consume(self, agent_id: str, tokens: int) -> bool:
        """Record token usage; return False when the daily limit would be exceeded."""
        if tokens < 0:
            msg = "tokens must be non-negative"
            raise ValueError(msg)

        limit = self._daily_limits.get(agent_id)
        if limit is None:
            self._store.increment(_agent_usage_key(agent_id), float(tokens))
            return True

        key = _agent_usage_key(agent_id)
        used = self._store.get(key)
        if used + tokens > limit:
            return False

        self._store.increment(key, float(tokens))
        return True

    def remaining(self, agent_id: str) -> float:
        """Return unused daily token budget for *agent_id*."""
        limit = self._daily_limits.get(agent_id)
        if limit is None:
            return float("inf")

        used = self._store.get(_agent_usage_key(agent_id))
        return max(0.0, limit - used)

    def reset_daily(self, agent_id: str) -> None:
        """Reset daily usage counters for *agent_id*."""
        self._store.reset(_agent_usage_key(agent_id))


class TokenBudget:
    """Project-level token budget backed by a QuotaStore."""

    def __init__(self, store: QuotaStore, project_limits: dict[str, float]) -> None:
        self._store = store
        self._project_limits = project_limits

    def deduct(self, project_id: str, tokens: int) -> bool:
        """Deduct tokens from the project budget; return False when over budget."""
        if tokens < 0:
            msg = "tokens must be non-negative"
            raise ValueError(msg)

        limit = self._project_limits.get(project_id)
        if limit is None:
            self._store.increment(_project_usage_key(project_id), float(tokens))
            return True

        key = _project_usage_key(project_id)
        used = self._store.get(key)
        if used + tokens > limit:
            return False

        self._store.increment(key, float(tokens))
        return True

    def remaining(self, project_id: str) -> float:
        """Return unused token budget for *project_id*."""
        limit = self._project_limits.get(project_id)
        if limit is None:
            return float("inf")

        used = self._store.get(_project_usage_key(project_id))
        return max(0.0, limit - used)


@dataclass
class _TokenBucket:
    tokens: float
    last_refill: float


class RateLimiter:
    """Token-bucket rate limiter — capacity and refill_rate injected at construction."""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        if capacity <= 0:
            msg = "capacity must be positive"
            raise ValueError(msg)
        if refill_rate <= 0:
            msg = "refill_rate must be positive"
            raise ValueError(msg)

        self._capacity = capacity
        self._refill_rate = refill_rate
        self._buckets: dict[str, _TokenBucket] = {}
        self._lock = threading.Lock()

    def check(self, client_id: str, cost: float = 1.0) -> bool:
        """Consume *cost* tokens when available; return False when rate-limited."""
        if cost < 0:
            msg = "cost must be non-negative"
            raise ValueError(msg)

        with self._lock:
            now = time.monotonic()
            bucket = self._buckets.get(client_id)
            if bucket is None:
                bucket = _TokenBucket(tokens=self._capacity, last_refill=now)
                self._buckets[client_id] = bucket

            elapsed = now - bucket.last_refill
            bucket.tokens = min(self._capacity, bucket.tokens + elapsed * self._refill_rate)
            bucket.last_refill = now

            if bucket.tokens < cost:
                return False

            bucket.tokens -= cost
            return True


__all__ = [
    "InMemoryQuotaStore",
    "QuotaStore",
    "QuotaTracker",
    "RateLimiter",
    "RedisQuotaStore",
    "TokenBudget",
]
