"""CLI quota tests — HTTP-only via respx (Milestone B Sprint 2)."""

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


def test_quota_project(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(f"{API_BASE}/quota/rust-gateway").mock(
        return_value=httpx.Response(
            200,
            json={
                "project_id": "rust-gateway",
                "tokens_used": 1000.0,
                "tokens_remaining": 99000.0,
                "requests_today": 5,
            },
        ),
    )

    result = runner.invoke(app, ["quota", "rust-gateway"])

    assert result.exit_code == 0
    assert "99000" in result.output
    assert "rust-gateway" in result.output
