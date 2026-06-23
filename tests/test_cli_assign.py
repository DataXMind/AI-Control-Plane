"""CLI assign tests — HTTP-only via mocked api/server.py (MB-S1-4, GAP-CLI-1)."""

from __future__ import annotations

import httpx
import pytest
import respx
from typer.testing import CliRunner

from ai_control_plane.main import app

runner = CliRunner()
API_BASE = "http://localhost:8000"


@pytest.fixture(autouse=True)
def _cli_api_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ACP_API_URL", API_BASE)


def test_assign_allowed(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/policy/evaluate").mock(
        return_value=httpx.Response(
            200,
            json={
                "allowed": True,
                "reason": "rbac_pass",
                "requires_approval": False,
                "policy_id": "rbac_backend",
                "latency_ms": 1.0,
            },
        ),
    )
    respx_mock.post(f"{API_BASE}/tasks").mock(
        return_value=httpx.Response(
            200,
            json={
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "state": "PENDING",
                "progress": 0,
                "updated_at": "2026-06-23T12:00:00+00:00",
            },
        ),
    )

    result = runner.invoke(app, ["assign", "rust-gateway", "agent2", "git_read"])

    assert result.exit_code == 0
    assert "Task created:" in result.output
    assert respx_mock.calls.call_count == 2


def test_assign_denied(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/policy/evaluate").mock(
        return_value=httpx.Response(
            200,
            json={
                "allowed": False,
                "reason": "rbac_deny_k8s",
                "requires_approval": False,
                "policy_id": "rbac_backend",
                "latency_ms": 1.0,
            },
        ),
    )

    result = runner.invoke(app, ["assign", "rust-gateway", "agent2", "k8s_apply_prod"])

    assert result.exit_code == 1
    assert "rbac_deny_k8s" in (result.output + result.stderr)
    assert respx_mock.calls.call_count == 1


def test_assign_requires_approval(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/policy/evaluate").mock(
        return_value=httpx.Response(
            200,
            json={
                "allowed": True,
                "reason": "abac_requires_approval",
                "requires_approval": True,
                "policy_id": "abac_prod_k8s",
                "latency_ms": 1.0,
            },
        ),
    )

    result = runner.invoke(app, ["assign", "rust-gateway", "agent1", "k8s_apply_prod"])

    assert result.exit_code == 0
    assert "Pending approval" in result.output
    assert respx_mock.calls.call_count == 1
