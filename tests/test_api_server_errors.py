"""API server error paths, approve, and fail-closed handlers (coverage Tier 1)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from ai_control_plane.api import server as server_module
from ai_control_plane.api.server import AppState, create_app
from ai_control_plane.core.identity import JWTValidationError, encode_hs256_token
from ai_control_plane.core.policies import ApprovalGate


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_policy_evaluate_invalid_body_fail_closed(client: TestClient) -> None:
    response = client.post("/policy/evaluate", json={})
    assert response.status_code == 503
    body = response.json()
    assert body["allowed"] is False
    assert "invalid request" in body["reason"]


def test_policy_evaluate_unknown_agent_fail_closed(client: TestClient) -> None:
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "no-such-agent",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "unknown agent or role" in body["reason"]


def test_policy_evaluate_agent_not_on_project(client: TestClient) -> None:
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "agent2",
            "project_id": "unknown-project",
            "tool_name": "git_read",
            "role": "backend",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "not authorized" in body["reason"]


def test_policy_evaluate_timeout_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _timeout(coro: object, timeout: float | None = None) -> object:
        raise TimeoutError

    monkeypatch.setattr(server_module.asyncio, "wait_for", _timeout)
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
    assert response.status_code == 503
    assert response.json()["allowed"] is False
    assert "timed out" in response.json()["reason"]


def test_policy_evaluate_engine_exception_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("engine failure")

    monkeypatch.setattr(app.state.acp.policy_engine, "evaluate", _boom)
    client = TestClient(app)
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "agent2",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
            "role": "backend",
        },
    )
    assert response.status_code == 503
    assert response.json()["allowed"] is False
    assert "policy evaluation failed" in response.json()["reason"]


def test_policy_approve_resolves_pending_request() -> None:
    app = create_app()
    pending = app.state.acp.approval_gate.request("test.event", {"k": "v"})
    client = TestClient(app)
    response = client.post(
        "/policy/approve",
        json={
            "approval_id": str(pending.id),
            "approved": True,
            "approver": "reviewer1",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["approved"] is True
    assert body["approver"] == "reviewer1"


def test_policy_approve_unknown_id_returns_503(client: TestClient) -> None:
    response = client.post(
        "/policy/approve",
        json={
            "approval_id": str(uuid4()),
            "approved": True,
            "approver": "reviewer1",
        },
    )
    assert response.status_code == 503
    assert response.json()["reason"] == "approval resolution failed"


def test_register_task_unknown_project(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "project_id": "unknown-project",
            "agent_id": "agent2",
            "task_type": "assign",
            "task_id": str(uuid4()),
            "payload": {},
        },
    )
    assert response.status_code == 503
    assert "unknown project" in response.json()["reason"]


def test_register_task_store_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()

    def _fail(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("disk full")

    monkeypatch.setattr(app.state.acp.task_store, "set", _fail)
    client = TestClient(app)
    response = client.post(
        "/tasks",
        json={
            "project_id": "rust-gateway",
            "agent_id": "agent2",
            "task_type": "assign",
            "task_id": str(uuid4()),
            "payload": {},
        },
    )
    assert response.status_code == 503
    assert response.json()["reason"] == "task registration failed"


def test_project_status_store_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()

    def _fail(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("store down")

    monkeypatch.setattr(app.state.acp.task_store, "get", _fail)
    client = TestClient(app)
    response = client.get("/status/rust-gateway")
    assert response.status_code == 503
    assert response.json()["reason"] == "status unavailable"


def test_quota_unknown_project(client: TestClient) -> None:
    response = client.get("/quota/unknown-project")
    assert response.status_code == 503
    assert "unknown project" in response.json()["reason"]


def test_quota_store_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()
    store = MagicMock()
    store.get.side_effect = RuntimeError("redis down")
    app.state.acp.quota_store = store
    client = TestClient(app)
    response = client.get("/quota/rust-gateway")
    assert response.status_code == 503
    assert response.json()["reason"] == "quota unavailable"


def test_agent_quota_store_failure() -> None:
    app = create_app()
    tracker = MagicMock()
    tracker.remaining.side_effect = RuntimeError("redis down")
    app.state.acp.quota_tracker = tracker
    client = TestClient(app)
    response = client.get("/quota/agent/agent2")
    assert response.status_code == 503
    assert response.json()["reason"] == "quota unavailable"


def test_profile_quota_unknown_profile(client: TestClient) -> None:
    response = client.get("/quota/profile/unknown-profile")
    assert response.status_code == 503


def test_telemetry_list_store_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()
    store = MagicMock()
    store.list_events.side_effect = RuntimeError("telemetry down")
    app.state.acp.telemetry_store = store
    client = TestClient(app)
    response = client.get("/telemetry/events")
    assert response.status_code == 503
    assert response.json()["reason"] == "telemetry unavailable"


def test_apex_status_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()

    def _fail(*_args: object, **_kwargs: object) -> list[Any]:
        raise RuntimeError("apex broken")

    monkeypatch.setattr(app.state.acp.telemetry_store, "list_events", _fail)
    client = TestClient(app)
    response = client.get("/apex/status")
    assert response.status_code == 503


def test_apex_trigger_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        server_module,
        "run_sapal_pipeline",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("pipeline fail")),
    )
    client = TestClient(create_app())
    response = client.post("/apex/trigger")
    assert response.status_code == 503


def test_identity_verify_missing_agent_id_claim(client: TestClient) -> None:
    token = encode_hs256_token({"project_id": "rust-gateway", "role": "backend"})
    response = client.post("/identity/verify", json={"token": token})
    assert response.status_code == 401
    assert response.json()["detail"] == "missing agent_id claim"


def test_identity_verify_missing_role_claim() -> None:
    app = create_app()
    validator = MagicMock()
    validator.validate.return_value = {
        "agent_id": "agent2",
        "project_id": "rust-gateway",
    }
    entry = dict(app.state.acp.agent_registry["agent2"])
    entry.pop("role", None)
    app.state.acp.agent_registry["agent2"] = entry
    app.state.acp.jwt_validator = validator
    client = TestClient(app)
    response = client.post("/identity/verify", json={"token": "token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "missing role claim"


def test_identity_verify_jwt_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()
    validator = MagicMock()
    validator.validate.side_effect = JWTValidationError("bad token")
    app.state.acp.jwt_validator = validator
    client = TestClient(app)
    response = client.post("/identity/verify", json={"token": "bad.token.here"})
    assert response.status_code == 401


def test_identity_verify_internal_error(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()
    validator = MagicMock()
    validator.validate.side_effect = RuntimeError("validator crash")
    app.state.acp.jwt_validator = validator
    client = TestClient(app)
    response = client.post("/identity/verify", json={"token": "any.token.here"})
    assert response.status_code == 503
    assert response.json()["detail"] == "identity service error"


def test_policy_approve_internal_failure() -> None:
    class BrokenGate(ApprovalGate):
        def resolve(self, *_args: object, **_kwargs: object) -> None:
            raise RuntimeError("gate broken")

    app = create_app()
    acp: AppState = app.state.acp
    acp.approval_gate = BrokenGate()
    pending = acp.approval_gate.request("x", {})
    test_client = TestClient(app)
    response = test_client.post(
        "/policy/approve",
        json={
            "approval_id": str(pending.id),
            "approved": True,
            "approver": "r",
        },
    )
    assert response.status_code == 503
    assert response.json()["reason"] == "approval resolution failed"


def test_governance_status_ok(client: TestClient) -> None:
    response = client.get("/governance/status")
    assert response.status_code == 200
    body = response.json()
    assert body["governance_version"] == "1.5.0"
    assert "mac_pilot_deploy_url" in body["practice_evidence"]
