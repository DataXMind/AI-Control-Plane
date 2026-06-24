"""MCP HTTP transport E2E — JSON-RPC over POST /mcp (#34)."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from ai_control_plane.core.models import ProjectConfig
from ai_control_plane.mcp.git_server import (
    GitMcpServer,
    HttpGitForwarder,
    StubGitForwarder,
    create_mcp_http_app,
)

POLICY_ALLOW = {
    "allowed": True,
    "reason": "ok",
    "requires_approval": False,
    "policy_id": None,
    "latency_ms": 1.0,
}


def _policy_transport(body: dict[str, Any]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/policy/evaluate"
        return httpx.Response(200, json=body)

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_mcp_http_tools_list(sample_project_config: ProjectConfig) -> None:
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_ALLOW),
        base_url="http://acp.test",
    ) as policy_client:
        server = GitMcpServer(sample_project_config, policy_client)
        app = create_mcp_http_app(server)
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/mcp",
                json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
            )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    tool_names = {tool["name"] for tool in body["result"]["tools"]}
    assert "git_status" in tool_names


@pytest.mark.asyncio
async def test_http_git_forwarder_delegates(respx_mock) -> None:
    respx_mock.post("http://git-mcp.test/mcp").respond(
        200,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"content": [{"type": "text", "text": "delegated"}]},
        },
    )
    forwarder = HttpGitForwarder("http://git-mcp.test")
    result = await forwarder.call_tool("git_status", {"repo": "x"})
    assert result["content"][0]["text"] == "delegated"


@pytest.mark.asyncio
async def test_mcp_http_tools_call_with_stub_forwarder(
    sample_project_config: ProjectConfig,
) -> None:
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_ALLOW),
        base_url="http://acp.test",
    ) as policy_client:
        server = GitMcpServer(
            sample_project_config,
            policy_client,
            git_forwarder=StubGitForwarder(),
        )
        app = create_mcp_http_app(server)
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "git_status",
                        "arguments": {
                            "_identity": {
                                "agent_id": "agent2",
                                "project_id": "rust-gateway",
                                "role": "backend",
                            },
                        },
                    },
                },
            )

    assert response.status_code == 200
    body = response.json()
    assert "result" in body
    assert body["result"]["content"]


@pytest.mark.asyncio
async def test_mcp_http_e2e_policy_and_tool_call(
    sample_project_config: ProjectConfig,
) -> None:
    """MC-8 — JSON-RPC tools/list + tools/call through HTTP MCP with policy gate."""
    async with httpx.AsyncClient(
        transport=_policy_transport(POLICY_ALLOW),
        base_url="http://acp.test",
    ) as policy_client:
        server = GitMcpServer(
            sample_project_config,
            policy_client,
            git_forwarder=StubGitForwarder(),
        )
        app = create_mcp_http_app(server)
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            list_resp = await client.post(
                "/mcp",
                json={"jsonrpc": "2.0", "id": 10, "method": "tools/list"},
            )
            call_resp = await client.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 11,
                    "method": "tools/call",
                    "params": {
                        "name": "git_status",
                        "arguments": {
                            "_identity": {
                                "agent_id": "agent2",
                                "project_id": "rust-gateway",
                                "role": "backend",
                            },
                        },
                    },
                },
            )

    assert list_resp.status_code == 200
    assert call_resp.status_code == 200
    call_body = call_resp.json()
    assert "result" in call_body
    assert call_body["result"]["content"]
