"""CLI gov tests — agentctl gov status (MB-S1-4 extension, Gov UX #86)."""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from typer.testing import CliRunner

from ai_control_plane.main import app

runner = CliRunner()
API_BASE = "http://localhost:8000"

GOV_PAYLOAD: dict[str, object] = {
    "status": "ok",
    "framework": "6-layer-karpathy",
    "governance_version": "1.4.0",
    "config_loaded": True,
    "policy_rules_count": 8,
    "milestones": {
        "milestone_c_plus": "CLOSED",
        "public_beta": "IN_PROGRESS",
    },
    "layers": {"L0": "Behavioral", "L5": "Memory"},
    "verify_gate": ["pytest tests/ -v"],
    "doc_links": {"agents_md": "AGENTS.md"},
    "public_beta": {
        "phase": "PB-9 staging soak",
        "open_issues": "#77-#80",
        "soak_started": "2026-06-22",
        "soak_review_target": "2026-07-06",
        "gates_remaining": ["PB-9 calendar soak (G-05)"],
        "gates_closed": ["PB-11 legal artifacts"],
    },
    "case_studies": [
        {
            "id": "CS-01",
            "title": "Monolithic PR risk",
            "layer": "L3",
            "occurrence": "PR #48",
            "runtime_check": "PR diff LOC before merge",
            "action": "Split PR",
        },
        {
            "id": "CS-06",
            "title": "Fail-closed policy path",
            "layer": "L4",
            "occurrence": "SMK-04",
            "runtime_check": "POST /policy/evaluate deny unknown",
            "action": "DENY on API down",
        },
    ],
    "known_gaps": [
        {
            "id": "G-01",
            "study": "05",
            "title": "Kill switch drill",
            "severity": "medium",
            "status": "CLOSED",
            "remediation": "G2-1",
        },
    ],
    "lessons_patterns": [
        {
            "id": "P-01",
            "title": "Monolithic PR risk",
            "layer": "L3",
            "status": "ACTIVE",
            "rule_ref": "CURSOR_RISK_POLICY.md F4",
            "case_study_id": "CS-01",
            "prevention": "git diff master --stat",
        },
    ],
    "practice_evidence": {
        "studies_completed": 8,
        "last_run": "2026-06-26",
        "overall_verdict": "PASS",
        "open_gaps_count": 1,
        "artifacts_count": 32,
        "hosts": ["MSI WSL", "Mac Mini M2", "ubuntu-vps"],
        "network_topologies": ["localhost", "Docker", "LAN", "Tailscale"],
        "note": "Studies 01-08 PASS",
        "index_url": "docs/governance/practice-evidence/README.md",
        "audit_url": "docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md",
        "study_08_url": "docs/governance/practice-evidence/study-08-shipped-remote/RESULTS.md",
    },
}


@pytest.fixture(autouse=True)
def _cli_api_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ACP_API_URL", API_BASE)


def test_gov_status_text_output(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/governance/status").mock(
        return_value=httpx.Response(200, json=GOV_PAYLOAD),
    )

    result = runner.invoke(app, ["gov", "status"])

    assert result.exit_code == 0
    assert "6-layer-karpathy (v1.4.0)" in result.output
    assert "Config loaded: True | Policy rules: 8" in result.output
    assert "milestone_c_plus: CLOSED" in result.output
    assert "PB-9 staging soak (#77-#80)" in result.output
    assert "[CS-01] Monolithic PR risk (L3)" in result.output
    assert "PR diff LOC before merge" in result.output
    assert "GOVERNANCE_UX_RUNTIME.md" in result.output


def test_gov_status_json_output(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/governance/status").mock(
        return_value=httpx.Response(200, json=GOV_PAYLOAD),
    )

    result = runner.invoke(app, ["gov", "status", "--json"])

    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert parsed["framework"] == "6-layer-karpathy"
    assert parsed["governance_version"] == "1.4.0"
    assert len(parsed["case_studies"]) == 2
    assert parsed["case_studies"][0]["id"] == "CS-01"


def test_gov_status_http_error(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/governance/status").mock(
        return_value=httpx.Response(503, json={"detail": "unavailable"}),
    )

    result = runner.invoke(app, ["gov", "status"])

    assert result.exit_code != 0
