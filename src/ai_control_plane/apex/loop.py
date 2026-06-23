"""Loop — Milestone C: SAPAL orchestration entrypoint."""

from __future__ import annotations

from ai_control_plane.apex.act import ActAdapter
from ai_control_plane.apex.analyze import AnalyzeAdapter
from ai_control_plane.apex.learn import LearnAdapter
from ai_control_plane.apex.predict import PredictAdapter
from ai_control_plane.apex.sense import SenseAdapter


class SapalLoop:
    """Sense → Analyze → Predict → Act → Learn orchestrator (stub until Milestone C)."""

    def __init__(self, config: dict) -> None:
        self._config = config
        self._sense = SenseAdapter(config)
        self._analyze = AnalyzeAdapter(config)
        self._predict = PredictAdapter(config)
        self._act = ActAdapter(config)
        self._learn = LearnAdapter(config)

    def run(self) -> None:
        """Run one SAPAL cycle."""
        raise NotImplementedError("Milestone C")
