"""Import-clean regression tests for apex/ SAPAL stubs (NEW-4)."""

from __future__ import annotations

import pytest

from ai_control_plane.apex.act import ActAdapter
from ai_control_plane.apex.analyze import AnalyzeAdapter
from ai_control_plane.apex.learn import LearnAdapter
from ai_control_plane.apex.loop import SapalLoop
from ai_control_plane.apex.pipeline import run_sapal_pipeline
from ai_control_plane.apex.predict import PredictAdapter
from ai_control_plane.apex.sense import SenseAdapter


def test_all_apex_modules_importable() -> None:
    from ai_control_plane.apex import act, analyze, learn, loop, predict, sense

    assert all([loop, sense, analyze, predict, act, learn])


def test_sapal_loop_run_raises() -> None:
    loop = SapalLoop({})
    with pytest.raises(NotImplementedError, match="Milestone C"):
        loop.run()


def test_pipeline_entrypoint_raises() -> None:
    with pytest.raises(NotImplementedError, match="Milestone C"):
        run_sapal_pipeline()


@pytest.mark.parametrize(
    ("adapter_cls", "method", "args"),
    [
        (SenseAdapter, "collect", ([],)),
        (AnalyzeAdapter, "analyze", ({},)),
        (PredictAdapter, "predict", ({},)),
        (ActAdapter, "execute", ({},)),
        (LearnAdapter, "ingest", ([],)),
        (LearnAdapter, "propose_policy_update", ()),
        (LearnAdapter, "apply_adaptation", ({}, False)),
    ],
)
def test_apex_adapters_raise_not_implemented(
    adapter_cls: type,
    method: str,
    args: tuple,
) -> None:
    adapter = adapter_cls({})
    with pytest.raises(NotImplementedError, match="Milestone C"):
        getattr(adapter, method)(*args)
