# ACP Integration Examples

Runnable copy-paste patterns for **CONNECT door** (Task 2) — see [`docs/CLIENT_INTEGRATION.md`](../../docs/CLIENT_INTEGRATION.md) for Rust / Go / TypeScript and zero-git checklist.

**Prerequisite:** ACP API is running and `ACP_API_URL` points to it. Who hosts ACP: [`minimal/CUSTOMER_INSTALL.md`](../minimal/CUSTOMER_INSTALL.md).

```bash
export ACP_API_URL=http://localhost:8000   # or your operator's URL
pip install httpx                          # or: pip install -e ".[dev]" from repo root
```

## Python

| Script | Scenario | Run |
|--------|----------|-----|
| [`python/before_tool_call.py`](python/before_tool_call.py) | Deny unknown agents before tool execution | `python examples/integrate/python/before_tool_call.py` |
| [`python/run_tool_guarded.py`](python/run_tool_guarded.py) | **Enforce:** run shell cmd only if policy allows | `python examples/integrate/python/run_tool_guarded.py --tool git_read -- git status` |
| [`python/startup_health_gate.py`](python/startup_health_gate.py) | Exit non-zero if ACP unreachable at worker start | `python examples/integrate/python/startup_health_gate.py` |
| [`python/quota_check.py`](python/quota_check.py) | Read project quota before an LLM call | `python examples/integrate/python/quota_check.py` |

## Shell (Antigravity terminal / CI)

Run from **ai-control-plane repo root** (not Hybrid-AI-Gateway unless you synced `scripts/acp/` there):

```bash
export ACP_API_URL=http://<acp-host>:8000
export ACP_AGENT_ID=agent1   # MSI infra; use agent2 on Mac backend
export ACP_ROLE=infra

bash examples/integrate/shell/policy_smoke_matrix.sh
bash examples/integrate/shell/fail_closed_drill.sh
bash examples/integrate/shell/acp_evaluate.sh git_read && git status
```

| Script | Purpose |
|--------|---------|
| [`shell/acp_evaluate.sh`](shell/acp_evaluate.sh) | Exit 1 on deny — wrap any shell tool |
| [`shell/policy_smoke_matrix.sh`](shell/policy_smoke_matrix.sh) | 5-case live policy smoke |
| [`shell/fail_closed_drill.sh`](shell/fail_closed_drill.sh) | ACP down → gate blocks command |

## When to use which pattern

| Your situation | Pattern | API |
|----------------|---------|-----|
| Agent about to call `git_read`, `k8s_apply`, etc. | Before tool call | `POST /policy/evaluate` |
| Background worker / sidecar startup | Health gate | `GET /health` |
| Budget guard before model API | Quota check | `GET /quota/{project_id}` |
| Human approval required | Advanced | `requires_approval` in evaluate response — see Study 02 |

## Fail-closed rule

If `httpx` raises, `/health` is not `ok`, or `allowed` is `false` → **do not perform the action**.

## Index

- Full integration guide (all languages): [`docs/CLIENT_INTEGRATION.md`](../../docs/CLIENT_INTEGRATION.md)
- Operator install (Task 1): [`minimal/CUSTOMER_INSTALL.md`](../minimal/CUSTOMER_INSTALL.md)
- Minimal Docker stack: [`examples/minimal/`](../minimal/README.md)
- Full scenario map: [`docs/DEVELOPER_SCENARIOS.md`](../../docs/DEVELOPER_SCENARIOS.md)
