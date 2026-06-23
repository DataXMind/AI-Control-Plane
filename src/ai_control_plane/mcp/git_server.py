"""MCP Git facade — policy gate + telemetry; no direct Git execution."""

from __future__ import annotations

import asyncio
import json
import sys
from collections.abc import Callable
from typing import Any, NoReturn, Protocol, runtime_checkable

import httpx
import structlog

from ai_control_plane.api.schemas import PolicyEvalRequest, PolicyEvalResponse
from ai_control_plane.core.models import (
    AgentIdentity,
    McpError,
    ProjectConfig,
    TelemetryEvent,
)
from ai_control_plane.core.telemetry import InMemoryTelemetryStore, TelemetryWriter
from ai_control_plane.core.tool_names import resolve_policy_tool_name

logger = structlog.get_logger(__name__)

JSON_RPC_INTERNAL_ERROR = -32603
POLICY_EVAL_PATH = "/policy/evaluate"
POLICY_TIMEOUT_SECONDS = 2.0
EVENT_TOOL_CALL = "TOOL_CALL"


class McpToolError(Exception):
    """Exception raised for MCP tool failures; carries a domain McpError payload."""

    def __init__(
        self,
        code: int,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        self.error = McpError(code=code, message=message, data=data)
        super().__init__(message)


@runtime_checkable
class GitForwarder(Protocol):
    """Delegate Git tool execution to the cyanheads TypeScript MCP server."""

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Forward a tool call to the underlying Git MCP runtime."""
        ...


class SubprocessGitForwarder:
    """Forward tool calls to cyanheads git-mcp-server via subprocess (stdio JSON-RPC)."""

    def __init__(self, command: list[str]) -> None:
        self._command = command

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": args},
        }
        process = await asyncio.create_subprocess_exec(
            *self._command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate(json.dumps(request).encode("utf-8"))
        if process.returncode != 0:
            msg = f"git forwarder failed: {stderr.decode('utf-8', errors='replace')}"
            raise McpToolError(JSON_RPC_INTERNAL_ERROR, msg)

        try:
            payload = json.loads(stdout.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise McpToolError(
                JSON_RPC_INTERNAL_ERROR,
                "invalid response from git forwarder",
            ) from exc

        if "error" in payload:
            error = payload["error"]
            raise McpToolError(
                int(error.get("code", JSON_RPC_INTERNAL_ERROR)),
                str(error.get("message", "git forwarder error")),
                data=error.get("data"),
            )

        result = payload.get("result", {})
        if isinstance(result, dict) and "content" in result:
            return dict(result)
        return {"content": result}


class StubGitForwarder:
    """Milestone A stub when cyanheads server is not wired yet."""

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "delegated": True,
                            "tool": tool_name,
                            "args": args,
                            "note": "cyanheads git-mcp-server not configured",
                        },
                    ),
                },
            ],
        }


def _raise_mcp(code: int, message: str, data: dict[str, Any] | None = None) -> NoReturn:
    raise McpToolError(code, message, data)


_GIT_TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "git_clone",
        "description": "Clone the project repository into the workspace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "branch": {"type": "string"},
            },
        },
    },
    {
        "name": "git_branch",
        "description": "Create or list Git branches.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "checkout": {"type": "boolean"},
            },
        },
    },
    {
        "name": "git_commit",
        "description": "Stage and commit changes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "paths": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["message"],
        },
    },
    {
        "name": "git_push",
        "description": "Push commits to the remote repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "remote": {"type": "string"},
                "branch": {"type": "string"},
            },
        },
    },
    {
        "name": "git_pr_create",
        "description": "Open a pull request for the current branch.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "base": {"type": "string"},
            },
            "required": ["title"],
        },
    },
    {
        "name": "git_status",
        "description": "Show working tree status.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


class GitMcpServer:
    """Policy-gated MCP Git facade; Git execution lives in cyanheads TypeScript."""

    def __init__(
        self,
        project: ProjectConfig,
        policy_client: httpx.AsyncClient,
        *,
        git_forwarder: GitForwarder | None = None,
        store: InMemoryTelemetryStore | None = None,
        on_telemetry: Callable[[TelemetryEvent], None] | None = None,
    ) -> None:
        self._project = project
        self._policy_client = policy_client
        self._git_forwarder: GitForwarder = git_forwarder or StubGitForwarder()
        self._store = store or InMemoryTelemetryStore()
        self._writer = TelemetryWriter(self._store)
        self._on_telemetry = on_telemetry

    @property
    def project(self) -> ProjectConfig:
        return self._project

    @property
    def telemetry_store(self) -> InMemoryTelemetryStore:
        return self._store

    @property
    def telemetry_events(self) -> list[TelemetryEvent]:
        return self._store.list_events()

    def list_tools(self) -> list[dict[str, Any]]:
        """Return MCP tool definitions in JSON-RPC tools/list format."""
        return [dict(tool) for tool in _GIT_TOOL_DEFINITIONS]

    async def handle_tool_call(
        self,
        tool_name: str,
        args: dict[str, Any],
        identity: AgentIdentity,
    ) -> dict[str, Any]:
        """Evaluate policy, optionally forward to cyanheads, emit telemetry."""
        decision = await self._evaluate_policy(tool_name, args, identity)

        if not decision.allowed:
            _raise_mcp(
                JSON_RPC_INTERNAL_ERROR,
                decision.reason,
                data={"policy_id": decision.policy_id, "allowed": False},
            )

        if decision.requires_approval:
            _raise_mcp(
                JSON_RPC_INTERNAL_ERROR,
                "approval required",
                data={
                    "status": "pending_approval",
                    "policy_id": decision.policy_id,
                    "reason": decision.reason,
                },
            )

        forward_args = {
            **args,
            "repo": self._project.repo,
            "default_branch": self._project.default_branch,
            "project_id": self._project.id,
        }
        result = await self._git_forwarder.call_tool(tool_name, forward_args)

        self._emit_tool_call(tool_name, args, identity, decision.policy_id)
        return result

    async def start(self, transport: str = "stdio") -> None:
        """Start the MCP server loop (stdio for Milestone A)."""
        if transport == "stdio":
            await self._run_stdio()
            return
        if transport == "http":
            msg = "HTTP transport is planned for Milestone B"
            raise NotImplementedError(msg)
        msg = f"unsupported transport '{transport}'"
        raise ValueError(msg)

    async def _evaluate_policy(
        self,
        tool_name: str,
        args: dict[str, Any],
        identity: AgentIdentity,
    ) -> PolicyEvalResponse:
        payload = PolicyEvalRequest(
            agent_id=identity.agent_id,
            project_id=identity.project_id,
            tool_name=resolve_policy_tool_name(tool_name),
            args=args,
            role=identity.role,
        )
        try:
            response = await self._policy_client.post(
                POLICY_EVAL_PATH,
                json=payload.model_dump(mode="json"),
                timeout=POLICY_TIMEOUT_SECONDS,
            )
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            raise McpToolError(JSON_RPC_INTERNAL_ERROR, "policy_unavailable") from exc

        try:
            body = response.json()
            if not isinstance(body, dict):
                _raise_mcp(JSON_RPC_INTERNAL_ERROR, "policy_unavailable")
            return PolicyEvalResponse.model_validate(body)
        except (ValueError, TypeError) as exc:
            raise McpToolError(JSON_RPC_INTERNAL_ERROR, "policy_unavailable") from exc

    def _emit_tool_call(
        self,
        tool_name: str,
        args: dict[str, Any],
        identity: AgentIdentity,
        policy_id: str | None,
    ) -> None:
        event = TelemetryEvent(
            event_type=EVENT_TOOL_CALL,
            agent_id=identity.agent_id,
            project_id=identity.project_id,
            payload={
                "tool_name": tool_name,
                "args": args,
                "policy_id": policy_id,
                "repo": self._project.repo,
            },
        )
        try:
            sealed = self._writer.emit(event)
            if self._on_telemetry is not None:
                self._on_telemetry(sealed)
        except Exception as exc:
            logger.warning(
                "telemetry_emit_failed",
                tool_name=tool_name,
                agent_id=identity.agent_id,
                error=str(exc),
            )

    async def _run_stdio(self) -> None:
        """Minimal MCP stdio loop for tools/list and tools/call."""
        loop = asyncio.get_running_loop()
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break

            try:
                message = json.loads(line.decode("utf-8") if isinstance(line, bytes) else line)
            except json.JSONDecodeError:
                continue

            response = await self._dispatch_stdio_message(message)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

    async def _dispatch_stdio_message(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        request_id = message.get("id")
        if request_id is None:
            return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "ai-control-plane-git", "version": "0.0.1"},
                },
            }

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": self.list_tools()},
            }

        if method == "tools/call":
            params = message.get("params", {})
            tool_name = str(params.get("name", ""))
            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                arguments = {}

            identity_payload = arguments.pop("_identity", {})
            if not isinstance(identity_payload, dict):
                identity_payload = {}

            identity = AgentIdentity(
                agent_id=str(identity_payload.get("agent_id", "unknown")),
                project_id=str(identity_payload.get("project_id", self._project.id)),
                role=str(identity_payload.get("role", "backend")),
                jwt_claims=dict(identity_payload.get("jwt_claims", {})),
                did=identity_payload.get("did"),
            )

            try:
                result = await self.handle_tool_call(tool_name, arguments, identity)
                return {"jsonrpc": "2.0", "id": request_id, "result": result}
            except McpToolError as exc:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": exc.error.model_dump(mode="json"),
                }

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": JSON_RPC_INTERNAL_ERROR,
                "message": f"unsupported method '{method}'",
            },
        }


__all__ = [
    "GitForwarder",
    "GitMcpServer",
    "McpToolError",
    "StubGitForwarder",
    "SubprocessGitForwarder",
]
