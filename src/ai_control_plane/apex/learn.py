"""Learn — Milestone C: policy adaptation from execution history."""

from __future__ import annotations

from typing import Any

from ai_control_plane.core.models import TelemetryEvent


class LearnAdapter:
    """Closes SAPAL loop — adapts policies from execution history."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._events_reviewed = 0

    def ingest(self, events: list[TelemetryEvent]) -> None:
        """Replay telemetry events for learning."""
        self._events_reviewed = len(events)

    def propose_policy_update(self) -> dict[str, Any]:
        """Propose policy updates from ingested history."""
        return {
            "proposals": [],
            "events_reviewed": self._events_reviewed,
            "note": "human approval required before any YAML change",
        }

    def apply_adaptation(self, proposal: dict[str, Any], approved: bool) -> dict[str, Any]:
        """Apply an approved policy adaptation proposal."""
        if not approved:
            return {"applied": False, "reason": "not approved"}
        return {"applied": True, "proposal": proposal}
