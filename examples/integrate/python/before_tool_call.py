#!/usr/bin/env python3
"""Call POST /policy/evaluate before executing an agent tool (fail-closed).

Usage:
    export ACP_API_URL=http://localhost:8000
    python examples/integrate/python/before_tool_call.py

Copy the acp_allow() helper into your agent or tool wrapper.
"""

from __future__ import annotations

import os
import sys

import httpx

DEFAULT_API_URL = "http://127.0.0.1:8000"


def acp_api_url() -> str:
    return os.environ.get("ACP_API_URL", DEFAULT_API_URL).rstrip("/")


def acp_allow(
    *,
    agent_id: str,
    project_id: str,
    tool_name: str,
    role: str,
    timeout: float = 2.0,
) -> dict:
    """Raise PermissionError when policy denies; return evaluate body on allow."""
    url = f"{acp_api_url()}/policy/evaluate"
    payload = {
        "agent_id": agent_id,
        "project_id": project_id,
        "tool_name": tool_name,
        "role": role,
    }
    try:
        response = httpx.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        msg = f"ACP evaluate failed (fail-closed): {exc}"
        raise PermissionError(msg) from exc

    body = response.json()
    if not body.get("allowed"):
        reason = body.get("reason") or "policy denied"
        raise PermissionError(reason)
    return body


def run_demo_tool() -> str:
    """Placeholder — replace with your real tool (MCP, LangChain tool, subprocess, etc.)."""
    return "tool executed"


def main() -> int:
    print(f"ACP_API_URL={acp_api_url()}")

    # Demo: allowed path (fixture config agent2 / rust-gateway / git_read)
    body = acp_allow(
        agent_id="agent2",
        project_id="rust-gateway",
        tool_name="git_read",
        role="backend",
    )
    print(f"ALLOW: policy_id={body.get('policy_id')} latency_ms={body.get('latency_ms')}")
    print(run_demo_tool())

    # Demo: deny path
    try:
        acp_allow(
            agent_id="unknown-agent",
            project_id="rust-gateway",
            tool_name="git_read",
            role="backend",
        )
    except PermissionError as exc:
        print(f"DENY (expected): {exc}")
    else:
        print("ERROR: unknown agent should be denied", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
