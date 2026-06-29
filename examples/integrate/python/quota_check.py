#!/usr/bin/env python3
"""Read project quota before an LLM call (budget guard example).

Usage:
    export ACP_API_URL=http://localhost:8000
    python examples/integrate/python/quota_check.py
"""

from __future__ import annotations

import os
import sys

import httpx

DEFAULT_API_URL = "http://127.0.0.1:8000"
DEFAULT_PROJECT = "rust-gateway"
MIN_TOKENS = 1_000.0


def acp_api_url() -> str:
    return os.environ.get("ACP_API_URL", DEFAULT_API_URL).rstrip("/")


def fetch_project_quota(project_id: str, *, timeout: float = 2.0) -> dict:
    url = f"{acp_api_url()}/quota/{project_id}"
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        print(f"Quota read failed (fail-closed): {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> int:
    project_id = os.environ.get("ACP_PROJECT_ID", DEFAULT_PROJECT)
    quota = fetch_project_quota(project_id)
    remaining = float(quota.get("tokens_remaining", 0))
    print(f"project={project_id} tokens_remaining={remaining}")

    if remaining < MIN_TOKENS:
        print(
            f"Quota gate: remaining {remaining} < minimum {MIN_TOKENS} — skip LLM call",
            file=sys.stderr,
        )
        return 1

    print("Quota gate OK — proceed with LLM call.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
