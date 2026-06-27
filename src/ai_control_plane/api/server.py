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

from ai_control_plane.apex.pipeline import run_sapal_pipeline
from ai_control_plane.api.schemas import (
    AgentQuotaStatus,
    ApprovalResolveRequest,
    GovernanceCaseStudy,
    GovernanceKnownGap,
    GovernanceStatusResponse,
    HealthResponse,
    IdentityVerifyRequest,
    LessonPattern,
    ModelProfileQuotaStatus,
    PolicyEvalRequest,
    PolicyEvalResponse,
    PracticeEvidenceSummary,
    PublicBetaSummary,
    QuotaStatus,
    ServiceUnavailableResponse,
    TaskRegisterRequest,
    TaskStatus,
)
from ai_control_plane.config.loader import (
    build_agent_registry,
    get_config_dir,
    load_agent_token_limits,
    load_guardrails,
    load_kill_switch,
    load_model_profile_token_limits,
    load_model_profiles,
    load_policies,
    load_project_token_limits,
    load_projects,
)
from ai_control_plane.core.exceptions import ApprovalError, ConfigError, ControlPlaneError
from ai_control_plane.core.governance_catalog import (
    CASE_STUDIES,
    DOC_LINKS,
    GOVERNANCE_FRAMEWORK,
    GOVERNANCE_VERSION,
    KNOWN_GAPS,
    LAYER_SUMMARY,
    LESSON_PATTERNS,
    MILESTONE_STATUS,
    PRACTICE_EVIDENCE,
    PUBLIC_BETA,
    VERIFY_GATE_COMMANDS,
)
from ai_control_plane.core.identity import JWTValidationError, TokenValidator, create_jwt_validator
from ai_control_plane.core.models import (
    AgentIdentity,
    ModelProfile,
    PolicyRule,
    TaskState,
    TelemetryEvent,
)
from ai_control_plane.core.policies import ApprovalGate, PolicyEngine
from ai_control_plane.core.quota import (
    ProfileQuotaTracker,
    QuotaStore,
    QuotaTracker,
    TokenBudget,
    create_quota_store,
)
from ai_control_plane.core.registry import (
    ActionRegistryLike,
    create_action_registry,
    seed_registry_from_rules,
)
from ai_control_plane.core.task_store import TaskStore, create_task_store
from ai_control_plane.core.telemetry import TelemetryStore, create_telemetry_store
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
    quota_store: QuotaStore
    quota_tracker: QuotaTracker
    profile_quota_tracker: ProfileQuotaTracker
    action_registry: ActionRegistryLike
    policy_rules_count: int = 0
    config_loaded: bool = False
    agents_loaded: list[str] = field(default_factory=list)
    projects_loaded: list[str] = field(default_factory=list)
    agent_registry: dict[str, dict[str, Any]] = field(default_factory=dict)
    model_profiles: dict[str, ModelProfile] = field(default_factory=dict)
    task_store: TaskStore = field(default_factory=create_task_store)
    project_limits: dict[str, float] = field(default_factory=dict)
    agent_limits: dict[str, float] = field(default_factory=dict)
    model_profile_limits: dict[str, float] = field(default_factory=dict)
    telemetry_store: TelemetryStore = field(default_factory=create_telemetry_store)
    jwt_validator: TokenValidator = field(default_factory=create_jwt_validator)
    sapal_last_result: dict[str, Any] | None = None


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


def _validate_agent_model_profiles(
    agent_registry: dict[str, dict[str, Any]],
    model_profiles: dict[str, ModelProfile],
) -> None:
    """Ensure every agent references a loaded model profile (#9 / GAP-S4-1)."""
    for agent_id, meta in agent_registry.items():
        profile_name = str(meta.get("model_profile", ""))
        if not profile_name:
            continue
        if profile_name not in model_profiles:
            msg = (
                f"agent '{agent_id}' references unknown model_profile "
                f"'{profile_name}' — check agents.yml model_profiles section"
            )
            raise ConfigError(msg)


