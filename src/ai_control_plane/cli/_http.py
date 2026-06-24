"""Shared HTTP helpers for CLI → api/server.py calls (async I/O, sync entrypoints)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx

from ai_control_plane.api.schemas import (
    ApprovalResolveRequest,
    PolicyEvalRequest,
    PolicyEvalResponse,
    QuotaStatus,
    TaskRegisterRequest,
    TaskStatus,
)
from ai_control_plane.core.models import ApprovalDecision, TelemetryEvent

DEFAULT_API_URL = "http://localhost:8000"
API_TIMEOUT_SECONDS = 2.0


def api_base_url() -> str:
    return os.environ.get("ACP_API_URL", DEFAULT_API_URL)


def _client_headers(agent_id: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if agent_id:
        headers["X-Agent-Id"] = agent_id
    return headers


async def _post_policy_evaluate_async(request: PolicyEvalRequest) -> PolicyEvalResponse:
    """Call POST /policy/evaluate; fail-closed on transport errors."""
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.post(
                "/policy/evaluate",
                json=request.model_dump(mode="json"),
                headers=_client_headers(request.agent_id),
            )
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "policy service unavailable"
            raise RuntimeError(msg) from exc

        try:
            body = response.json()
            if not isinstance(body, dict):
                msg = "invalid policy response"
                raise TypeError(msg)
            return PolicyEvalResponse.model_validate(body)
        except (ValueError, TypeError) as exc:
            msg = "invalid policy response"
            raise RuntimeError(msg) from exc


def post_policy_evaluate(request: PolicyEvalRequest) -> PolicyEvalResponse:
    """Sync wrapper for Typer commands."""
    return asyncio.run(_post_policy_evaluate_async(request))


async def _get_project_status_async(project_id: str) -> TaskStatus:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.get(f"/status/{project_id}")
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "status service unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"status request failed ({response.status_code})"
            raise RuntimeError(msg)

        return TaskStatus.model_validate(response.json())


def get_project_status(project_id: str) -> TaskStatus:
    """Call GET /status/{project_id}."""
    return asyncio.run(_get_project_status_async(project_id))


async def _post_register_task_async(request: TaskRegisterRequest) -> TaskStatus:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.post(
                "/tasks",
                json=request.model_dump(mode="json"),
                headers=_client_headers(request.agent_id),
            )
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "task registration unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"task registration failed ({response.status_code})"
            raise RuntimeError(msg)

        return TaskStatus.model_validate(response.json())


def post_register_task(request: TaskRegisterRequest) -> TaskStatus:
    """Call POST /tasks to register an assigned task with the control plane."""
    return asyncio.run(_post_register_task_async(request))


async def _post_policy_approve_async(body: ApprovalResolveRequest) -> ApprovalDecision:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.post(
                "/policy/approve",
                json=body.model_dump(mode="json"),
            )
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "approval service unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"approval request failed ({response.status_code})"
            raise RuntimeError(msg)

        return ApprovalDecision.model_validate(response.json())


def post_policy_approve(body: ApprovalResolveRequest) -> ApprovalDecision:
    """Call POST /policy/approve."""
    return asyncio.run(_post_policy_approve_async(body))


async def _get_project_quota_async(project_id: str) -> QuotaStatus:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.get(f"/quota/{project_id}")
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "quota service unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"quota request failed ({response.status_code})"
            raise RuntimeError(msg)

        return QuotaStatus.model_validate(response.json())


def get_project_quota(project_id: str) -> QuotaStatus:
    """Call GET /quota/{project_id}."""
    return asyncio.run(_get_project_quota_async(project_id))


async def _get_telemetry_events_async(project_id: str | None = None) -> list[TelemetryEvent]:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        params = {"project_id": project_id} if project_id else None
        try:
            response = await client.get("/telemetry/events", params=params)
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "telemetry service unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"telemetry request failed ({response.status_code})"
            raise RuntimeError(msg)

        payload = response.json()
        if not isinstance(payload, list):
            msg = "invalid telemetry response"
            raise RuntimeError(msg)
        return [TelemetryEvent.model_validate(item) for item in payload]


def get_telemetry_events(project_id: str | None = None) -> list[TelemetryEvent]:
    """Call GET /telemetry/events."""
    return asyncio.run(_get_telemetry_events_async(project_id))


async def _get_apex_status_async() -> dict[str, Any]:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.get("/apex/status")
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "apex status unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"apex status failed ({response.status_code})"
            raise RuntimeError(msg)

        body = response.json()
        if not isinstance(body, dict):
            msg = "invalid apex status response"
            raise RuntimeError(msg)
        return body


def get_apex_status() -> dict[str, Any]:
    """Call GET /apex/status."""
    return asyncio.run(_get_apex_status_async())


async def _post_apex_trigger_async() -> dict[str, Any]:
    async with httpx.AsyncClient(base_url=api_base_url(), timeout=API_TIMEOUT_SECONDS) as client:
        try:
            response = await client.post("/apex/trigger")
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            msg = "apex trigger unavailable"
            raise RuntimeError(msg) from exc

        if response.status_code != 200:
            msg = f"apex trigger failed ({response.status_code})"
            raise RuntimeError(msg)

        body = response.json()
        if not isinstance(body, dict):
            msg = "invalid apex trigger response"
            raise RuntimeError(msg)
        return body


def post_apex_trigger() -> dict[str, Any]:
    """Call POST /apex/trigger."""
    return asyncio.run(_post_apex_trigger_async())


def format_json(data: dict[str, Any]) -> str:
    import json

    return json.dumps(data, indent=2, default=str)
