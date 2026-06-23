"""Sense — Milestone C: ingest telemetry and environment signals."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_control_plane.core.models import TelemetryEvent


class SenseAdapter:
    """SAPAL Sense stage — collect signals from telemetry and config."""

    def __init__(self, config: dict) -> None:
        self._config = config

    def collect(self, events: list[TelemetryEvent]) -> dict:
        """Collect sense inputs from telemetry events."""
        raise NotImplementedError("Milestone C")
