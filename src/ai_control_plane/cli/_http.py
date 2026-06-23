"""Shared HTTP helpers for CLI → api/server.py calls (async I/O, sync entrypoints)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx

from ai_control_plane.api.schemas import (
    PolicyEvalRequest,
    PolicyEvalResponse,
    TaskRegisterRequest,
    TaskStatus,
)

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


def format_json(data: dict[str, Any]) -> str:
    import json

    return json.dumps(data, indent=2, default=str)
