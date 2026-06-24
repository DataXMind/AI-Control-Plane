"""Act — Milestone C+ : proposal-only execution path (ADR-5 Option C)."""

from __future__ import annotations

from typing import Any


class ActAdapter:
    """SAPAL Act stage — emits proposals; policy eval via TS/MCP bridge."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def execute(self, prediction: dict[str, Any]) -> dict[str, Any]:
        """Return action proposals without side effects (C+-5)."""
        action = str(prediction.get("recommended_action", "continue"))
        tool_name = "git_read" if action == "review" else "git_status"
        return {
            "executed": False,
            "status": "proposal_only",
            "policy_eval_required": True,
            "proposals": [
                {
                    "tool_name": tool_name,
                    "args": {"reason": f"sapal_{action}"},
                    "policy_eval_required": True,
                },
            ],
            "action": action,
        }
