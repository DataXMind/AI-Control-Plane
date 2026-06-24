"""Append-only telemetry store with hash-chained audit events."""

from __future__ import annotations

import hashlib
import json
import os
import threading
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from ai_control_plane.core.models import TelemetryEvent


def compute_event_hash(previous_hash: str | None, event: TelemetryEvent) -> str:
    """Compute SHA-256 hash for *event* chained to *previous_hash*."""
    payload = event.model_dump(
        mode="json",
        exclude={"event_hash", "previous_hash", "id"},
    )
    material = json.dumps(
        {"previous_hash": previous_hash, "event": payload},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def seal_event(previous_hash: str | None, event: TelemetryEvent) -> TelemetryEvent:
    """Attach chain metadata and content hash to *event*."""
    event_hash = compute_event_hash(previous_hash, event)
    return event.model_copy(
        update={"previous_hash": previous_hash, "event_hash": event_hash},
    )


def verify_event_chain(events: Sequence[TelemetryEvent]) -> bool:
    """Verify hash-chain integrity for an ordered event sequence."""
    previous_hash: str | None = None
    for event in events:
        if event.previous_hash != previous_hash:
            return False
        expected = compute_event_hash(previous_hash, event)
        if event.event_hash != expected:
            return False
        previous_hash = event.event_hash
    return True


class TelemetryStore(ABC):
    """Abstract append-only telemetry persistence."""

    @abstractmethod
    def append(self, event: TelemetryEvent) -> TelemetryEvent:
        """Seal and persist *event*, returning the stored record."""

    @abstractmethod
    def get(self, event_id: str) -> TelemetryEvent | None:
        """Return a single event by ID, or None if not found."""

    @abstractmethod
    def list_events(self) -> list[TelemetryEvent]:
        """Return all events in append order."""

    @abstractmethod
    def verify_chain(self) -> bool:
        """Return True when the stored event chain is intact."""


class InMemoryTelemetryStore(TelemetryStore):
    """Process-local append-only store for PoC and unit tests."""

    def __init__(self) -> None:
        self._events: list[TelemetryEvent] = []
        self._index: dict[str, TelemetryEvent] = {}
        self._lock = threading.Lock()

    def append(self, event: TelemetryEvent) -> TelemetryEvent:
        with self._lock:
            previous_hash = self._events[-1].event_hash if self._events else None
            sealed = seal_event(previous_hash, event)
            self._events.append(sealed)
            self._index[sealed.event_id] = sealed
            return sealed.model_copy(deep=True)

    def get(self, event_id: str) -> TelemetryEvent | None:
        with self._lock:
            stored = self._index.get(event_id)
            if stored is None:
                return None
            return stored.model_copy(deep=True)

    def list_events(self) -> list[TelemetryEvent]:
        with self._lock:
            return [event.model_copy(deep=True) for event in self._events]

    def verify_chain(self) -> bool:
        with self._lock:
            return verify_event_chain(self._events)


class FileTelemetryStore(TelemetryStore):
    """JSON file-backed store under ``ACP_DATA_DIR/telemetry/events.json`` (#MC-9)."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        if not self._path.exists():
            self._path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[TelemetryEvent]:
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [TelemetryEvent.model_validate(item) for item in raw]

    def _save(self, events: list[TelemetryEvent]) -> None:
        payload = [event.model_dump(mode="json") for event in events]
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def append(self, event: TelemetryEvent) -> TelemetryEvent:
        with self._lock:
            events = self._load()
            previous_hash = events[-1].event_hash if events else None
            sealed = seal_event(previous_hash, event)
            events.append(sealed)
            self._save(events)
            return sealed.model_copy(deep=True)

    def get(self, event_id: str) -> TelemetryEvent | None:
        with self._lock:
            for event in self._load():
                if event.event_id == event_id:
                    return event.model_copy(deep=True)
            return None

    def list_events(self) -> list[TelemetryEvent]:
        with self._lock:
            return [event.model_copy(deep=True) for event in self._load()]

    def verify_chain(self) -> bool:
        with self._lock:
            return verify_event_chain(self._load())


def create_telemetry_store() -> TelemetryStore:
    """File store when ``ACP_DATA_DIR`` set; else in-memory."""
    data_dir = os.environ.get("ACP_DATA_DIR")
    if data_dir:
        return FileTelemetryStore(Path(data_dir) / "telemetry" / "events.json")
    return InMemoryTelemetryStore()


class TelemetryWriter:
    """Convenience wrapper for emitting sealed telemetry events."""

    def __init__(self, store: TelemetryStore) -> None:
        self._store = store

    @property
    def store(self) -> TelemetryStore:
        return self._store

    def emit(self, event: TelemetryEvent) -> TelemetryEvent:
        return self._store.append(event)
