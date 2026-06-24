"""File-backed telemetry store tests — MC-9."""

from __future__ import annotations

import os

from ai_control_plane.core.models import TelemetryEvent
from ai_control_plane.core.telemetry import FileTelemetryStore, create_telemetry_store


def _sample_event() -> TelemetryEvent:
    return TelemetryEvent(
        event_type="TOOL_CALL",
        agent_id="agent2",
        project_id="rust-gateway",
        payload={"tool": "git_status"},
    )


def test_file_telemetry_store_survives_new_instance(tmp_path) -> None:
    path = tmp_path / "telemetry" / "events.json"
    store1 = FileTelemetryStore(path)
    event = store1.append(_sample_event())

    store2 = FileTelemetryStore(path)
    loaded = store2.get(event.event_id)
    assert loaded is not None
    assert loaded.event_hash == event.event_hash
    assert store2.verify_chain() is True


def test_create_telemetry_store_uses_file_when_acp_data_dir_set(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ACP_DATA_DIR", str(tmp_path))
    store = create_telemetry_store()
    store.append(_sample_event())
    path = tmp_path / "telemetry" / "events.json"
    assert path.exists()
    assert os.environ["ACP_DATA_DIR"] == str(tmp_path)
