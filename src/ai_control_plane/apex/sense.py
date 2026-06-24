"""Sense — Milestone C+ : telemetry replay + Z-score / optional IsolationForest."""

from __future__ import annotations

import math
from typing import Any

from ai_control_plane.core.models import TelemetryEvent
from ai_control_plane.core.telemetry import TelemetryStore


def _numeric_payload_values(events: list[TelemetryEvent]) -> list[float]:
    values: list[float] = []
    for event in events:
        for key in ("tokens", "token_count", "n"):
            raw = event.payload.get(key)
            if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                values.append(float(raw))
    return values


def z_score_anomaly(values: list[float], *, threshold: float = 2.5) -> bool:
    """True when the latest value is an outlier vs series mean/std."""
    if len(values) < 2:
        return False
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    if variance == 0:
        return False
    std = math.sqrt(variance)
    latest = values[-1]
    return abs((latest - mean) / std) > threshold


def isolation_forest_anomaly(values: list[float]) -> bool | None:
    """Optional sklearn detector; None when [apex] extra not installed."""
    if len(values) < 3:
        return None
    try:
        from sklearn.ensemble import IsolationForest  # type: ignore[import-not-found]
    except ImportError:
        return None

    model = IsolationForest(contamination=0.1, random_state=0)
    samples = [[value] for value in values]
    model.fit(samples)
    prediction = model.predict([samples[-1]])
    return bool(prediction[0] == -1)


class SenseAdapter:
    """SAPAL Sense stage — collect signals from telemetry replay."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def collect_from_store(self, store: TelemetryStore) -> dict[str, Any]:
        """Collect sense inputs via ``TelemetryStore.replay()`` (C+-1/C+-2)."""
        events = store.replay()
        return self.collect(events)

    def collect(self, events: list[TelemetryEvent]) -> dict[str, Any]:
        """Collect sense inputs from telemetry events."""
        by_event_type: dict[str, int] = {}
        by_project: dict[str, int] = {}
        for event in events:
            by_event_type[event.event_type] = by_event_type.get(event.event_type, 0) + 1
            by_project[event.project_id] = by_project.get(event.project_id, 0) + 1

        numeric_values = _numeric_payload_values(events)
        z_threshold = float(self._config.get("sense_z_threshold", 2.5))
        z_anomaly = z_score_anomaly(numeric_values, threshold=z_threshold)
        iforest = isolation_forest_anomaly(numeric_values)

        return {
            "event_count": len(events),
            "by_event_type": by_event_type,
            "by_project": by_project,
            "numeric_sample_count": len(numeric_values),
            "z_score_anomaly": z_anomaly,
            "isolation_forest_anomaly": iforest,
            "chain_valid": True,
        }
