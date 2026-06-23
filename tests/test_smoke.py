"""ACP smoke tests (SMK-01..SMK-05) — gold-pattern build verification gate.

Run: pytest tests/test_smoke.py -v -m smoke
Or: scripts/smoke_acp.sh (CI mode) / scripts/smoke_acp.sh --live (manual curl)
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import ai_control_plane.core.registry
import ai_control_plane.core.telemetry

pytestmark = pytest.mark.smoke


def test_smk01_core_import_python() -> None:
    """SMK-01: Core modules import without error (registry + telemetry)."""
    # pytest import collection already verifies — explicit import = clear signal
    assert ai_control_plane.core.registry is not None
    assert ai_control_plane.core.telemetry is not None


def test_smk02_health_readiness(client: TestClient) -> None:
    """SMK-02: GET /health returns 200 with config wire proof."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["config_loaded"] is True
    assert body["policy_rules_count"] > 0
    assert len(body["agents_loaded"]) > 0
    assert len(body["projects_loaded"]) > 0


def test_smk03_policy_allow_critical_path(client: TestClient) -> None:
    """SMK-03: Policy evaluate allows backend git_read (core governance path)."""
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "agent2",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
            "role": "backend",
        },
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is True


def test_smk04_policy_deny_fail_closed(client: TestClient) -> None:
    """SMK-04: Unknown agent is denied with explicit reason (fail-closed)."""
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "unknown-agent-xyz",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
            "args": {},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "reason" in body
    assert body["reason"] != ""
    # HTTP 200 + allowed=false is correct; 503 only when server unreachable.


def test_smk05_quota_dependency_read(client: TestClient) -> None:
    """SMK-05: GET /quota reads configured project limits (floor from fixture)."""
    response = client.get("/quota/rust-gateway")
    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "rust-gateway"
    assert "tokens_remaining" in body
    # Floor 100_000: agents.yml claude-pro-backend max_tokens_per_day=150000
    assert body["tokens_remaining"] >= 100_000
