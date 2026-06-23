"""API integration tests — PolicyEngine wired from config at startup (P0-2)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app


def test_create_app_loads_policy_rules_from_config() -> None:
    app = create_app()
    assert app.state.acp.policy_rules_count > 0


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
