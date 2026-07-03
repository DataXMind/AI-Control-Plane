#!/usr/bin/env python3
"""Run a shell command only after ACP allows the tool (fail-closed).

Works from ai-control-plane OR Hybrid-AI-Gateway — no gateway package import.

Usage (from repo root):
    export ACP_API_URL=http://100.94.21.33:8000
    export ACP_AGENT_ID=agent1
    export ACP_ROLE=infra
    python examples/integrate/python/run_tool_guarded.py --tool git_read -- git status
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import httpx

DEFAULT_PROJECT_ID = "rust-gateway"


def _api_url() -> str:
    return os.environ.get("ACP_API_URL", "http://127.0.0.1:8000").rstrip("/")


def _timeout() -> float:
    return float(os.environ.get("ACP_TIMEOUT_S", "3.0"))


def acp_allow_tool(
    *,
    agent_id: str,
    role: str,
    tool_name: str,
    project_id: str | None = None,
    args: dict | None = None,
) -> dict:
    """Raise PermissionError on deny or ACP unreachable (fail-closed)."""
    payload: dict = {
        "agent_id": agent_id,
        "project_id": project_id or os.environ.get("ACP_PROJECT_ID", DEFAULT_PROJECT_ID),
        "tool_name": tool_name,
        "role": role,
    }
    if args:
        payload["args"] = args
    try:
        response = httpx.post(
            f"{_api_url()}/policy/evaluate",
            json=payload,
            timeout=_timeout(),
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise PermissionError(f"ACP evaluate failed (fail-closed): {exc}") from exc
    body = response.json()
    if not body.get("allowed"):
        raise PermissionError(body.get("reason") or "policy denied")
    return body


def _resolve_identity(
    agent_id: str | None,
    role: str | None,
) -> tuple[str, str]:
    aid = agent_id or os.environ.get("ACP_AGENT_ID") or "agent1"
    if role:
        return aid, role
    if aid == "agent2":
        return aid, os.environ.get("ACP_ROLE", "backend")
    if aid == "agent3":
        return aid, os.environ.get("ACP_ROLE", "reviewer")
    return aid, os.environ.get("ACP_ROLE", "infra")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACP-gated subprocess runner")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--args-json", default="{}")
    parser.add_argument("--agent-id", default=None)
    parser.add_argument("--role", default=None)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    ns = parser.parse_args()
    cmd = ns.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("error: no command after --", file=sys.stderr)
        return 2
    try:
        tool_args = json.loads(ns.args_json)
    except json.JSONDecodeError as exc:
        print(f"error: invalid --args-json: {exc}", file=sys.stderr)
        return 2
    if not isinstance(tool_args, dict):
        print("error: --args-json must be a JSON object", file=sys.stderr)
        return 2

    aid, r = _resolve_identity(ns.agent_id, ns.role)
    try:
        body = acp_allow_tool(
            agent_id=aid,
            role=r,
            tool_name=ns.tool,
            args=tool_args or None,
        )
        print(
            f"ACP allow tool={ns.tool} agent={aid} path={body.get('evaluation_path')}",
            file=sys.stderr,
        )
    except PermissionError as exc:
        print(f"ACP deny (fail-closed): {exc}", file=sys.stderr)
        return 1

    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