def build_default_app_state() -> AppState:
    """Construct default AppState from ACP_CONFIG_DIR YAML (P0-2, P0-4)."""
    quota_store = create_quota_store()
    telemetry_store = create_telemetry_store()
    policies_path = get_config_dir() / "policies.yml"
    all_rules = _load_policy_rules()
    kill_switch = load_kill_switch(policies_path)
    agent_registry = build_agent_registry()
    model_profiles = load_model_profiles()
    _validate_agent_model_profiles(agent_registry, model_profiles)
    projects = load_projects()
    project_limits = load_project_token_limits()
    agent_limits = load_agent_token_limits()
    model_profile_limits = load_model_profile_token_limits()
    action_registry = create_action_registry()
    seed_registry_from_rules(action_registry, all_rules)

    if not projects:
        raise ConfigError("no projects loaded from projects.yml")

    return AppState(
        policy_engine=PolicyEngine(rules=all_rules, kill_switch=kill_switch),
        approval_gate=ApprovalGate(),
        quota_store=quota_store,
        quota_tracker=QuotaTracker(quota_store, agent_limits),
        profile_quota_tracker=ProfileQuotaTracker(quota_store, model_profile_limits),
        action_registry=action_registry,
        token_budget=TokenBudget(quota_store, project_limits),
        policy_rules_count=len(all_rules),
        config_loaded=True,
        agents_loaded=sorted(agent_registry.keys()),
        projects_loaded=sorted(projects.keys()),
        agent_registry=agent_registry,
        model_profiles=model_profiles,
        project_limits=project_limits,
        agent_limits=agent_limits,
        model_profile_limits=model_profile_limits,
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
            reason = str(exc) if isinstance(exc, ApprovalError) else "approval resolution failed"
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
            model_profiles_loaded=sorted(acp.model_profiles.keys()),
        )

    @app.get("/governance/status", response_model=GovernanceStatusResponse)
    async def governance_status(request: Request) -> GovernanceStatusResponse:
        """Governance UX runtime — 6-layer status, case studies, verify gate."""
        acp: AppState = request.app.state.acp
        studies = [GovernanceCaseStudy.model_validate(cs) for cs in CASE_STUDIES]
        gaps = [GovernanceKnownGap.model_validate(g) for g in KNOWN_GAPS]
        patterns = [LessonPattern.model_validate(p) for p in LESSON_PATTERNS]
        practice = PracticeEvidenceSummary.model_validate(PRACTICE_EVIDENCE)
        return GovernanceStatusResponse(
            status="ok",
            framework=GOVERNANCE_FRAMEWORK,
            governance_version=GOVERNANCE_VERSION,
            config_loaded=acp.config_loaded,
            policy_rules_count=acp.policy_rules_count,
            milestones=dict(MILESTONE_STATUS),
            layers=dict(LAYER_SUMMARY),
            verify_gate=list(VERIFY_GATE_COMMANDS),
            doc_links=dict(DOC_LINKS),
            public_beta=PublicBetaSummary.model_validate(PUBLIC_BETA),
            case_studies=studies,
            known_gaps=gaps,
            lessons_patterns=patterns,
            practice_evidence=practice,
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
            acp.task_store.set(body.project_id, status)
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
            status = acp.task_store.get(project_id)
            if status is None:
                status = _default_task_status(project_id)
                acp.task_store.set(project_id, status)
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

    @app.get("/quota/agent/{agent_id}", response_model=AgentQuotaStatus)
    async def agent_quota(request: Request, agent_id: str) -> AgentQuotaStatus | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            limit = acp.agent_limits.get(agent_id)
            if limit is None:
                return JSONResponse(
                    status_code=SERVICE_UNAVAILABLE,
                    content=ServiceUnavailableResponse(
                        reason=f"unknown agent '{agent_id}'",
                    ).model_dump(mode="json"),
                )

            tokens_remaining = acp.quota_tracker.remaining(agent_id)
            tokens_used = max(0.0, limit - tokens_remaining)
            return AgentQuotaStatus(
                agent_id=agent_id,
                tokens_used=tokens_used,
                tokens_remaining=tokens_remaining,
            )
        except Exception:
            logger.exception("agent_quota_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="quota unavailable",
                ).model_dump(mode="json"),
            )

    @app.get("/quota/profile/{profile_id}", response_model=ModelProfileQuotaStatus)
    async def profile_quota(
        request: Request,
        profile_id: str,
    ) -> ModelProfileQuotaStatus | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            limit = acp.model_profile_limits.get(profile_id)
            if limit is None:
                return JSONResponse(
                    status_code=SERVICE_UNAVAILABLE,
                    content=ServiceUnavailableResponse(
                        reason=f"unknown model profile '{profile_id}'",
                    ).model_dump(mode="json"),
                )

            tokens_remaining = acp.profile_quota_tracker.remaining(profile_id)
            tokens_used = max(0.0, limit - tokens_remaining)
            return ModelProfileQuotaStatus(
                model_profile=profile_id,
                tokens_used=tokens_used,
                tokens_remaining=tokens_remaining,
            )
        except Exception:
            logger.exception("profile_quota_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="quota unavailable",
                ).model_dump(mode="json"),
            )

    @app.get("/telemetry/events", response_model=list[TelemetryEvent])
    async def list_telemetry_events(
        request: Request,
        project_id: str | None = None,
    ) -> list[TelemetryEvent] | JSONResponse:
        acp: AppState = request.app.state.acp
        try:
            events = acp.telemetry_store.list_events()
            if project_id is not None:
                events = [event for event in events if event.project_id == project_id]
            return events
        except Exception:
            logger.exception("telemetry_list_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="telemetry unavailable",
                ).model_dump(mode="json"),
            )

    @app.get("/apex/status", response_model=None)
    async def apex_status(request: Request) -> JSONResponse | dict[str, Any]:
        acp: AppState = request.app.state.acp
        try:
            events = acp.telemetry_store.list_events()
            return {
                "telemetry_event_count": len(events),
                "telemetry_chain_valid": acp.telemetry_store.verify_chain(),
                "last_cycle": acp.sapal_last_result,
            }
        except Exception:
            logger.exception("apex_status_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="apex status unavailable",
                ).model_dump(mode="json"),
            )

    @app.post("/apex/trigger", response_model=None)
    async def apex_trigger(request: Request) -> JSONResponse | dict[str, Any]:
        acp: AppState = request.app.state.acp
        try:
            result = await asyncio.to_thread(
                run_sapal_pipeline,
                acp.telemetry_store,
                {},
            )
            acp.sapal_last_result = result
            return result
        except Exception:
            logger.exception("apex_trigger_failed")
            return JSONResponse(
                status_code=SERVICE_UNAVAILABLE,
                content=ServiceUnavailableResponse(
                    reason="apex trigger failed",
                ).model_dump(mode="json"),
            )

    return app


app = create_app()
