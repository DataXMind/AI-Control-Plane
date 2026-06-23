"""MCP → real PolicyEngine via ASGI (no mocked policy HTTP)."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from httpx import ASGITransport

from ai_control_plane.core.models import AgentIdentity, McpError
from ai_control_plane.mcp.git_server import GitMcpServer, McpToolError


class RecordingForwarder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((tool_name, args))
        return {"content": [{"type": "text", "text": "ok"}]}


@pytest.fixture
def backend_mcp_identity() -> AgentIdentity:
    return AgentIdentity(
        agent_id="agent2",
        project_id="rust-gateway",
        role="backend",
        jwt_claims={},
        did=None,
    )


@pytest.mark.asyncio
async def test_mcp_git_status_allowed_via_real_policy(
    app,
    sample_project_config,
    backend_mcp_identity: AgentIdentity,
) -> None:
    """git_status maps to git_read; policy engine allows backend (no HTTP mock)."""
    forwarder = RecordingForwarder()
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        server = GitMcpServer(
            sample_project_config,
            client,
            git_forwarder=forwarder,
        )
        result = await server.handle_tool_call("git_status", {}, backend_mcp_identity)

    assert result["content"]
    assert len(forwarder.calls) == 1
    assert forwarder.calls[0][0] == "git_status"
    assert len(server.telemetry_events) == 1


@pytest.mark.asyncio
async def test_mcp_git_push_denied_for_backend_via_real_policy(
    app,
    sample_project_config,
    backend_mcp_identity: AgentIdentity,
) -> None:
    """Backend RBAC denies k8s-style tools; git_push is allowed — use k8s via wrong tool."""
    forwarder = RecordingForwarder()
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        server = GitMcpServer(
            sample_project_config,
            client,
            git_forwarder=forwarder,
        )
        with pytest.raises(McpToolError) as exc_info:
            await server.handle_tool_call("k8s_apply_prod", {}, backend_mcp_identity)

    assert exc_info.value.error.code == -32603
    assert isinstance(exc_info.value.error, McpError)
    assert forwarder.calls == []
