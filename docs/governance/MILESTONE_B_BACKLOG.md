# Milestone B — Backlog (governance)

> **Status:** **CLOSED** (code) — 2026-06-24  
> **Master:** post PR #51 (`milestone-b/s4-registry-quotas`)  
> **Sprint 1 report:** [`PHASE2_SPRINT1_REPORT.md`](PHASE2_SPRINT1_REPORT.md)

---

## Sprint 1 — CLOSED

| ID | Item | Status | Close commit |
|----|------|--------|--------------|
| MB-S1-1 | Guardrails + kill_switch loader | ✅ DONE | `2631c8e` |
| MB-S1-2 | ABAC full | ✅ DONE | `5f8ce38` |
| MB-S1-3 | Coverage floor 70% | ✅ DONE | `1720dc2` |
| MB-S1-4 | CLI assign/status tests | ✅ DONE | `4ee97d9` |
| MB-S1-5 | Identity JWT stub + SMK-06 | ✅ DONE | `41ccf65` |

---

## Sprint 2 — CLOSED

| ID | Item | Status | Issue |
|----|------|--------|-------|
| MB-S2-1 | RedisQuotaStore + `ACP_REDIS_URL` | ✅ | #29 |
| MB-S2-2 | cli/approve live | ✅ | #30 |
| MB-S2-3 | cli/quota live | ✅ | #31 |
| MB-S2-4 | cli/logs + GET `/telemetry/events` | ✅ | #32 |
| MB-S2-5 | mcp/server_factory.py | ✅ | #34 |
| MB-S2-6 | Task persistence (`ACP_DATA_DIR`) | ✅ | #36 |
| MB-S2-7 | MCP HTTP transport + E2E | ✅ | #34 |
| MB-S2-8 | JWKS RS256 (`ACP_JWKS_URL`) | ✅ | — |
| MB-S2-9 | Branch protection workflow doc | ✅ | GAP-BP-1 |
| MB-S2-10 | Redis ActionRegistry (#33) | ✅ | #33 |
| MB-S2-11 | Quotas by_agent / by_model_profile (GAP-Q-1) | ✅ | — |

See [`PHASE2_SPRINT2_EXECUTION.md`](PHASE2_SPRINT2_EXECUTION.md).

---

## Remaining (Public Beta / ops)

| Item | Issue / gap | Target |
|------|-------------|--------|
| ~~apex/ SAPAL pipeline live~~ | ~~#37~~ | ✅ Milestone C — PR #63 |
| ~~Telemetry persistence~~ | ~~#52~~ | ✅ PR #63 |
| cyanheads MCP E2E in CI | C+-6 | ✅ PR #74 |
| Public beta legal + examples | `OPEN_SOURCE_READINESS.md` | Pre-public |
| ~~Model profiles in AppState~~ | ~~#9, GAP-S4-1~~ | ✅ `load_model_profiles()` + `/health` wire proof |
| Branch protection API enforced | GAP-BP-1 (residual) | GitHub Team / public repo |

---

**Last updated:** 2026-06-24 (Milestone B + C + C+ code complete; #9 closed)
