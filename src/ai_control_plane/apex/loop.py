"""Loop — Milestone C: SAPAL orchestration entrypoint."""

from __future__ import annotations

from typing import Any

from ai_control_plane.apex.act import ActAdapter
from ai_control_plane.apex.analyze import AnalyzeAdapter
from ai_control_plane.apex.learn import LearnAdapter
from ai_control_plane.apex.predict import PredictAdapter
from ai_control_plane.apex.sense import SenseAdapter
from ai_control_plane.core.telemetry import TelemetryStore


class SapalLoop:
    """Sense → Analyze → Predict → Act → Learn orchestrator."""

    def __init__(self, config: dict[str, Any], telemetry_store: TelemetryStore) -> None:
        self._config = config
        self._telemetry_store = telemetry_store
        self._sense = SenseAdapter(config)
        self._analyze = AnalyzeAdapter(config)
        self._predict = PredictAdapter(config)
        self._act = ActAdapter(config)
        self._learn = LearnAdapter(config)

    def run(self) -> dict[str, Any]:
        """Run one SAPAL cycle."""
        events = self._telemetry_store.list_events()
        sense = self._sense.collect(events)
        analysis = self._analyze.analyze(sense)
        prediction = self._predict.predict(analysis)
        act_result = self._act.execute(prediction)
        self._learn.ingest(events)
        proposal = self._learn.propose_policy_update()
        return {
            "sense": sense,
            "analysis": analysis,
            "prediction": prediction,
            "act": act_result,
            "learn_proposal": proposal,
            "telemetry_chain_valid": self._telemetry_store.verify_chain(),
        }
