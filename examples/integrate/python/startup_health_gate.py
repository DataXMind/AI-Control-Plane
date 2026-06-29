#!/usr/bin/env python3
"""Refuse to start if ACP /health is not ok (fail-closed worker gate).

Usage:
    export ACP_API_URL=http://localhost:8000
    python examples/integrate/python/startup_health_gate.py
    echo $?   # 0 = safe to start worker; non-zero = do not start
"""

from __future__ import annotations

import os
import sys

import httpx

DEFAULT_API_URL = "http://127.0.0.1:8000"


def acp_api_url() -> str:
    return os.environ.get("ACP_API_URL", DEFAULT_API_URL).rstrip("/")


def assert_acp_healthy(*, timeout: float = 2.0) -> dict:
    """Exit the process if ACP is unreachable or not ready."""
    url = f"{acp_api_url()}/health"
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        body = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        print(f"ACP health gate FAILED (fail-closed): {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if body.get("status") != "ok":
        print(f"ACP health gate FAILED: status={body.get('status')!r}", file=sys.stderr)
        raise SystemExit(1)
    if not body.get("config_loaded"):
        print("ACP health gate FAILED: config_loaded=false", file=sys.stderr)
        raise SystemExit(1)

    return body


def main() -> int:
    body = assert_acp_healthy()
    rules = body.get("policy_rules_count", "?")
    print(f"ACP health gate OK — policy_rules_count={rules}")
    print("Safe to start agent worker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
