"""API contract snapshots — L4 governance (see docs/CONTRACT_TESTS.md)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ai_control_plane.api.schemas import HealthResponse, PolicyEvalResponse
from ai_control_plane.api.server import create_app

_HEALTH_FIELDS = frozenset(HealthResponse.model_fields.keys())
_POLICY_EVAL_FIELDS = frozenset(PolicyEvalResponse.model_fields.keys())


def test_health_response_schema_keys() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert frozenset(body.keys()) == _HEALTH_FIELDS


def test_policy_evaluate_deny_schema_keys() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/policy/evaluate",
        json={
            "agent_id": "unknown-agent-xyz",
            "project_id": "rust-gateway",
            "tool_name": "git_read",
            "role": "backend",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert body["reason"]
    assert frozenset(body.keys()) == _POLICY_EVAL_FIELDS
