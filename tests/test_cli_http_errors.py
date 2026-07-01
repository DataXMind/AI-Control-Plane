"""CLI HTTP helper transport and validation errors (coverage Tier 2)."""

from __future__ import annotations

import httpx
import pytest
import respx

from ai_control_plane.api.schemas import (
    ApprovalResolveRequest,
    PolicyEvalRequest,
    TaskRegisterRequest,
)
from ai_control_plane.cli import _http as http_helpers


@pytest.fixture(autouse=True)
def _api_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ACP_API_URL", "http://127.0.0.1:8000")


@respx.mock
def test_post_policy_evaluate_transport_error() -> None:
    respx.post("http://127.0.0.1:8000/policy/evaluate").mock(
        side_effect=httpx.ConnectError("connection refused"),
    )
    with pytest.raises(RuntimeError, match="policy service unavailable"):
        http_helpers.post_policy_evaluate(
            PolicyEvalRequest(
                agent_id="agent2",
                project_id="rust-gateway",
                tool_name="git_read",
                role="backend",
            ),
        )


@respx.mock
def test_post_policy_evaluate_invalid_json() -> None:
    respx.post("http://127.0.0.1:8000/policy/evaluate").mock(
        return_value=httpx.Response(200, text="not-json"),
    )
    with pytest.raises(RuntimeError, match="invalid policy response"):
        http_helpers.post_policy_evaluate(
            PolicyEvalRequest(
                agent_id="agent2",
                project_id="rust-gateway",
                tool_name="git_read",
                role="backend",
            ),
        )


@respx.mock
def test_get_project_status_non_200() -> None:
    respx.get("http://127.0.0.1:8000/status/rust-gateway").mock(
        return_value=httpx.Response(503, json={"reason": "down"}),
    )
    with pytest.raises(RuntimeError, match="status request failed"):
        http_helpers.get_project_status("rust-gateway")


@respx.mock
def test_post_register_task_timeout() -> None:
    respx.post("http://127.0.0.1:8000/tasks").mock(
        side_effect=httpx.ReadTimeout("slow"),
    )
    with pytest.raises(RuntimeError, match="task registration unavailable"):
        http_helpers.post_register_task(
            TaskRegisterRequest(
                project_id="rust-gateway",
                agent_id="agent2",
                task_type="assign",
                task_id="123e4567-e89b-12d3-a456-426614174000",
                payload={},
            ),
        )


@respx.mock
def test_post_policy_approve_failure_status() -> None:
    respx.post("http://127.0.0.1:8000/policy/approve").mock(
        return_value=httpx.Response(503, json={"reason": "fail"}),
    )
    with pytest.raises(RuntimeError, match="approval request failed"):
        http_helpers.post_policy_approve(
            ApprovalResolveRequest(
                approval_id="00000000-0000-0000-0000-000000000001",
                approved=True,
                approver="reviewer1",
            ),
        )


@respx.mock
def test_get_project_quota_invalid_body() -> None:
    respx.get("http://127.0.0.1:8000/quota/rust-gateway").mock(
        return_value=httpx.Response(200, json={"bad": "shape"}),
    )
    with pytest.raises(Exception):
        http_helpers.get_project_quota("rust-gateway")


@respx.mock
def test_get_telemetry_not_a_list() -> None:
    respx.get("http://127.0.0.1:8000/telemetry/events").mock(
        return_value=httpx.Response(200, json={"events": []}),
    )
    with pytest.raises(RuntimeError, match="invalid telemetry response"):
        http_helpers.get_telemetry_events()


@respx.mock
def test_get_apex_status_non_dict() -> None:
    respx.get("http://127.0.0.1:8000/apex/status").mock(
        return_value=httpx.Response(200, json=[]),
    )
    with pytest.raises(RuntimeError, match="invalid apex status response"):
        http_helpers.get_apex_status()


@respx.mock
def test_get_governance_status_ok() -> None:
    respx.get("http://127.0.0.1:8000/governance/status").mock(
        return_value=httpx.Response(200, json={"governance_version": "1.5.0"}),
    )
    body = http_helpers.get_governance_status()
    assert body["governance_version"] == "1.5.0"


def test_format_json_roundtrip() -> None:
    text = http_helpers.format_json({"a": 1, "b": "x"})
    assert '"a": 1' in text
