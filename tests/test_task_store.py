"""Task store unit tests — file persistence (#36)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from ai_control_plane.core.models import TaskState, TaskStatus
from ai_control_plane.core.task_store import FileTaskStore, InMemoryTaskStore


def _sample_status(project_id: str = "rust-gateway") -> TaskStatus:
    return TaskStatus(
        task_id=uuid4(),
        state=TaskState.PENDING,
        progress=0,
        updated_at=datetime.now(tz=UTC),
    )


def test_in_memory_task_store_round_trip() -> None:
    store = InMemoryTaskStore()
    status = _sample_status()
    store.set("rust-gateway", status)
    loaded = store.get("rust-gateway")
    assert loaded is not None
    assert loaded.task_id == status.task_id
    assert loaded.state == TaskState.PENDING


def test_file_task_store_survives_new_instance(tmp_path) -> None:
    root = tmp_path / "tasks"
    status = _sample_status()
    store1 = FileTaskStore(root)
    store1.set("rust-gateway", status)

    store2 = FileTaskStore(root)
    loaded = store2.get("rust-gateway")
    assert loaded is not None
    assert loaded.task_id == status.task_id


def test_file_task_store_delete(tmp_path) -> None:
    store = FileTaskStore(tmp_path / "tasks")
    store.set("p1", _sample_status())
    store.delete("p1")
    assert store.get("p1") is None
