"""Telemetry hash-chain tests — Issue #23 / Tab 7."""

from __future__ import annotations

import pytest

from ai_control_plane.core.exceptions import ControlPlaneError
from ai_control_plane.core.models import TelemetryEvent
from ai_control_plane.core.telemetry import (
    InMemoryTelemetryStore,
    TelemetryWriter,
    compute_event_hash,
    filter_telemetry_events,
    seal_event,
    verify_event_chain,
)

EVENT_TOOL_CALL = "TOOL_CALL"
EVENT_POLICY = "POLICY_DECISION"


def _sample_event(**overrides: object) -> TelemetryEvent:
    base = {
        "event_type": EVENT_TOOL_CALL,
        "agent_id": "agent2",
        "project_id": "rust-gateway",
        "payload": {"tool_name": "git_read"},
    }
    base.update(overrides)
    return TelemetryEvent(**base)  # type: ignore[arg-type]


def test_compute_event_hash_deterministic() -> None:
    event = _sample_event()
    assert compute_event_hash("", event) == compute_event_hash("", event)


def test_seal_event_sets_hash_and_previous() -> None:
    sealed = seal_event("abc", _sample_event())
    assert sealed.previous_hash == "abc"
    assert len(sealed.event_hash) == 64


def test_verify_chain_passes_for_valid_sequence() -> None:
    store = InMemoryTelemetryStore()
    for index in range(3):
        store.append(_sample_event(payload={"index": index}))
    assert store.verify_chain() is True


def test_verify_chain_fails_if_tampered() -> None:
    store = InMemoryTelemetryStore()
    store.append(_sample_event(payload={"n": 1}))
    store.append(_sample_event(payload={"n": 2}))
    store.append(_sample_event(payload={"n": 3}))
    events = store.list_events()
    tampered = list(events)
    tampered[1] = tampered[1].model_copy(update={"event_hash": "tampered"})
    assert verify_event_chain(tampered) is False
    assert store.verify_chain() is True


def test_store_append_links_chain() -> None:
    store = InMemoryTelemetryStore()
    e1 = store.append(_sample_event(event_type=EVENT_TOOL_CALL))
    e2 = store.append(_sample_event(event_type=EVENT_POLICY))
    assert e2.previous_hash == e1.event_hash
    assert store.verify_chain() is True


def test_store_get_returns_sealed_copy() -> None:
    store = InMemoryTelemetryStore()
    event = store.append(_sample_event())
    retrieved = store.get(event.event_id)
    assert retrieved is not None
    assert retrieved.event_hash != ""


def test_writer_emits_sealed_and_chained() -> None:
    store = InMemoryTelemetryStore()
    writer = TelemetryWriter(store)
    r1 = writer.emit(
        TelemetryEvent(
            event_type="tool.call",
            agent_id="a",
            project_id="p",
            payload={},
        ),
    )
    r2 = writer.emit(
        TelemetryEvent(
            event_type="tool.call",
            agent_id="a",
            project_id="p",
            payload={"n": 2},
        ),
    )
    assert r1.event_hash != r2.event_hash
    assert r2.previous_hash == r1.event_hash
    assert store.verify_chain() is True


def test_replay_filters_by_event_type() -> None:
    store = InMemoryTelemetryStore()
    store.append(_sample_event(event_type=EVENT_TOOL_CALL))
    store.append(_sample_event(event_type=EVENT_POLICY))
    replayed = store.replay(event_type=EVENT_TOOL_CALL)
    assert len(replayed) == 1
    assert replayed[0].event_type == EVENT_TOOL_CALL


def test_replay_fail_closed_on_broken_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryTelemetryStore()
    store.append(_sample_event())
    monkeypatch.setattr(store, "verify_chain", lambda: False)
    with pytest.raises(ControlPlaneError, match="telemetry chain integrity failed"):
        store.replay()


def test_filter_telemetry_events_by_project() -> None:
    events = [
        _sample_event(project_id="p1"),
        _sample_event(project_id="p2"),
    ]
    filtered = filter_telemetry_events(events, project_id="p1")
    assert len(filtered) == 1
    assert filtered[0].project_id == "p1"
