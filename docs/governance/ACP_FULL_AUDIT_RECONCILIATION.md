# ACP Full Audit — Reconciliation (strict)

**Document ID:** ACP-GOV-AUDIT-RECON-001  
**Version:** 1.0  
**Audit date:** 2026-06-24  
**Baseline artifact:** [`acp_full_audit_report.html`](acp_full_audit_report.html) (Claude, snapshot @ `fc296d4`)  
**Code truth:** `master` @ `a285539` (PR #63 Milestone C + PR #64 hygiene)  
**Method:** Pass 1 artifact vs code; Pass 2 governance vs GitHub; Pass 3 Claude prompt intent vs delivered diff

---

## Executive verdict

| Dimension | @ `fc296d4` (HTML) | @ `a285539` (live) | Strict assessment |
|-----------|-------------------|-------------------|-------------------|
| Milestone A | 100% CLOSED | 100% CLOSED | ✅ Aligned |
| Milestone B | 100% CLOSED | 100% CLOSED | ✅ Aligned |
| Milestone C | **5% stubs** | **~55% boundary / ~25% architect vision** | ⚠️ **Scope reinterpretation** |
| Public Beta | 38% | ~38% | ✅ Aligned (unchanged) |
| Doc truth | 9 drift items | **5 resolved, 4 remain** | ⚠️ Partial |
| GitHub hygiene | 5 OPEN (HTML) | **2 OPEN (#9, #39)** | ✅ Improved post #64 |
| 8 invariants | Intact | Intact | ✅ |

**Strict Milestone C verdict:** **BOUNDARY CLOSED, DEPTH NO-GO** for architect-grade SAPAL (OTel, Argos, Darts, PolicyEngine-gated act, cyanheads CI). PR #63 đóng milestone *scaffold/wiring*; không đóng milestone *intelligence layer* trong HTML pane ⑤.

---

## 1. Completion % (re-scored)

### Milestone A — 100% ✅

No change from HTML audit. Evidence: #38 closed, P0 gate passed, 156 tests (superset of 91).

### Milestone B — 100% ✅

No change from HTML audit. Evidence: `MILESTONE_B_BACKLOG.md` Sprint 1+2, PR #48–#51.

### Milestone C — rescored

| Layer | Weight | HTML @ fc296d4 | Live @ a285539 | Evidence |
|-------|--------|----------------|----------------|----------|
| **C-boundary** (no stubs, loop runs, API/CLI, file telemetry) | 50% | 5% | **100%** | PR #63: adapters, `SapalLoop`, `/apex/*`, `agentctl apex`, `FileTelemetryStore`, 156 pytest |
| **C-integration** (otel script, MCP E2E) | 15% | 0% | **60%** | `run_otel_collector.sh` stub; MCP E2E with `StubGitForwarder` only |
| **C-architect** (OTel IF, Argos, Darts, replay API, policy-gated act) | 35% | 0% | **0%** | Not in code; see pane ⑤ blockers in HTML |

**Composite Milestone C (strict):** 50%×100% + 15%×60% + 35%×0% = **59%** overall.  
**Reporting labels:**

- **Milestone C (boundary):** CLOSED — issues #37, #52–#62, PR #63  
- **Milestone C+ (architect depth):** NOT STARTED — see `CLAUDE_PROMPT_MILESTONE_C_PLUS.md`

### Public Beta — ~38% ✅

Unchanged. Legal artifacts, soak, OpenAPI, `examples/` absent.

---

## 2. HTML discrepancies D-01..D-09 — reconciliation

| ID | HTML claim | Status @ a285539 | Action |
|----|------------|------------------|--------|
| D-01 | Sprint 1 close commit ambiguity | ✅ `1dae3ea` = PR #48 merge on master | None |
| D-02 | PHASE1 §4.2 GAP-Q-1/S4-1 stale | ❌ **Still stale** | Fix PHASE1_REPORT_V2 §4.2 |
| D-03 | ARCHITECTURE stores section misleading | ✅ Fixed PR #63/#64 (`TelemetryStore`, title) | None |
| D-04 | Rule 1 seven PRs waived | ✅ Documented Path B | None |
| D-05 | Milestone B description incomplete | ⚠️ Partial — C closed, B line still short | Expand ARCHITECTURE §mapping |
| D-06 | DEVELOPMENT_PROTOCOL SMK count | ✅ v1.4 has 8 smoke tests | None |
| D-07 | #35, #45 state conflict | ✅ Closed (hygiene) | None |
| D-08 | agent4 ordering risk | ✅ MB-S1-2 + parity tests | None |
| D-09 | API surface missing Sprint 2 endpoints | ❌ **Still stale** — table stops at 7 rows | Add quota agent/profile, telemetry, apex |

---

## 3. HTML issue verdicts (pane ③) vs live

| Issue | HTML verdict | Live @ a285539 |
|-------|--------------|----------------|
| #8 | CLOSE | ✅ Closed |
| #35 | CLOSE | ✅ Closed (prior hygiene) |
| #45 | CLOSE | ✅ Closed (prior hygiene) |
| #37 | KEEP OPEN (stubs) | ✅ Closed PR #64 — **was stale verdict**; SAPAL MVP live |
| GAP-BP-1 | KEEP OPEN | ✅ Still open (external) — no GitHub issue #, doc only |

**Additional closures PR #64:** #3 (exceptions exist), #13 (README runbook), #53–#62 (MC items).

**Remaining OPEN:** #9 (`load_model_profiles` → AppState), #39 (extended `/health` proof).

---

## 4. Go/No-Go pane ⑤ — blocker reconciliation

HTML said **NO-GO** to *start* Milestone C. Execution **proceeded** with MVP scope (human-approved MC-1..11 bulk). Blocker status now:

| Blocker | @ fc296d4 | @ a285539 | Notes |
|---------|-----------|-----------|-------|
| OTel collector | ❌ absent | ⚠️ stub script only | `scripts/run_otel_collector.sh` — no `otel-collector.yaml` |
| `TelemetryStore.replay()` | ❌ | ❌ | Only `list_events()` used |
| Darts / sklearn extras | ❌ | ❌ | Not in `pyproject.toml` |
| Argos design doc | ❌ | ❌ | Not created |
| act.py PolicyEngine gate | ❌ | ❌ | Heuristic skip only |
| cyanheads MCP E2E CI | ❌ | ❌ | `HttpGitForwarder` unit mock only |
| Production soak | ❌ | ❌ | Unchanged |
| Doc drift HIGH | ❌ | ⚠️ partial | API table + PHASE1 §4.2 remain |
| #37 sub-issues | ❌ | ✅ #52–#62 created | Titles match modules; AC depth not met |

**Interpretation:** HTML NO-GO was **correct for architect-grade C**. Team **overrode** with boundary MVP — valid if labeled honestly (now in this doc + `MILESTONE_C_SPRINT_PLAN.md` beyond section).

---

## 5. Cursor prompt packet (HTML pane ⑥) — execution scorecard

| Prompt | Tasks | Done | Partial | Not done |
|--------|-------|------|---------|----------|
| **1** Issue hygiene | Close #8,#35,#45; label #37 | #8,#35,#45,#37,#3,#13,#53–62 | — | GAP-BP-1 issue (no #) |
| **2** HIGH doc drift | API surface, stores, execution, PHASE1 | stores, execution, MC status | API surface table | PHASE1 §4.2 |
| **3** MED + MC breakdown | SMK sync, OS readiness, MC issues OTel/Argos | SMK, partial OS | MC issues created | OTel/Argos/Darts in code |

---

## 6. Strict invariant audit @ a285539

| # | Invariant | Status | Note |
|---|-----------|--------|------|
| 1 | Custom PolicyEngine | ✅ | |
| 2 | models.py SSOT | ✅ | MC added no new types |
| 3 | MCP facade | ✅ | |
| 4 | CLI HTTP-only | ✅ | `agentctl apex` via `_http.py` |
| 5 | apex owns SAPAL | ⚠️ | Loop lives in apex; **OSS not called from apex** (architect target unmet) |
| 6 | api/ TS bridge | ✅ | + `/apex/*` |
| 7 | QuotaStore swappable | ✅ | |
| 8 | ACP_CONFIG_DIR | ✅ | + `ACP_DATA_DIR` telemetry |

---

## 7. Remaining doc drift (ordered)

| Sev | File | Fix |
|-----|------|-----|
| HIGH | `PHASE1_REPORT_V2.md` §4.2, §5, §6 | Move GAP-Q-1 to closed; update invariant #5/#7; apex not stubs |
| HIGH | `ARCHITECTURE.md` §API surface | Add `/quota/agent`, `/quota/profile`, `/telemetry/events`, `/apex/status`, `/apex/trigger` |
| MED | `OPEN_SOURCE_READINESS.md` §Milestone mapping | Milestone B/C CLOSED dates |
| MED | `ARCHITECTURE.md` §Milestone B one-liner | Expand Sprint 2 scope |
| LOW | `PHASE2_SPRINT1_REPORT.md` | Reference final Codecov if available |

---

## 8. Recommended next artifacts / prompts

1. **`CLAUDE_PROMPT_MILESTONE_C_PLUS.md`** — architect review for OTel, Argos, Darts, act policy-gate (before code)  
2. **`ACP_CURSOR_PROMPT_PACKET_POST_MC.md`** — Cursor: fix remaining doc drift + optional C+ issues  
3. Update **`DEVELOPMENT_PROTOCOL.md`** D8 footnote: "MVP live; C+ = OSS adapters"

---

## 9. Sign-off

| Question | Answer |
|----------|--------|
| Project on track for private governance core? | **Yes** |
| Milestone C "done" per HTML architect spec? | **No** (59% strict composite) |
| Safe to claim Public Beta? | **No** |
| HTML `acp_full_audit_report.html` still valid? | **Historical only** — use this reconciliation |

---

**Related:** [`ACP_ARTIFACT_PUZZLE_MAP.md`](ACP_ARTIFACT_PUZZLE_MAP.md) · [`MILESTONE_C_SPRINT_PLAN.md`](MILESTONE_C_SPRINT_PLAN.md) · [`docs/prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md`](../prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md)
