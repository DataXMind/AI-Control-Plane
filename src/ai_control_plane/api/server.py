"""FastAPI HTTP bridge for TypeScript PolicyClient — fail-closed by design."""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import structlog
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from ai_control_plane.api.schemas import (
    ApprovalResolveRequest,
    HealthResponse,
    IdentityVerifyRequest,
    PolicyEvalRequest,
    PolicyEvalResponse,
    QuotaStatus,
    ServiceUnavailableResponse,
    TaskRegisterRequest,
    TaskStatus,
)
from ai_control_plane.config.loader import (
    build_agent_registry,
    get_config_dir,
    load_guardrails,
    load_kill_switch,
    load_policies,
    load_project_token_limits,
    load_projects,
)
from ai_control_plane.core.exceptions import ApprovalError, ConfigError, ControlPlaneError
from ai_control_plane.core.identity import JWTValidationError, JWTValidator
from ai_control_plane.core.models import AgentIdentity, PolicyRule, TaskState
from ai_control_plane.core.policies import ApprovalGate, PolicyEngine
from ai_control_plane.core.quota import InMemoryQuotaStore, TokenBudget
from ai_control_plane.core.telemetry import InMemoryTelemetryStore
from ai_control_plane.core.tool_names import resolve_policy_tool_name

logger = structlog.get_logger(__name__)
http_logger = structlog.get_logger("ai_control_plane.http")

POLICY_EVAL_TIMEOUT_SECONDS = 2.0
SERVICE_UNAVAILABLE = 503


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
    config_loaded: bool = False
    agents_loaded: list[str] = field(default_factory=list)
    projects_loaded: list[str] = field(default_factory=list)
    agent_registry: dict[str, dict[str, Any]] = field(default_factory=dict)
    task_status_by_project: dict[str, TaskStatus] = field(default_factory=dict)
    project_limits: dict[str, float] = field(default_factory=dict)
    telemetry_store: InMemoryTelemetryStore = field(default_factory=InMemoryTelemetryStore)
    jwt_validator: JWTValidator = field(default_factory=JWTValidator)


def _load_policy_rules() -> list[PolicyRule]:
    """Load RBAC/ABAC + guardrail rules from policies.yml."""
    policies_path = get_config_dir() / "policies.yml"
    return load_policies(policies_path) + load_guardrails(policies_path)


def build_policy_engine() -> PolicyEngine:
    """Load PolicyEngine rules from ACP_CONFIG_DIR or shipped config/policies.yml."""
    policies_path = get_config_dir() / "policies.yml"
    all_rules = _load_policy_rules()
    kill_switch = load_kill_switch(policies_path)
    logger.info("policy_rules_loaded", count=len(all_rules))
    return PolicyEngine(rules=all_rules, kill_switch=kill_switch)


def build_default_app_state() -> AppState:
    """Construct default AppState from ACP_CONFIG_DIR YAML (P0-2, P0-4)."""
    quota_store = InMemoryQuotaStore()
    telemetry_store = InMemoryTelemetryStore()
    policies_path = get_config_dir() / "policies.yml"
    all_rules = _load_policy_rules()
    kill_switch = load_kill_switch(policies_path)
    agent_registry = build_agent_registry()
    projects = load_projects()
    project_limits = load_project_token_limits()

    if not projects:
        raise ConfigError("no projects loaded from projects.yml")

    return AppState(
        policy_engine=PolicyEngine(rules=all_rules, kill_switch=kill_switch),
        approval_gate=ApprovalGate(),
        quota_store=quota_store,
        token_budget=TokenBudget(quota_store, project_limits),
        policy_rules_count=len(all_rules),
        config_loaded=True,
        agents_loaded=sorted(agent_registry.keys()),
        projects_loaded=sorted(projects.keys()),
        agent_registry=agent_registry,
        project_limits=project_limits,
        telemetry_store=telemetry_store,
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
                "http_request",
                method=request.method,
                path=request.url.path,
                agent_id=agent_id,
                status=response.status_code if response is not None else None,
                latency_ms=round(latency_ms, 2),
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

    @app.exception_handler(ControlPlaneError)
    async def control_plane_fail_closed(
        request: Request,
        exc: ControlPlaneError,
    ) -> JSONResponse:
        logger.warning("control_plane_error", path=request.url.path, error=str(exc))
        if request.url.path == "/policy/evaluate":
            body = _deny_response(str(exc)).model_dump(mode="json")
            return JSONResponse(status_code=SERVICE_UNAVAILABLE, content=body)
        return JSONResponse(
            status_code=SERVICE_UNAVAILABLE,
            content=ServiceUnavailableResponse(reason=str(exc)).model_dump(mode="json"),
        )

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
        logger.exception("unhandled_exception", path=request.url.path)
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

        policy_tool_name = resolve_policy_tool_name(body.tool_name)

        try:
            decision = await asyncio.wait_for(
                asyncio.to_thread(
                    acp.policy_engine.evaluate,
                    identity,
                    policy_tool_name,
                    body.args,
                    body.project_id,
                ),
                timeout=POLICY_EVAL_TIMEOUT_SECONDS,
            )
        except TimeoutError:
            latency_ms = (time.perf_counter() - start) * 1000.0
            logger.error(
                "policy_evaluate_timeout",
                agent_id=body.agent_id,
                project_id=body.project_id,
                tool=body.tool_name,
                latency_ms=round(latency_ms, 2),
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
        except Exception as exc:
            logger.exception("policy_approve_failed")
            reason = (
                str(exc)
                if isinstance(exc, ApprovalError)
                else "approval resolution failed"
            )
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(reason=reason).model_dump(mode="json"),
            )

    @app.post("/identity/verify", response_model=AgentIdentity)
    async def identity_verify(
        request: Request,
        body: IdentityVerifyRequest,
    ) -> AgentIdentity:
        acp: AppState = request.app.state.acp
        try:
            claims = acp.jwt_validator.validate(body.token)
            agent_id_raw = claims.get("agent_id") or claims.get("sub")
            if not agent_id_raw:
                raise HTTPException(status_code=401, detail="missing agent_id claim")
            agent_id = str(agent_id_raw)

            agent_entry = acp.agent_registry.get(agent_id)
            if agent_entry is None:
                raise HTTPException(status_code=401, detail="agent_not_found")

            project_id = str(claims.get("project_id", ""))
            if not project_id or not _agent_allowed_for_project(
                agent_id,
                project_id,
                acp.agent_registry,
            ):
                raise HTTPException(status_code=401, detail="agent_not_found")

            role_raw = claims.get("role") or agent_entry.get("role")
            if role_raw is None:
                raise HTTPException(status_code=401, detail="missing role claim")
            role = str(role_raw)

            return AgentIdentity(
                agent_id=agent_id,
                project_id=project_id,
                role=role,
                jwt_claims=claims,
                did=claims.get("did") if claims.get("did") is not None else None,
            )
        except JWTValidationError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("identity_verify_error", error=str(exc))
            raise HTTPException(status_code=503, detail="identity service error") from exc

    @app.get("/health", response_model=HealthResponse)
    async def health(request: Request) -> HealthResponse:
        acp: AppState = request.app.state.acp
        return HealthResponse(
            status="ok",
            config_loaded=acp.config_loaded,
            policy_rules_count=acp.policy_rules_count,
            agents_loaded=acp.agents_loaded,
            projects_loaded=acp.projects_loaded,
        )

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
