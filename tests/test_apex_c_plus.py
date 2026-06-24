"""Milestone C+ tests — C+-1..C+-5 (ADR pack)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from ai_control_plane.apex.act import ActAdapter
from ai_control_plane.apex.analyze import AnalyzeAdapter
from ai_control_plane.apex.predict import PredictAdapter
from ai_control_plane.apex.sense import SenseAdapter, z_score_anomaly
from ai_control_plane.core.models import TelemetryEvent
from ai_control_plane.core.policies import ApprovalGate
from ai_control_plane.core.telemetry import InMemoryTelemetryStore


def _event(**payload: object) -> TelemetryEvent:
    return TelemetryEvent(
        event_type="TOOL_CALL",
        agent_id="agent2",
        project_id="rust-gateway",
        payload=dict(payload),
    )


def test_z_score_detects_outlier() -> None:
    series = [1.0] * 9 + [100.0]
    assert z_score_anomaly(series) is True
    assert z_score_anomaly([1.0, 1.0, 1.0]) is False


def test_sense_collect_from_store_uses_replay() -> None:
    store = InMemoryTelemetryStore()
    store.append(_event(n=1))
    store.append(_event(n=100))
    out = SenseAdapter({}).collect_from_store(store)
    assert out["event_count"] == 2
    assert "z_score_anomaly" in out


def test_analyze_argos_stages_on_anomaly() -> None:
    gate = ApprovalGate()
    adapter = AnalyzeAdapter({"anomaly_event_threshold": 1}, approval_gate=gate)
    sense = {"event_count": 5, "z_score_anomaly": True, "isolation_forest_anomaly": None}
    result = adapter.analyze(sense)
    assert result["status"] == "ok"
    assert result["anomaly_detected"] is True
    assert result["detect"] is not None
    assert result["repair"] is not None
    assert result["review"]["requires_approval"] is True


def test_predict_rolling_mean_without_darts() -> None:
    now = datetime.now(tz=UTC)
    events = [
        TelemetryEvent(
            event_type="TOOL_CALL",
            agent_id="a",
            project_id="p",
            payload={"tokens": 100},
            timestamp=now - timedelta(hours=2),
        ),
        TelemetryEvent(
            event_type="TOOL_CALL",
            agent_id="a",
            project_id="p",
            payload={"tokens": 200},
            timestamp=now - timedelta(hours=1),
        ),
    ]
    out = PredictAdapter({}).predict({"anomaly_detected": False}, events)
    assert out["forecast_method"] == "rolling_mean"
    assert out["forecast_tokens_per_hour"] > 0


def test_act_proposal_only_option_c() -> None:
    out = ActAdapter({}).execute({"recommended_action": "continue", "risk_level": "low"})
    assert out["executed"] is False
    assert out["status"] == "proposal_only"
    assert out["policy_eval_required"] is True
    assert out["proposals"]
