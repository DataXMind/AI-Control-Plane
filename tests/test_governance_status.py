"""Governance UX runtime endpoint tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ai_control_plane.api.schemas import GovernanceStatusResponse
from ai_control_plane.api.server import create_app
from ai_control_plane.core.governance_catalog import (
    CASE_STUDIES,
    GOVERNANCE_FRAMEWORK,
    LESSON_PATTERNS,
)


def test_governance_status_returns_6_layer_payload() -> None:
    client = TestClient(create_app())
    response = client.get("/governance/status")
    assert response.status_code == 200
    body = response.json()
    parsed = GovernanceStatusResponse.model_validate(body)
    assert parsed.framework == GOVERNANCE_FRAMEWORK
    assert parsed.config_loaded is True
    assert parsed.policy_rules_count > 0
    assert parsed.milestones["milestone_c_plus"] == "CLOSED"
    assert parsed.milestones["public_beta"] == "BETA"
    assert set(parsed.layers.keys()) == {"L0", "L1", "L2", "L3", "L4", "L5"}
    assert len(parsed.case_studies) == len(CASE_STUDIES)
    assert parsed.case_studies[0].id == "CS-01"
    assert len(parsed.verify_gate) >= 5
    assert len(parsed.known_gaps) >= 7
    assert parsed.known_gaps[0].id == "G-01"
    closed = {g.id for g in parsed.known_gaps if g.status == "CLOSED"}
    assert "G-01" in closed and "G-02" in closed and "G-03" in closed and "G-04" in closed
    assert "G-06" in closed and "G-07" in closed
    open_gaps = {g.id for g in parsed.known_gaps if g.status == "OPEN"}
    assert open_gaps == {"G-05"}
    assert len(parsed.lessons_patterns) == len(LESSON_PATTERNS)
    assert parsed.lessons_patterns[0].id == "P-01"
    assert parsed.lessons_patterns[0].case_study_id == "CS-01"
    assert parsed.governance_version == "1.6.0"
    assert len(parsed.public_beta.gates_remaining) == 1
    assert len(parsed.public_beta.gates_closed) >= 10
    assert parsed.public_beta.gates_blocking_pb12 == []
    assert len(parsed.public_beta.gate_details) == 7
    assert parsed.practice_evidence.studies_completed == 8
    assert parsed.practice_evidence.open_gaps_count == 1
    assert parsed.practice_evidence.study_08_url.endswith("study-08-shipped-remote/RESULTS.md")
    assert parsed.practice_evidence.mac_pilot_deploy_url.endswith(
        "mac-pilot-deploy-2026-06-30/RESULTS.md"
    )
    assert parsed.practice_evidence.overall_verdict == "PASS"


def test_governance_status_schema_keys_stable() -> None:
    client = TestClient(create_app())
    response = client.get("/governance/status")
    expected = frozenset(GovernanceStatusResponse.model_fields.keys())
    assert frozenset(response.json().keys()) == expected
