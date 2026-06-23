"""Analyze — Milestone C: interpret signals and detect patterns."""

from __future__ import annotations

from typing import Any


class AnalyzeAdapter:
    """SAPAL Analyze stage — pattern detection over sense output."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def analyze(self, sense_output: dict[str, Any]) -> dict[str, Any]:
        """Analyze collected signals."""
        raise NotImplementedError("Milestone C")
