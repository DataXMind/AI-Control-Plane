"""Analyze — Milestone C: interpret signals and detect patterns."""

from __future__ import annotations


class AnalyzeAdapter:
    """SAPAL Analyze stage — pattern detection over sense output."""

    def __init__(self, config: dict) -> None:
        self._config = config

    def analyze(self, sense_output: dict) -> dict:
        """Analyze collected signals."""
        raise NotImplementedError("Milestone C")
