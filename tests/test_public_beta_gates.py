"""P-14 — public beta gate evidence predicates."""

from __future__ import annotations

from ai_control_plane.core.governance_catalog import (
    PUBLIC_BETA_GATE_REGISTRY,
    build_public_beta_summary,
)


def test_build_public_beta_summary_gate_counts() -> None:
    summary = build_public_beta_summary()
    assert len(summary["gates_remaining"]) == 7
    assert len(summary["gates_closed"]) == 4
    assert len(summary["gate_details"]) == len(PUBLIC_BETA_GATE_REGISTRY)


def test_gates_blocking_pb12_only_open_blockers() -> None:
    summary = build_public_beta_summary()
    blocking = summary["gates_blocking_pb12"]
    assert blocking == ["PB-9", "PB-12"]
    passed_ids = {g["id"] for g in summary["gate_details"] if g["practice_status"] == "PASS"}
    assert "PB-7" in passed_ids
    assert "PB-8" in passed_ids
    assert "PB-SEC" in passed_ids


def test_gate_details_include_evidence_paths() -> None:
    summary = build_public_beta_summary()
    pb9 = next(g for g in summary["gate_details"] if g["id"] == "PB-9")
    assert pb9["evidence"].endswith("PB9_STAGING_SOAK_LOG.md")
    assert pb9["blocks_pb12"] is True
