"""All control-plane data contracts — single source of truth for types."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

_FROZEN = ConfigDict(frozen=True)


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


class TaskState(StrEnum):
    """Lifecycle state for a task."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"


class ProjectConfig(BaseModel):
    """Registered project with repo, environments, and role bindings."""

    model_config = _FROZEN

    id: str
    repo: str
    default_branch: str
    environments: dict[str, dict[str, Any]]
    roles: dict[str, dict[str, Any]]
    docs: dict[str, Any]


class AgentConfig(BaseModel):
    """Agent identity binding: runner, roles, and model profile."""

    model_config = _FROZEN

    id: str
    name: str
    roles: list[str]
    runner: str
    model_profile: str
    capabilities: list[str]
    restrictions: list[str]


class ModelProfile(BaseModel):
    """LLM provider account and per-day token budget."""

    model_config = _FROZEN

    name: str
    provider: str
    account_type: str
    api_key_env: str
    max_tokens_per_day: int
    allowed_tasks: list[str]


class PolicyRule(BaseModel):
    """ABAC/RBAC rule with conditions and allow/deny effect."""

    model_config = _FROZEN

    name: str
    description: str
    conditions: dict[str, Any]
    effect: Literal["allow", "deny"]


class Task(BaseModel):
    """Unit of work assigned to an agent within a project."""

    model_config = _FROZEN

    id: UUID = Field(default_factory=uuid4)
    project_id: str
    agent_id: str
    task_type: str
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=_utc_now)


class TaskStatus(BaseModel):
    """Current execution state of a task."""

    model_config = _FROZEN

    task_id: UUID
    state: TaskState
    updated_at: datetime = Field(default_factory=_utc_now)


class PolicyDecision(BaseModel):
    """Result of policy evaluation for TypeScript PolicyClient."""

    model_config = _FROZEN

    allowed: bool
    reason: str
    requires_approval: bool
    policy_id: Optional[str] = None  # noqa: UP045


class AgentIdentity(BaseModel):
    """Verified agent identity for cross-language policy checks."""

    model_config = _FROZEN

    agent_id: str
    project_id: str
    role: str
    jwt_claims: dict[str, Any]
    did: Union[str, None] = None  # noqa: UP007


class ApprovalRequest(BaseModel):
    """Human-in-the-loop approval request for a gated action."""

    model_config = _FROZEN

    id: UUID = Field(default_factory=uuid4)
    event_type: str
    context: dict[str, Any]
    created_at: datetime = Field(default_factory=_utc_now)


class ApprovalDecision(BaseModel):
    """Recorded outcome of an approval request."""

    model_config = _FROZEN

    request_id: UUID
    approved: bool
    approver: str
    decided_at: datetime = Field(default_factory=_utc_now)


class TelemetryEvent(BaseModel):
    """Append-only audit/telemetry record."""

    model_config = _FROZEN

    id: UUID = Field(default_factory=uuid4)
    event_type: str
    agent_id: str
    project_id: str
    payload: dict[str, Any]
    timestamp: datetime = Field(default_factory=_utc_now)


class McpError(BaseModel):
    """JSON-RPC style error envelope for MCP tool failures."""

    model_config = _FROZEN

    code: int
    message: str
    data: Union[dict[str, Any], None] = None  # noqa: UP007


__all__ = [
    "AgentConfig",
    "AgentIdentity",
    "ApprovalDecision",
    "ApprovalRequest",
    "McpError",
    "ModelProfile",
    "PolicyDecision",
    "PolicyRule",
    "ProjectConfig",
    "Task",
    "TaskState",
    "TaskStatus",
    "TelemetryEvent",
]
