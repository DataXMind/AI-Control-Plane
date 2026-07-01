"""MCP git forwarder stubs and subprocess error paths (coverage Tier 3)."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from ai_control_plane.mcp.git_server import (
    JSON_RPC_INTERNAL_ERROR,
    McpToolError,
    StubGitForwarder,
    SubprocessGitForwarder,
)

_SUBPROCESS_PATCH = "ai_control_plane.mcp.git_server.asyncio.create_subprocess_exec"


@pytest.mark.asyncio
async def test_stub_git_forwarder_returns_delegated_payload() -> None:
    forwarder = StubGitForwarder()
    result = await forwarder.call_tool("git_status", {"path": "."})
    assert result["content"][0]["type"] == "text"
    payload = json.loads(result["content"][0]["text"])
    assert payload["delegated"] is True
    assert payload["tool"] == "git_status"


@pytest.mark.asyncio
async def test_subprocess_forwarder_nonzero_exit() -> None:
    forwarder = SubprocessGitForwarder(["false"])
    with pytest.raises(McpToolError) as exc_info:
        await forwarder.call_tool("git_status", {})
    assert exc_info.value.error.code == JSON_RPC_INTERNAL_ERROR


@pytest.mark.asyncio
async def test_subprocess_forwarder_invalid_json_stdout() -> None:
    process = AsyncMock()
    process.returncode = 0
    process.communicate = AsyncMock(return_value=(b"not-json", b""))

    with patch(_SUBPROCESS_PATCH, return_value=process):
        forwarder = SubprocessGitForwarder(["echo"])
        with pytest.raises(McpToolError, match="invalid response"):
            await forwarder.call_tool("git_status", {})


@pytest.mark.asyncio
async def test_subprocess_forwarder_json_rpc_error() -> None:
    error_payload = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": "tool failed"}},
    ).encode()
    process = AsyncMock()
    process.returncode = 0
    process.communicate = AsyncMock(return_value=(error_payload, b""))

    with patch(_SUBPROCESS_PATCH, return_value=process):
        forwarder = SubprocessGitForwarder(["cat"])
        with pytest.raises(McpToolError) as exc_info:
            await forwarder.call_tool("git_status", {})
        assert exc_info.value.error.code == -32000
