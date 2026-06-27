# Claude `acp_status_audit_analysis.html` — reconciliation & action plan

**Document ID:** ACP-GOV-ACP-STATUS-AUDIT-RECON-001  
**Audit date:** 2026-06-27  
**Source:** `acp_status_audit_analysis.html` (Claude analysis of `PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`)  
**Baseline:** `master` · catalog **v1.3.3**  
**Execution SSOT:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)

---

## Executive verdict

| Claude claim | Reconciliation |
|--------------|----------------|
| Project at engineering → operations handoff | ✅ **Agree** — accurate framing |
| Technical surface complete | ✅ **Agree** — no missing PB-T Cursor work |
| 7 gates remaining, calendar/human | ✅ **Agree** — matches runtime catalog |
| Claude role = review prep, no new code | ⚠️ **Mostly agree** — **exception:** ops hygiene (soak repo log, templates) is valid LOW-risk Cursor work |
| PB-9 gap needs clarify | ✅ **Agree** — **resolved** in `PB9_STAGING_SOAK_LOG.md` § clock vs evidence |
| PB-10 may not block 0.x beta | ✅ **Agree with human sign-off** — policy documented; catalog entry unchanged until flip |
| Drift guard 10 items | ✅ **Agree** — aligned with `PROJECT_STATUS_AUDIT` §7 |

---

## Tab-by-tab harsh audit

### ① Verdict

| Element | Assessment | Deeper view |
|---------|------------|-------------|
| Self-correcting OpenAPI fix | ✅ Valid | Demonstrates reconciliation loop works; should be cited as ML5 pattern not luck |
| CI chain praise | ✅ Valid | `examples-minimal-smoke` is the real gate — not hypothetical `examples-smoke` |
| "Cursor work is done" | ⚠️ Nuance | **Feature code:** done. **Ops docs + soak persistence:** ongoing through PB-12 |
| PB-9 gap 06-22→25 | ✅ Critical catch | Root cause: Day 0 "deploy deferred" + `/tmp` logs — not silent failure |
| Governance 3-stream LIVE | ✅ Valid | Single curl is the integration test for convergence |

### ② Seven gates

| Gate | Claude | Our assessment | Action taken |
|------|--------|----------------|--------------|
| PB-9 | IN PROGRESS, blocks PB-8/10/12 | ✅ | OP-01/02/07 in action plan |
| PB-7 | CLEAN pending; waiver OK | ✅ with formal template | `PB7_WAIVER_TEMPLATE.md` |
| PB-8 | After PB-9 | ✅ | Phase 3 pre-flip |
| PB-10 | Clarify beta vs GA | ✅ **Defer for 0.x beta** | `PUBLIC_BETA_GO_NO_GO.md` § PB-10 |
| PB-6 | Partial; publish on flip | ⚠️ **Fix command** | Use `export_openapi.py` not raw curl to wrong path |
| security@ | 1 min human | ✅ | OP-06 |
| PB-12 | Human gate | ✅ | OP-10 |

**Reject:** Closing PB-10 in catalog pre-flip without maintainer catalog bump.

### ③ PB-9 soak plan

| Claude recommendation | Verdict | Implementation |
|----------------------|---------|----------------|
| Clarify gap | ✅ | Soak log § clock vs evidence |
| Day 14 template | ✅ | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| Persist log to repo | ✅ | `soak_staging.sh --repo-log` + `PB9_SOAK_ITERATION_LOG.md` |
| `tee` into soak log markdown | ❌ Reject | Corrupts human daily table — use separate iteration log |

### ④ PB-7 clean fork

| Claude content | Verdict |
|----------------|---------|
| WARM vs CLEAN distinction | ✅ Excellent — keep in all Claude sessions |
| VM / Codespaces options | ✅ Valid |
| `cd examples/minimal && cp .env` | ⚠️ `.env` optional — compose works without |
| `docker compose up` from minimal dir | ✅ OK — equivalent to `-f` from root |
| Codespaces chicken-egg | ✅ Valid — prefer local VM pre-flip |
| Waiver suggestion | ✅ — requires `PB7_WAIVER_TEMPLATE.md` sign-off |

### ⑤ PB-12 go/no-go draft

| Element | Verdict |
|---------|---------|
| Narrative structure | ✅ Adopted into `PUBLIC_BETA_GO_NO_GO.md` updates |
| PB-10 defer to GA | ✅ Policy — human must record at flip |
| Pre-flip `curl > docs/openapi.json` | ❌ **Wrong path** — `docs/openapi/openapi.json` via `export_openapi.py` |
| Tag `v0.1.0-rc.1` | ✅ Matches sprint plan |
| Release `v0.1.0-beta.1` | ✅ Standard 0.x naming |

### ⑥ Drift guard

All 10 items **confirmed** — no changes to drift list.

### ⑦ Next steps timeline

| Claude date | Assessment |
|-------------|------------|
| 06-27 gap clarify | ✅ Done in docs |
| 06-30–07-05 PB-7 | ✅ In action plan |
| ~07-06 Day 14 | ✅ Unchanged |
| ~07-07–09 pre-flip | ✅ Use export script |
| ~07-10 flip | ✅ Target — contingent on OP-07 PASS |

---

## Deeper perspectives (beyond Claude HTML)

### 1. Evidence architecture

Three layers now explicit:

1. **Calendar** — maintainer-approved soak start (06-22)
2. **Daily human** — `PB9_STAGING_SOAK_LOG.md` rows
3. **Machine hourly** — `PB9_SOAK_ITERATION_LOG.md`

ML5 requires layers 2+3; layer 1 alone is insufficient for audit.

### 2. Risk register @ flip

| Risk | Mitigation |
|------|------------|
| PB-7 not CLEAN | Waiver + 0.x disclaimer |
| PB-10 not started | Explicit GA deferral in go/no-go |
| PB-11 API 403 | Process-only until public |
| Gap 06-22→25 | Documented deploy deferral |

### 3. What Claude should not do

- Generate duplicate compose/CI/OpenAPI code
- Mark `gates_remaining` closed in catalog
- Accelerate PB-9 calendar
- Treat HTML "no code needed" as "no repo commits ever" — ops docs are commits

### 4. What Claude should do

- Fill Day 14 template when operator shares logs
- Draft PB-12 narrative from `PUBLIC_BETA_GO_NO_GO.md`
- PB-7 RUNBOOK Q&A on CLEAN machines
- Audit new prompts against § drift

---

## Wired artifacts (this reconciliation)

| File | Purpose |
|------|---------|
| [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) | Task register OP-01..11, CUR-01..02 |
| [`PB9_DAY14_REVIEW_TEMPLATE.md`](PB9_DAY14_REVIEW_TEMPLATE.md) | ~07-06 review |
| [`PB9_SOAK_ITERATION_LOG.md`](PB9_SOAK_ITERATION_LOG.md) | Hourly machine log |
| [`PB7_WAIVER_TEMPLATE.md`](practice-evidence/pb-7-clean-machine-fork/PB7_WAIVER_TEMPLATE.md) | Optional PB-7 bypass |
| `scripts/soak_staging.sh` | `--repo-log` flag |
| `scripts/restart_soak_loop.sh` | Enables repo log by default |

---

## Snapshot

In-repo copy: [`acp_status_audit_analysis.html`](acp_status_audit_analysis.html) (read-only reference).

**Drift:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) §11
