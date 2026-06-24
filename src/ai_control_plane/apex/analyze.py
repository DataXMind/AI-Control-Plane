"""Analyze — Milestone C: interpret signals and detect patterns."""

from __future__ import annotations

from typing import Any


class AnalyzeAdapter:
    """SAPAL Analyze stage — pattern detection over sense output."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def analyze(self, sense_output: dict[str, Any]) -> dict[str, Any]:
        """Analyze collected signals."""
        threshold = int(self._config.get("anomaly_event_threshold", 50))
        event_count = int(sense_output.get("event_count", 0))
        return {
            "anomaly_detected": event_count > threshold,
            "event_count": event_count,
            "threshold": threshold,
        }
