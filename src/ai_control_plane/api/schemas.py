"""HTTP request/response schemas for the TypeScript PolicyClient bridge."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ai_control_plane.core.models import (
    ApprovalDecision,
    ApprovalRequest,
    TaskStatus,
)

_HTTP = ConfigDict(extra="forbid")


class PolicyEvalRequest(BaseModel):
    """POST /policy/evaluate request body."""

    model_config = _HTTP

    agent_id: str
    project_id: str
    tool_name: str
    args: dict[str, Any] = Field(default_factory=dict)
    role: str | None = None


class PolicyEvalResponse(BaseModel):
    """POST /policy/evaluate response — fail-closed contract for PolicyClient."""

    model_config = _HTTP

    allowed: bool
    reason: str
    requires_approval: bool
    policy_id: str | None = None
    latency_ms: float


class TaskRequest(BaseModel):
    """Task submission payload."""

    model_config = _HTTP

    project_id: str
    agent_id: str
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskRegisterRequest(TaskRequest):
    """POST /tasks — register a task after policy approval."""

    task_id: UUID


class QuotaStatus(BaseModel):
    """GET /quota/{project_id} response."""

    model_config = _HTTP

    project_id: str
    tokens_used: float
    tokens_remaining: float
    requests_today: int


class ApprovalSubmitRequest(BaseModel):
    """HTTP wrapper to create an approval request."""

    model_config = _HTTP

    event_type: str
    context: dict[str, Any] = Field(default_factory=dict)

    def to_domain(self) -> ApprovalRequest:
        return ApprovalRequest(event_type=self.event_type, context=self.context)


class ApprovalSubmitResponse(BaseModel):
    """HTTP wrapper returning a domain ApprovalRequest."""

    model_config = _HTTP

    request: ApprovalRequest


class ApprovalResolveRequest(BaseModel):
    """POST /policy/approve request body."""

    model_config = _HTTP

    approval_id: str
    approved: bool
    approver: str


class IdentityVerifyRequest(BaseModel):
    """POST /identity/verify request body."""

    model_config = _HTTP

    agent_id: str
    project_id: str
    role: str | None = None
    jwt_claims: dict[str, Any] = Field(default_factory=dict)
    did: str | None = None


class ServiceUnavailableResponse(BaseModel):
    """503 payload — always deny; never default-allow."""

    model_config = _HTTP

    allowed: bool = False
    reason: str = "control plane unavailable"
    requires_approval: bool = False
    policy_id: str | None = None
    latency_ms: float = 0.0


class HealthResponse(BaseModel):
    """GET /health — config wire proof for operators and CI (#39)."""

    model_config = ConfigDict(extra="forbid")

    status: str
    config_loaded: bool
    policy_rules_count: int
    agents_loaded: list[str]
    projects_loaded: list[str]


__all__ = [
    "ApprovalDecision",
    "ApprovalRequest",
    "ApprovalResolveRequest",
    "ApprovalSubmitRequest",
    "ApprovalSubmitResponse",
    "HealthResponse",
    "IdentityVerifyRequest",
    "PolicyEvalRequest",
    "PolicyEvalResponse",
    "QuotaStatus",
    "ServiceUnavailableResponse",
    "TaskRegisterRequest",
    "TaskRequest",
    "TaskStatus",
]
