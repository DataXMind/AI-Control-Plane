"""CLI apex tests — HTTP-only via mocked api/server.py (MC-7)."""

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


def test_apex_status(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/apex/status").mock(
        return_value=httpx.Response(
            200,
            json={
                "telemetry_event_count": 2,
                "telemetry_chain_valid": True,
                "last_cycle": None,
            },
        ),
    )

    result = runner.invoke(app, ["apex", "status"])
    assert result.exit_code == 0
    assert "telemetry_event_count" in result.output


def test_apex_trigger(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/apex/trigger").mock(
        return_value=httpx.Response(
            200,
            json={
                "sense": {"event_count": 0},
                "telemetry_chain_valid": True,
            },
        ),
    )

    result = runner.invoke(app, ["apex", "trigger"])
    assert result.exit_code == 0
    assert "event_count" in result.output
