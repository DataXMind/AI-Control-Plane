"""CLI status tests — HTTP-only via mocked api/server.py (MB-S1-4, GAP-CLI-1)."""

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


def test_status_project(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/status/rust-gateway").mock(
        return_value=httpx.Response(
            200,
            json={
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "state": "RUNNING",
                "progress": 42,
                "updated_at": "2026-06-23T12:00:00+00:00",
            },
        ),
    )

    result = runner.invoke(app, ["status", "--project", "rust-gateway"])

    assert result.exit_code == 0
    assert "RUNNING" in result.output
    assert "rust-gateway" in result.output
