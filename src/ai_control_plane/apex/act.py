"""Act — Milestone C: execute approved actions from predictions."""

from __future__ import annotations

from typing import Any


class ActAdapter:
    """SAPAL Act stage — orchestrate approved tool/agent actions."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def execute(self, prediction: dict[str, Any]) -> dict[str, Any]:
        """Execute an action plan derived from prediction (fail-closed on high risk)."""
        high_risk = prediction.get("risk_level") == "high"
        return {
            "executed": not high_risk,
            "action": prediction.get("recommended_action"),
            "status": "skipped_high_risk" if high_risk else "ok",
        }
