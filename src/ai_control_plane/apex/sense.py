"""Sense — Milestone C: ingest telemetry and environment signals."""

from __future__ import annotations

from typing import Any

from ai_control_plane.core.models import TelemetryEvent


class SenseAdapter:
    """SAPAL Sense stage — collect signals from telemetry and config."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def collect(self, events: list[TelemetryEvent]) -> dict[str, Any]:
        """Collect sense inputs from telemetry events."""
        by_event_type: dict[str, int] = {}
        by_project: dict[str, int] = {}
        for event in events:
            by_event_type[event.event_type] = by_event_type.get(event.event_type, 0) + 1
            by_project[event.project_id] = by_project.get(event.project_id, 0) + 1
        return {
            "event_count": len(events),
            "by_event_type": by_event_type,
            "by_project": by_project,
            "chain_valid": True,
        }
