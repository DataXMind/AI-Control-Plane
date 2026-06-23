"""MCP server factory tests."""

from __future__ import annotations

from ai_control_plane.core.models import ProjectConfig
from ai_control_plane.mcp.git_server import GitMcpServer, StubGitForwarder
from ai_control_plane.mcp.server_factory import create_git_mcp_server


def test_create_git_mcp_server(sample_project_config: ProjectConfig) -> None:
    server = create_git_mcp_server(
        sample_project_config,
        api_base_url="http://acp.test",
        git_forwarder=StubGitForwarder(),
    )
    assert isinstance(server, GitMcpServer)
    assert server.project.id == sample_project_config.id
