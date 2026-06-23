# Milestone B — Sprint 2 execution plan

> **Status:** IN PROGRESS (branch `milestone-b/s2-execution`)  
> **Baseline:** Sprint 1 close `1dae3ea` (PR #48)

---

## Sprint 2 scope (#29–34, partial #36)

| ID | Item | Issue | Status |
|----|------|-------|--------|
| MB-S2-1 | `RedisQuotaStore` + `ACP_REDIS_URL` | #29 | ✅ Implemented |
| MB-S2-2 | `cli/approve` → POST `/policy/approve` | #30 | ✅ Implemented |
| MB-S2-3 | `cli/quota` → GET `/quota/{project_id}` | #31 | ✅ Implemented |
| MB-S2-4 | `cli/logs` → GET `/telemetry/events` | #32 | ✅ Implemented |
| MB-S2-5 | `mcp/server_factory.py` | #34 partial | ✅ Factory stub |
| MB-S2-6 | Task persistence across restart | #36 | 🔲 OPEN |
| MB-S2-7 | MCP HTTP transport + cyanheads E2E | #34, #37 | 🔲 OPEN |
| MB-S2-8 | JWKS / RS256 JWT | Milestone C | 🔲 Deferred |
| MB-S2-9 | Branch protection CI gate | GAP-BP-1 | 🔲 Human/org — blocked |

---

## Gates (target)

- pytest full pass
- CLI tests: assign, status, approve, quota, logs
- `ACP_REDIS_URL` optional — in-memory default unchanged

---

**Related:** [`PHASE2_SPRINT1_CHECKLIST_COMPLETION.md`](PHASE2_SPRINT1_CHECKLIST_COMPLETION.md)
