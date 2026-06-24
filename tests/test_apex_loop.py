"""SAPAL loop and adapter tests — Milestone C (MC-1..MC-6, MC-11)."""

from __future__ import annotations

from ai_control_plane.apex.act import ActAdapter
from ai_control_plane.apex.analyze import AnalyzeAdapter
from ai_control_plane.apex.learn import LearnAdapter
from ai_control_plane.apex.loop import SapalLoop
from ai_control_plane.apex.pipeline import run_sapal_pipeline
from ai_control_plane.apex.predict import PredictAdapter
from ai_control_plane.apex.sense import SenseAdapter
from ai_control_plane.core.models import TelemetryEvent
from ai_control_plane.core.telemetry import InMemoryTelemetryStore


def _event(n: int) -> TelemetryEvent:
    return TelemetryEvent(
        event_type="TOOL_CALL",
        agent_id="agent2",
        project_id="rust-gateway",
        payload={"n": n},
    )


def test_all_apex_modules_importable() -> None:
    from ai_control_plane.apex import act, analyze, learn, loop, predict, sense

    assert all([loop, sense, analyze, predict, act, learn])


def test_sense_collect_aggregates_events() -> None:
    events = [_event(1), _event(2)]
    out = SenseAdapter({}).collect(events)
    assert out["event_count"] == 2
    assert out["by_event_type"]["TOOL_CALL"] == 2


def test_analyze_detects_anomaly_above_threshold() -> None:
    adapter = AnalyzeAdapter({"anomaly_event_threshold": 1})
    assert adapter.analyze({"event_count": 5, "z_score_anomaly": False})["anomaly_detected"] is True
    no_anomaly = adapter.analyze({"event_count": 0, "z_score_anomaly": False})
    assert no_anomaly["anomaly_detected"] is False


def test_predict_maps_risk_level() -> None:
    high = PredictAdapter({}).predict({"anomaly_detected": True}, [])
    low = PredictAdapter({}).predict({"anomaly_detected": False}, [])
    assert high["risk_level"] == "high"
    assert low["risk_level"] == "low"


def test_act_proposal_only() -> None:
    low = ActAdapter({}).execute({"risk_level": "low", "recommended_action": "continue"})
    high = ActAdapter({}).execute({"risk_level": "high", "recommended_action": "review"})
    assert low["executed"] is False
    assert high["executed"] is False
    assert low["status"] == "proposal_only"
    assert low["proposals"]


def test_learn_requires_approval() -> None:
    learn = LearnAdapter({})
    learn.ingest([_event(1)])
    proposal = learn.propose_policy_update()
    assert proposal["events_reviewed"] == 1
    denied = learn.apply_adaptation(proposal, approved=False)
    assert denied["applied"] is False


def test_sapal_loop_run_returns_full_cycle() -> None:
    store = InMemoryTelemetryStore()
    store.append(_event(1))
    result = SapalLoop({}, store).run()
    assert "sense" in result
    assert "analysis" in result
    assert "prediction" in result
    assert "act" in result
    assert "learn_proposal" in result
    assert result["telemetry_chain_valid"] is True


def test_pipeline_entrypoint() -> None:
    store = InMemoryTelemetryStore()
    result = run_sapal_pipeline(store, {})
    assert result["sense"]["event_count"] == 0
