"""API integration tests — config wiring and fail-closed policy (P0-2, P0-4)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app


def test_create_app_loads_policy_rules_from_config() -> None:
    app = create_app()
    assert app.state.acp.policy_rules_count > 0
    assert app.state.acp.config_loaded is True


def test_health_reports_config_wire_proof() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["config_loaded"] is True
    assert body["policy_rules_count"] > 0
    assert "agent2" in body["agents_loaded"]
    assert "rust-gateway" in body["projects_loaded"]


def test_policy_evaluate_backend_git_read_allowed() -> None:
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
    body = response.json()
    assert body["allowed"] is True


def test_policy_evaluate_backend_k8s_apply_denied() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "agent2",
            "project_id": "rust-gateway",
            "tool_name": "k8s_apply_prod",
            "role": "backend",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False


def test_policy_evaluate_unknown_agent_fail_closed() -> None:
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
    body = response.json()
    assert body["allowed"] is False


def test_quota_reflects_configured_project_limit() -> None:
    client = TestClient(create_app())
    response = client.get("/quota/rust-gateway")
    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "rust-gateway"
    assert body["tokens_remaining"] >= 100_000
