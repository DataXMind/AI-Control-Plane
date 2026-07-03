#!/usr/bin/env python3
"""ACP policy gate for Hybrid AI Gateway + Antigravity agents.

Maps shipped production-config agents (agent1=infra-antigravity, agent2=backend-vscode).

Usage:
    export ACP_API_URL=http://localhost:8000
    python examples/integrate/python/gateway_antigravity_hook.py

Copy acp_allow_tool() into gateway request-router or Antigravity tool wrapper.
See docs/integrations/HYBRID_AI_GATEWAY.md
"""

from __future__ import annotations

import os
import sys

import httpx

DEFAULT_API_URL = "http://127.0.0.1:8000"
DEFAULT_PROJECT_ID = "rust-gateway"


def acp_api_url() -> str:
    return os.environ.get("ACP_API_URL", DEFAULT_API_URL).rstrip("/")


def acp_allow_tool(
    *,
    agent_id: str,
    tool_name: str,
    role: str,
    project_id: str | None = None,
    timeout: float = 2.0,
) -> dict:
    """Raise PermissionError when policy denies; return body on allow."""
    url = f"{acp_api_url()}/policy/evaluate"
    payload = {
        "agent_id": agent_id,
        "project_id": project_id or os.environ.get("ACP_PROJECT_ID", DEFAULT_PROJECT_ID),
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


def main() -> int:
    print(f"ACP_API_URL={acp_api_url()}")
    print(f"ACP_PROJECT_ID={os.environ.get('ACP_PROJECT_ID', DEFAULT_PROJECT_ID)}")

    # agent1 — Antigravity infra (production-config agents.yml)
    body = acp_allow_tool(agent_id="agent1", tool_name="git_read", role="infra")
    print(f"ALLOW agent1: policy_id={body.get('policy_id')}")

    # agent2 — backend Rust work
    body = acp_allow_tool(agent_id="agent2", tool_name="build.rust", role="backend")
    print(f"ALLOW agent2: policy_id={body.get('policy_id')}")

    try:
        acp_allow_tool(agent_id="unknown-agent", tool_name="git_read", role="backend")
    except PermissionError as exc:
        print(f"DENY (expected): {exc}")
    else:
        print("ERROR: unknown agent should be denied", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
