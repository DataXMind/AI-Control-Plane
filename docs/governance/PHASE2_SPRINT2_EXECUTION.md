# Milestone B — Sprint 2 execution plan

> **Status:** CLOSED — master post PR #51  
> **Baseline:** master after PR #49 (`5cc43a7`)

---

## Sprint 2 scope (#29–34, #36)

| ID | Item | Issue | Status |
|----|------|-------|--------|
| MB-S2-1 | `RedisQuotaStore` + `ACP_REDIS_URL` | #29 | ✅ |
| MB-S2-2 | `cli/approve` → POST `/policy/approve` | #30 | ✅ |
| MB-S2-3 | `cli/quota` → GET `/quota/{project_id}` | #31 | ✅ |
| MB-S2-4 | `cli/logs` → GET `/telemetry/events` | #32 | ✅ |
| MB-S2-5 | `mcp/server_factory.py` | #34 partial | ✅ |
| MB-S2-6 | Task persistence (`ACP_DATA_DIR`) | #36 | ✅ |
| MB-S2-7 | MCP HTTP transport + E2E | #34 | ✅ |
| MB-S2-8 | JWKS / RS256 JWT (`ACP_JWKS_URL`) | Milestone B | ✅ |
| MB-S2-9 | Branch protection workflow doc | GAP-BP-1 | ✅ Doc |
| MB-S2-10 | Redis ActionRegistry (#33) | #33 | ✅ |
| MB-S2-11 | Quotas by_agent / by_model_profile | GAP-Q-1 | ✅ |

---

## API additions (Sprint 2 close)

| Endpoint | Purpose |
|----------|---------|
| `GET /quota/agent/{agent_id}` | Agent daily token budget |
| `GET /quota/profile/{profile_id}` | Model profile daily token budget |

| Variable | Purpose |
|----------|---------|
| `ACP_DATA_DIR` | File-backed `TaskStore` (`tasks/*.json`) |
| `ACP_JWKS_URL` | RS256 JWKS validator (else HS256 dev stub) |
| `ACP_MCP_GIT_URL` | HTTP forwarder to cyanheads git-mcp-server |
| `ACP_MCP_HTTP_HOST` / `ACP_MCP_HTTP_PORT` | MCP HTTP listen bind |
| `ACP_API_BASE_URL` | Factory default policy client base URL |

---

## Gates (target)

- pytest full pass
- ruff + mypy strict clean
- Optional extras: `[redis]`, `[jwt]`

---

**Related:** [`PHASE2_SPRINT1_CHECKLIST_COMPLETION.md`](PHASE2_SPRINT1_CHECKLIST_COMPLETION.md), [`BRANCH_PROTECTION.md`](BRANCH_PROTECTION.md)
