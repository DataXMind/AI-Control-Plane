"""Predict — Milestone C+ : token burn forecast (Darts optional + rolling fallback)."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from ai_control_plane.core.models import TelemetryEvent


def _hourly_token_counts(events: list[TelemetryEvent]) -> list[float]:
    """Aggregate token-like payload fields per UTC hour."""
    buckets: dict[datetime, float] = defaultdict(float)
    for event in events:
        if event.event_type != "TOOL_CALL":
            continue
        tokens_raw = event.payload.get("tokens", event.payload.get("token_count", 0))
        if not isinstance(tokens_raw, (int, float)) or isinstance(tokens_raw, bool):
            continue
        hour = event.timestamp.astimezone(UTC).replace(minute=0, second=0, microsecond=0)
        buckets[hour] += float(tokens_raw)
    if not buckets:
        return []
    ordered_hours = sorted(buckets.keys())
    return [buckets[hour] for hour in ordered_hours]


def _rolling_mean_forecast(series: list[float], *, window: int = 3) -> float:
    if not series:
        return 0.0
    tail = series[-window:]
    return sum(tail) / len(tail)


def _darts_forecast(series: list[float], *, horizon: int = 1) -> float | None:
    if len(series) < 24:
        return None
    try:
        from darts import TimeSeries  # type: ignore[import-not-found]
        from darts.models import ExponentialSmoothing  # type: ignore[import-not-found]
    except ImportError:
        return None

    ts = TimeSeries.from_values(series)
    model = ExponentialSmoothing()
    model.fit(ts)
    forecast = model.predict(horizon)
    values = forecast.values()
    return float(values[-1][0])


class PredictAdapter:
    """SAPAL Predict stage — token burn rate forecast (ADR-4 / C+-4)."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def predict(
        self,
        analysis: dict[str, Any],
        events: list[TelemetryEvent] | None = None,
    ) -> dict[str, Any]:
        """Predict outcomes from analysis + telemetry history."""
        high_risk = bool(analysis.get("anomaly_detected"))
        series = _hourly_token_counts(events or [])
        darts_value = _darts_forecast(series)
        fallback = _rolling_mean_forecast(series)
        forecast_tokens_per_hour = darts_value if darts_value is not None else fallback
        method = "darts" if darts_value is not None else "rolling_mean"

        burn_limit = float(self._config.get("token_burn_limit_per_hour", 100_000.0))
        burn_high = forecast_tokens_per_hour > burn_limit

        risk_level = "high" if (high_risk or burn_high) else "low"
        return {
            "risk_level": risk_level,
            "recommended_action": "review" if risk_level == "high" else "continue",
            "forecast_tokens_per_hour": forecast_tokens_per_hour,
            "forecast_method": method,
            "history_points": len(series),
        }
