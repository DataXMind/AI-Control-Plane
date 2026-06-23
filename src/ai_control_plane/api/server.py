"""FastAPI HTTP bridge for TypeScript PolicyClient — fail-closed by design."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from ai_control_plane.api.schemas import (
    ApprovalResolveRequest,
    IdentityVerifyRequest,
    PolicyEvalRequest,
    PolicyEvalResponse,
    QuotaStatus,
    ServiceUnavailableResponse,
    TaskRegisterRequest,
    TaskStatus,
)
from ai_control_plane.config.loader import load_policies
from ai_control_plane.core.models import AgentIdentity, TaskState
from ai_control_plane.core.policies import ApprovalGate, PolicyEngine
from ai_control_plane.core.quota import InMemoryQuotaStore, TokenBudget

logger = logging.getLogger(__name__)
http_logger = logging.getLogger("ai_control_plane.http")

POLICY_EVAL_TIMEOUT_SECONDS = 2.0
SERVICE_UNAVAILABLE = 503

_DEFAULT_AGENT_REGISTRY: dict[str, dict[str, Any]] = {
    "agent1": {"role": "infra", "projects": ["rust-gateway"]},
    "agent2": {"role": "backend", "projects": ["rust-gateway"]},
    "agent3": {"role": "reviewer", "projects": ["rust-gateway", "datax-analytics"]},
}

_DEFAULT_PROJECT_LIMITS: dict[str, float] = {
    "rust-gateway": 2_000_000.0,
    "datax-analytics": 800_000.0,
}


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


def _deny_response(reason: str, *, latency_ms: float = 0.0) -> PolicyEvalResponse:
    return PolicyEvalResponse(
        allowed=False,
        reason=reason,
        requires_approval=False,
        policy_id=None,
        latency_ms=latency_ms,
    )


def _project_requests_key(project_id: str) -> str:
    return f"quota:project:{project_id}:requests_today"


def _project_tokens_key(project_id: str) -> str:
    return f"quota:project:{project_id}:tokens"


@dataclass
class AppState:
    """Application dependencies injected into route handlers."""

    policy_engine: PolicyEngine
    approval_gate: ApprovalGate
    token_budget: TokenBudget
    quota_store: InMemoryQuotaStore
    policy_rules_count: int = 0
    agent_registry: dict[str, dict[str, Any]] = field(
        default_factory=lambda: dict(_DEFAULT_AGENT_REGISTRY),
    )
    task_status_by_project: dict[str, TaskStatus] = field(default_factory=dict)
    project_limits: dict[str, float] = field(
        default_factory=lambda: dict(_DEFAULT_PROJECT_LIMITS),
    )


def build_policy_engine() -> PolicyEngine:
    """Load PolicyEngine rules from ACP_CONFIG_DIR or shipped config/policies.yml."""
    rules = load_policies()
    logger.info("policy_rules_loaded count=%d", len(rules))
    return PolicyEngine(rules=rules)


def build_default_app_state() -> AppState:
    """Construct default AppState with YAML-driven PolicyEngine (P0-2)."""
    quota_store = InMemoryQuotaStore()
    rules = load_policies()
    return AppState(
        policy_engine=PolicyEngine(rules=rules),
        approval_gate=ApprovalGate(),
        quota_store=quota_store,
        token_budget=TokenBudget(quota_store, _DEFAULT_PROJECT_LIMITS),
        policy_rules_count=len(rules),
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with agent_id and latency."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start = time.perf_counter()
        agent_id = request.headers.get("X-Agent-Id", "unknown")
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            latency_ms = (time.perf_counter() - start) * 1000.0
            http_logger.info(
                "http_request method=%s path=%s agent_id=%s status=%s latency_ms=%.2f",
                request.method,
                request.url.path,
                agent_id,
                response.status_code if response is not None else None,
                latency_ms,
            )


def _resolve_role(
    agent_id: str,
    role: str | None,
    registry: dict[str, dict[str, Any]],
) -> str | None:
    if role is not None:
        return role
    entry = registry.get(agent_id)
    if entry is None:
        return None
    value = entry.get("role")
    return str(value) if value is not None else None


def _agent_allowed_for_project(
    agent_id: str,
    project_id: str,
    registry: dict[str, dict[str, Any]],
) -> bool:
    entry = registry.get(agent_id)
    if entry is None:
        return False
    projects = entry.get("projects", [])
    if not isinstance(projects, list):
        return False
    return project_id in projects


def _default_task_status(project_id: str) -> TaskStatus:
    return TaskStatus(
        task_id=uuid4(),
        state=TaskState.PENDING,
        progress=0,
        updated_at=_utc_now(),
    )


def create_app(state: AppState | None = None) -> FastAPI:
    """Build the FastAPI application with fail-closed handlers."""
    app_state = build_default_app_state() if state is None else state

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        _ = app
        app.state.acp = app_state
        yield

    app = FastAPI(
        title="ai-control-plane",
        description="HTTP bridge for TypeScript PolicyClient",
        lifespan=lifespan,
    )
    app.state.acp = app_state
    app.add_middleware(RequestLoggingMiddleware)

    @app.exception_handler(RequestValidationError)
    async def validation_fail_closed(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        if request.url.path == "/policy/evaluate":
            body = _deny_response(f"invalid request: {exc.errors()}").model_dump(mode="json")
            return JSONResponse(status_code=SERVICE_UNAVAILABLE, content=body)
        return JSONResponse(
            status_code=SERVICE_UNAVAILABLE,
            content=ServiceUnavailableResponse(
                reason="invalid request",
            ).model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def unhandled_fail_closed(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_exception path=%s", request.url.path)
        if request.url.path == "/policy/evaluate":
            body = _deny_response("control plane unavailable").model_dump(mode="json")
            return JSONResponse(status_code=SERVICE_UNAVAILABLE, content=body)
        return JSONResponse(
            status_code=SERVICE_UNAVAILABLE,
            content=ServiceUnavailableResponse().model_dump(mode="json"),
        )

    @app.post("/policy/evaluate", response_model=PolicyEvalResponse)
    async def policy_evaluate(
        request: Request,
        body: PolicyEvalRequest,
    ) -> PolicyEvalResponse | JSONResponse:
        start = time.perf_counter()
        acp: AppState = request.app.state.acp

        role = _resolve_role(body.agent_id, body.role, acp.agent_registry)
        if role is None:
            latency_ms = (time.perf_counter() - start) * 1000.0
            return _deny_response("unknown agent or role", latency_ms=latency_ms)

        if not _agent_allowed_for_project(body.agent_id, body.project_id, acp.agent_registry):
            latency_ms = (time.perf_counter() - start) * 1000.0
            return _deny_response(
                f"agent '{body.agent_id}' not authorized for project '{body.project_id}'",
                latency_ms=latency_ms,
            )

        identity = AgentIdentity(
            agent_id=body.agent_id,
            project_id=body.project_id,
            role=role,
            jwt_claims=dict(body.args.get("jwt_claims", {})),
            did=None,
        )

        try:
            decision = await asyncio.wait_for(
                asyncio.to_thread(
                    acp.policy_engine.evaluate,
                    identity,
                    body.tool_name,
                    body.args,
                    body.project_id,
                ),
                timeout=POLICY_EVAL_TIMEOUT_SECONDS,
            )
        except TimeoutError:
            latency_ms = (time.perf_counter() - start) * 1000.0
            logger.error(
                "policy_evaluate_timeout agent_id=%s project_id=%s tool=%s latency_ms=%.2f",
                body.agent_id,
                body.project_id,
                body.tool_name,
                latency_ms,
            )
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=_deny_response(
                    "policy evaluation timed out",
                    latency_ms=latency_ms,
                ).model_dump(mode="json"),
            )
        except Exception:
            latency_ms = (time.perf_counter() - start) * 1000.0
            logger.exception("policy_evaluate_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=_deny_response(
                    "policy evaluation failed",
                    latency_ms=latency_ms,
                ).model_dump(mode="json"),
            )

        latency_ms = (time.perf_counter() - start) * 1000.0
        return PolicyEvalResponse(
            allowed=decision.allowed,
            reason=decision.reason,
            requires_approval=decision.requires_approval,
            policy_id=decision.policy_id,
            latency_ms=round(latency_ms, 2),
        )

    @app.post("/policy/approve")
    async def policy_approve(
        request: Request,
        body: ApprovalResolveRequest,
    ) -> JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            decision = acp.approval_gate.resolve(
                body.approval_id,
                body.approved,
                body.approver,
            )
            return JSONResponse(
                status_code=200,
                content=decision.model_dump(mode="json"),
            )
        except Exception:
            logger.exception("policy_approve_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="approval resolution failed",
                ).model_dump(mode="json"),
            )

    @app.post("/identity/verify")
    async def identity_verify(
        request: Request,
        body: IdentityVerifyRequest,
    ) -> JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            role = _resolve_role(body.agent_id, body.role, acp.agent_registry)
            if role is None or not _agent_allowed_for_project(
                body.agent_id,
                body.project_id,
                acp.agent_registry,
            ):
                return JSONResponse(
                    status_code=SERVICE_UNAVAILABLE,
                    content=ServiceUnavailableResponse(
                        reason="identity verification failed",
                    ).model_dump(mode="json"),
                )

            identity = AgentIdentity(
                agent_id=body.agent_id,
                project_id=body.project_id,
                role=role,
                jwt_claims=body.jwt_claims,
                did=body.did,
            )
            return JSONResponse(status_code=200, content=identity.model_dump(mode="json"))
        except Exception:
            logger.exception("identity_verify_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="identity verification failed",
                ).model_dump(mode="json"),
            )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/tasks", response_model=TaskStatus)
    async def register_task(
        request: Request,
        body: TaskRegisterRequest,
    ) -> TaskStatus | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            if body.project_id not in acp.project_limits:
                return JSONResponse(
                    status_code=SERVICE_UNAVAILABLE,
                    content=ServiceUnavailableResponse(
                        reason=f"unknown project '{body.project_id}'",
                    ).model_dump(mode="json"),
                )
            status = TaskStatus(
                task_id=body.task_id,
                state=TaskState.PENDING,
                progress=0,
                updated_at=_utc_now(),
            )
            acp.task_status_by_project[body.project_id] = status
            return status
        except Exception:
            logger.exception("register_task_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="task registration failed",
                ).model_dump(mode="json"),
            )

    @app.get("/status/{project_id}", response_model=TaskStatus)
    async def project_status(request: Request, project_id: str) -> TaskStatus | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            status = acp.task_status_by_project.get(project_id)
            if status is None:
                status = _default_task_status(project_id)
                acp.task_status_by_project[project_id] = status
            return status
        except Exception:
            logger.exception("project_status_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="status unavailable",
                ).model_dump(mode="json"),
            )

    @app.get("/quota/{project_id}", response_model=QuotaStatus)
    async def project_quota(request: Request, project_id: str) -> QuotaStatus | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            limit = acp.project_limits.get(project_id)
            if limit is None:
                return JSONResponse(
                    status_code=SERVICE_UNAVAILABLE,
                    content=ServiceUnavailableResponse(
                        reason=f"unknown project '{project_id}'",
                    ).model_dump(mode="json"),
                )

            tokens_used = acp.quota_store.get(_project_tokens_key(project_id))
            tokens_remaining = max(0.0, limit - tokens_used)

            requests_today = int(acp.quota_store.get(_project_requests_key(project_id)))
            return QuotaStatus(
                project_id=project_id,
                tokens_used=tokens_used,
                tokens_remaining=tokens_remaining,
                requests_today=requests_today,
            )
        except Exception:
            logger.exception("project_quota_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="quota unavailable",
                ).model_dump(mode="json"),
            )

    return app


app = create_app()
