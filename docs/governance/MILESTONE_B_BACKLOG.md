# Milestone B — Backlog (governance)

> **Status:** ACTIVE backlog — Sprint 1 **CLOSED** (2026-06-22)  
> **Source:** Phase 1 v2 re-audit + `scripts/create_milestone_a_issues.sh` MB7  
> **Tracking:** [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues) label `milestone-b`  
> **Sprint 1 report:** [`PHASE2_SPRINT1_REPORT.md`](PHASE2_SPRINT1_REPORT.md)

---

## Sprint 1 — CLOSED

| ID | Item | Status | Close commit |
|----|------|--------|--------------|
| MB-S1-1 | Guardrails + kill_switch loader (GAP-GR-1/2) | ✅ DONE | `2631c8e` |
| MB-S1-2 | ABAC full — `role_not_in`, `approval_status`, `read_only` (GAP-ABAC-1/2) | ✅ DONE | `5f8ce38` |
| MB-S1-3 | Coverage floor `fail_under=70`, policies 99% | ✅ DONE | `1720dc2` |
| MB-S1-4 | CLI assign/status tests via respx (GAP-CLI-1) | ✅ DONE | `4ee97d9` |
| MB-S1-5 | Identity JWT stub + SMK-06 (GAP-ID-1) | ✅ DONE | `41ccf65` |

**Branch:** `phase2/p2-0-tool-naming-and-p2-2` · **Baseline:** `master` @ `83e3ab5`

---

## MB7 — Guardrails + kill_switch from policies.yml

**Priority:** P1 (governance completeness)  
**Status:** ✅ **DONE** (Sprint 1, MB-S1-1) — see `tests/test_guardrails.py`

**Problem:** Shipped `config/policies.yml` defines `guardrails:` and `kill_switch:` but `config/loader.load_policies()` does not load them. `PolicyEngine._evaluate_guardrails()` exists but receives no `rule_type: guardrail` rules from YAML in Milestone A.

**Acceptance criteria (Milestone B):**

- [x] `_load_guardrails(raw)` maps `guardrails[].applies_to` → `PolicyRule` with `rule_type: guardrail`, `check`, `actions`, `roles`
- [x] `kill_switch.enabled` → global deny at policy eval (or documented HTTP 503 path)
- [x] `tests/test_loader.py` + `tests/test_policies.py` cover plan_required, tests_passed, branch_allowed from YAML
- [x] `ARCHITECTURE.md` table updated — guardrails row → ✅
- [x] SMK-01..06 still pass

**Non-goals:** Redis persistence, MCP HTTP transport.

**Dependencies:** P0-2 ingress normalize (✅ Phase 1 v2).

---

## Sprint 2 — IN PROGRESS

| ID | Item | Status | Issue |
|----|------|--------|-------|
| MB-S2-1 | RedisQuotaStore + `ACP_REDIS_URL` | ✅ DONE | #29 |
| MB-S2-2 | cli/approve live | ✅ DONE | #30 |
| MB-S2-3 | cli/quota live | ✅ DONE | #31 |
| MB-S2-4 | cli/logs + GET `/telemetry/events` | ✅ DONE | #32 |
| MB-S2-5 | mcp/server_factory.py | ✅ DONE | #34 partial |
| MB-S2-6 | Task persistence (#36) | ✅ DONE | #36 |
| MB-S2-7 | MCP HTTP transport + E2E | ✅ DONE | #34 |
| MB-S2-8 | JWKS RS256 (`ACP_JWKS_URL`) | ✅ DONE | — |
| MB-S2-9 | Branch protection workflow | ✅ DOC | GAP-BP-1 |

See [`PHASE2_SPRINT2_EXECUTION.md`](PHASE2_SPRINT2_EXECUTION.md).

---

## Sprint 2 — backlog (remaining)

---

## Related Milestone B items (existing issues #29–37)

| Area | Issue theme |
|------|-------------|
| Persistence | Redis quota, task store (#29–31) |
| CLI live | `approve`, `quota`, `logs` subcommands |
| Identity | JWT validation, SMK-06 — ✅ Sprint 1 |
| ABAC full | `approval_status`, `role_not_in`, `read_only` — ✅ Sprint 1 |
| Quotas | `by_model_profile`, `by_agent` enforcement |
| MCP | HTTP transport |

---

## How to open on GitHub

```bash
gh issue create --repo DataXMind/AI-Control-Plane \
  --title "MB7: Load guardrails and kill_switch from policies.yml" \
  --label "milestone-b,spec-gap" \
  --body "See docs/governance/MILESTONE_B_BACKLOG.md § MB7"
```

---

**Last updated:** 2026-06-22 (Sprint 2 batch 2 — persistence, MCP HTTP, JWKS)
