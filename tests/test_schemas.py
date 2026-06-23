"""API schema unification tests — S5: core.models owns TaskStatus (Invariant #2)."""

from __future__ import annotations

from ai_control_plane.api import schemas as api_schemas
from ai_control_plane.core import models as core_models


def test_task_status_is_imported_from_core_models() -> None:
    assert api_schemas.TaskStatus is core_models.TaskStatus


def test_approval_types_are_imported_from_core_models() -> None:
    assert api_schemas.ApprovalDecision is core_models.ApprovalDecision
    assert api_schemas.ApprovalRequest is core_models.ApprovalRequest
