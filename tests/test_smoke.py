"""ACP smoke tests (SMK-01..SMK-05) — gold-pattern build verification gate.

Run: pytest tests/test_smoke.py -v -m smoke
Or: scripts/smoke_acp.sh (starts API if needed)
"""

from __future__ import annotations

import subprocess
import sys

import pytest
from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app

pytestmark = pytest.mark.smoke


def test_smk01_p0_core_import() -> None:
    """SMK-01: Core modules import without error (registry + telemetry)."""
    subprocess.run(
        [
            sys.executable,
            "-c",
            "from ai_control_plane.core import registry, telemetry; print('P0 OK')",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_smk02_health_readiness() -> None:
    """SMK-02: GET /health returns 200 with config wire proof."""
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["config_loaded"] is True
    assert body["policy_rules_count"] > 0
    assert len(body["agents_loaded"]) > 0
    assert len(body["projects_loaded"]) > 0


def test_smk03_policy_allow_critical_path() -> None:
    """SMK-03: Policy evaluate allows backend git_read (core governance path)."""
    client = TestClient(create_app())
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


def test_smk04_policy_deny_fail_closed() -> None:
    """SMK-04: Unknown agent is denied (fail-closed, no default-allow)."""
    client = TestClient(create_app())
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "unknown-agent",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
        },
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is False


def test_smk05_quota_dependency_read() -> None:
    """SMK-05: GET /quota reads configured project limits (config + quota path)."""
    client = TestClient(create_app())
    response = client.get("/quota/rust-gateway")
    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "rust-gateway"
    assert body["tokens_remaining"] > 0
