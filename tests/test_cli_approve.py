"""CLI approve tests — HTTP-only via respx (Milestone B Sprint 2)."""

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


def test_approve_allowed(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/policy/approve").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "approved": True,
                "approver": "reviewer1",
            },
        ),
    )

    result = runner.invoke(
        app,
        ["approve", "123e4567-e89b-12d3-a456-426614174000", "--approver", "reviewer1"],
    )

    assert result.exit_code == 0
    assert "approved" in result.output.lower()


def test_approve_denied(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{API_BASE}/policy/approve").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "approved": False,
                "approver": "reviewer1",
            },
        ),
    )

    result = runner.invoke(
        app,
        ["approve", "123e4567-e89b-12d3-a456-426614174000", "--approver", "reviewer1", "--deny"],
    )

    assert result.exit_code == 0
    assert "denied" in result.output.lower()
