"""MCP Git facade tests — policy gate, forwarder, telemetry (S7, #12)."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import httpx
import pytest

from ai_control_plane.core.models import AgentIdentity, McpError, ProjectConfig
from ai_control_plane.core.telemetry import InMemoryTelemetryStore, TelemetryWriter
from ai_control_plane.mcp.git_server import (
    EVENT_TOOL_CALL,
    JSON_RPC_INTERNAL_ERROR,
    GitMcpServer,
    McpToolError,
)

POLICY_ALLOW_BODY = {
    "allowed": True,
    "reason": "action permitted",
    "requires_approval": False,
    "policy_id": None,
    "latency_ms": 1.0,
}

POLICY_DENY_BODY = {
    "allowed": False,
    "reason": "denied by policy",
    "requires_approval": False,
    "policy_id": "deny-rule",
    "latency_ms": 1.0,
}


class RecordingForwarder:
    """Capture forwarder invocations for assertions."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((tool_name, args))
        return {"content": [{"type": "text", "text": "ok"}]}


def _policy_transport(body: dict[str, Any]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/policy/evaluate"
        return httpx.Response(200, json=body)

    return httpx.MockTransport(handler)


@pytest.fixture
def mcp_project(sample_project_config: ProjectConfig) -> ProjectConfig:
    return sample_project_config


@pytest.fixture
def backend_mcp_identity(backend_identity: AgentIdentity) -> AgentIdentity:
    return backend_identity


@pytest.mark.asyncio
async def test_policy_deny_blocks_forwarder(
    mcp_project: ProjectConfig,
    backend_mcp_identity: AgentIdentity,
) -> None:
    forwarder = RecordingForwarder()
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_DENY_BODY),
        base_url="http://acp.test",
    ) as client:
        server = GitMcpServer(mcp_project, client, git_forwarder=forwarder)
        with pytest.raises(McpToolError) as exc_info:
            await server.handle_tool_call("git_status", {}, backend_mcp_identity)

    assert exc_info.value.error.code == JSON_RPC_INTERNAL_ERROR
    assert exc_info.value.error.message == "denied by policy"
    assert isinstance(exc_info.value.error, McpError)
    assert forwarder.calls == []


@pytest.mark.asyncio
async def test_policy_allow_calls_forwarder_and_emits_telemetry(
    mcp_project: ProjectConfig,
    backend_mcp_identity: AgentIdentity,
) -> None:
    forwarder = RecordingForwarder()
    store = InMemoryTelemetryStore()
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_ALLOW_BODY),
        base_url="http://acp.test",
    ) as client:
        server = GitMcpServer(mcp_project, client, git_forwarder=forwarder, store=store)
        result = await server.handle_tool_call("git_status", {}, backend_mcp_identity)

    assert result["content"]
    assert len(forwarder.calls) == 1
    tool_name, args = forwarder.calls[0]
    assert tool_name == "git_status"
    assert args["repo"] == mcp_project.repo
    assert args["project_id"] == mcp_project.id

    events = store.list_events()
    assert len(events) == 1
    assert events[0].event_type == EVENT_TOOL_CALL
    assert events[0].event_hash != ""
    assert store.verify_chain() is True


@pytest.mark.asyncio
async def test_telemetry_emit_failure_is_fail_silent(
    mcp_project: ProjectConfig,
    backend_mcp_identity: AgentIdentity,
) -> None:
    forwarder = RecordingForwarder()
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_ALLOW_BODY),
        base_url="http://acp.test",
    ) as client:
        server = GitMcpServer(mcp_project, client, git_forwarder=forwarder)
        with patch.object(TelemetryWriter, "emit", side_effect=RuntimeError("telemetry down")):
            result = await server.handle_tool_call("git_status", {}, backend_mcp_identity)

    assert result["content"]
    assert len(forwarder.calls) == 1
    assert server.telemetry_events == []


@pytest.mark.asyncio
async def test_policy_unavailable_raises_mcp_error(
    mcp_project: ProjectConfig,
    backend_mcp_identity: AgentIdentity,
) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"detail": "unavailable"})

    forwarder = RecordingForwarder()
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://acp.test",
    ) as client:
        server = GitMcpServer(mcp_project, client, git_forwarder=forwarder)
        with pytest.raises(McpToolError, match="policy_unavailable"):
            await server.handle_tool_call("git_status", {}, backend_mcp_identity)

    assert forwarder.calls == []


def test_list_tools_returns_git_definitions(mcp_project: ProjectConfig) -> None:
    server = GitMcpServer(mcp_project, httpx.AsyncClient(base_url="http://acp.test"))
    tools = server.list_tools()

    names = {tool["name"] for tool in tools}
    assert "git_status" in names
    assert "git_commit" in names


@pytest.mark.asyncio
async def test_requires_approval_blocks_forwarder(
    mcp_project: ProjectConfig,
    backend_mcp_identity: AgentIdentity,
) -> None:
    body = {
        **POLICY_ALLOW_BODY,
        "allowed": True,
        "requires_approval": True,
        "reason": "needs approval",
        "policy_id": "approval-gate",
    }
    forwarder = RecordingForwarder()
    async with httpx.AsyncClient(
        transport=_policy_transport(body),
        base_url="http://acp.test",
    ) as client:
        server = GitMcpServer(mcp_project, client, git_forwarder=forwarder)
        with pytest.raises(McpToolError, match="approval required"):
            await server.handle_tool_call("git_push", {}, backend_mcp_identity)

    assert forwarder.calls == []
