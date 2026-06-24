"""API task persistence — survives process restart when ACP_DATA_DIR set (#36)."""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app


def test_task_persistence_across_app_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ACP_DATA_DIR", str(tmp_path))
    task_id = str(uuid4())

    client1 = TestClient(create_app())
    response = client1.post(
        "/tasks",
        json={
            "project_id": "rust-gateway",
            "agent_id": "agent2",
            "task_type": "assign",
            "task_id": task_id,
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id

    client2 = TestClient(create_app())
    status = client2.get("/status/rust-gateway")
    assert status.status_code == 200
    assert status.json()["task_id"] == task_id
