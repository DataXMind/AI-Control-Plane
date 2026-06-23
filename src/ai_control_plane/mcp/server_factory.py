"""MCP server factory — wire GitMcpServer with HTTP policy client (Milestone B)."""

from __future__ import annotations

import httpx

from ai_control_plane.core.models import ProjectConfig
from ai_control_plane.mcp.git_server import GitForwarder, GitMcpServer


def create_git_mcp_server(
    project: ProjectConfig,
    *,
    api_base_url: str = "http://localhost:8000",
    git_forwarder: GitForwarder | None = None,
    timeout: float = 2.0,
) -> GitMcpServer:
    """Build a Git MCP facade with an HTTP client to the control plane API."""
    client = httpx.AsyncClient(base_url=api_base_url, timeout=timeout)
    return GitMcpServer(project, client, git_forwarder=git_forwarder)


__all__ = ["create_git_mcp_server"]
