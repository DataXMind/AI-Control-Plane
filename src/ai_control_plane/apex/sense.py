"""Sense — Milestone C: ingest telemetry and environment signals."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_control_plane.core.models import TelemetryEvent


class SenseAdapter:
    """SAPAL Sense stage — collect signals from telemetry and config."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def collect(self, events: list[TelemetryEvent]) -> dict[str, Any]:
        """Collect sense inputs from telemetry events."""
        raise NotImplementedError("Milestone C")
