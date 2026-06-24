"""MCP server factory — wire GitMcpServer with HTTP policy client (Milestone B)."""

from __future__ import annotations

import os

import httpx

from ai_control_plane.core.models import ProjectConfig
from ai_control_plane.mcp.git_server import GitForwarder, GitMcpServer, HttpGitForwarder


def create_git_mcp_server(
    project: ProjectConfig,
    *,
    api_base_url: str | None = None,
    git_forwarder: GitForwarder | None = None,
    timeout: float = 2.0,
) -> GitMcpServer:
    """Build a Git MCP facade with an HTTP client to the control plane API."""
    base = api_base_url or os.environ.get("ACP_API_BASE_URL", "http://localhost:8000")
    client = httpx.AsyncClient(base_url=base, timeout=timeout)
    forwarder = git_forwarder
    if forwarder is None:
        git_url = os.environ.get("ACP_MCP_GIT_URL")
        if git_url:
            forwarder = HttpGitForwarder(git_url)
    return GitMcpServer(project, client, git_forwarder=forwarder)


__all__ = ["create_git_mcp_server"]
