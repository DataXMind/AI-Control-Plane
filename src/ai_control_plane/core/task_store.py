"""Task status persistence — swappable store (file or in-memory)."""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Protocol, runtime_checkable

from ai_control_plane.core.models import TaskStatus


@runtime_checkable
class TaskStore(Protocol):
    """Persist project-scoped task status across API restarts."""

    def get(self, project_id: str) -> TaskStatus | None:
        ...

    def set(self, project_id: str, status: TaskStatus) -> None:
        ...

    def delete(self, project_id: str) -> None:
        ...


class InMemoryTaskStore:
    """Default Milestone A store — lost on process exit."""

    def __init__(self) -> None:
        self._data: dict[str, TaskStatus] = {}
        self._lock = threading.Lock()

    def get(self, project_id: str) -> TaskStatus | None:
        with self._lock:
            stored = self._data.get(project_id)
            return stored.model_copy(deep=True) if stored is not None else None

    def set(self, project_id: str, status: TaskStatus) -> None:
        with self._lock:
            self._data[project_id] = status.model_copy(deep=True)

    def delete(self, project_id: str) -> None:
        with self._lock:
            self._data.pop(project_id, None)


class FileTaskStore:
    """JSON file per project under ``ACP_DATA_DIR/tasks/``."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _path(self, project_id: str) -> Path:
        safe_id = project_id.replace("/", "_")
        return self._root / f"{safe_id}.json"

    def get(self, project_id: str) -> TaskStatus | None:
        path = self._path(project_id)
        with self._lock:
            if not path.exists():
                return None
            raw = json.loads(path.read_text(encoding="utf-8"))
            return TaskStatus.model_validate(raw)

    def set(self, project_id: str, status: TaskStatus) -> None:
        path = self._path(project_id)
        with self._lock:
            path.write_text(
                status.model_dump_json(indent=2),
                encoding="utf-8",
            )

    def delete(self, project_id: str) -> None:
        path = self._path(project_id)
        with self._lock:
            if path.exists():
                path.unlink()


def create_task_store() -> TaskStore:
    """File store when ``ACP_DATA_DIR`` is set; otherwise in-memory."""
    data_dir = os.environ.get("ACP_DATA_DIR")
    if data_dir:
        return FileTaskStore(Path(data_dir) / "tasks")
    return InMemoryTaskStore()


__all__ = [
    "FileTaskStore",
    "InMemoryTaskStore",
    "TaskStore",
    "create_task_store",
]
