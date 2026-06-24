"""Milestone C — APEX / SAPAL loop over telemetry."""

from __future__ import annotations

from typing import Any

from ai_control_plane.apex.loop import SapalLoop
from ai_control_plane.core.telemetry import TelemetryStore, create_telemetry_store


def run_sapal_pipeline(
    telemetry_store: TelemetryStore | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the APEX SAPAL loop (Sense → Analyze → Predict → Act → Learn)."""
    store = telemetry_store or create_telemetry_store()
    return SapalLoop(config or {}, store).run()
