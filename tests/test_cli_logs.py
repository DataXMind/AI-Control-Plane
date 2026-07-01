"""CLI logs tests — HTTP-only via respx (Milestone B Sprint 2)."""

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


def test_logs_list(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/telemetry/events").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "event_id": "evt-1",
                    "event_type": "mcp.tool_call",
                    "agent_id": "agent2",
                    "project_id": "rust-gateway",
                    "payload": {},
                    "timestamp": "2026-06-23T12:00:00+00:00",
                    "event_hash": "abc",
                    "previous_hash": None,
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                },
            ],
        ),
    )

    result = runner.invoke(app, ["logs", "--project", "rust-gateway"])

    assert result.exit_code == 0
    assert "mcp.tool_call" in result.output


def test_logs_json_output(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/telemetry/events").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "event_id": "evt-2",
                    "event_type": "policy.evaluate",
                    "agent_id": "agent2",
                    "project_id": "rust-gateway",
                    "payload": {},
                    "timestamp": "2026-06-23T12:00:00+00:00",
                    "event_hash": "def",
                    "previous_hash": None,
                    "id": "223e4567-e89b-12d3-a456-426614174001",
                },
            ],
        ),
    )

    result = runner.invoke(app, ["logs", "--json", "--limit", "5"])

    assert result.exit_code == 0
    assert "policy.evaluate" in result.output


def test_logs_service_unavailable(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/telemetry/events").mock(
        return_value=httpx.Response(503, json={"reason": "down"}),
    )

    result = runner.invoke(app, ["logs"])

    assert result.exit_code == 1
    assert "telemetry request failed" in result.output
