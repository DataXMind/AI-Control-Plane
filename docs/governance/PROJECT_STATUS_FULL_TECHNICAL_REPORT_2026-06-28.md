# AI Control Plane — Full Technical Status Report (Claude Handoff)

**Document ID:** ACP-GOV-PROJECT-FULL-TECH-REPORT-2026-06-28  
**Audience:** Claude (Anthropic) · maintainer · operator  
**Audit date:** 2026-06-28 (UTC)  
**Repository:** [DataXMind/AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane)  
**Baseline:** `master` @ **`20e4fc3`**  
**Governance catalog:** **v1.3.3** (`governance_catalog.py` · `GET /governance/status`)  
**Supersedes for handoff:** extends [`PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`](PROJECT_STATUS_AUDIT_FOR_CLAUDE.md) @ 2026-06-27 with post-wave evidence through 2026-06-28.

---

## 0. Audit methodology (strict)

| Layer | Source | Rule |
|-------|--------|------|
| **Runtime** | `curl /governance/status` · `verify_*_runtime.sh` | Trust over HTML/JSON samples |
| **Practice** | `practice-evidence/**/RESULTS.md` · operator artifacts | PASS/FAIL with path + date |
| **Catalog** | `governance_catalog.py` | `gates_remaining` until maintainer bump @ flip |
| **Calendar** | `PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` · `PB9_STAGING_SOAK_LOG.md` | PB-9 not PASS before ~2026-07-06 |
| **PACE** | Pause → Act → Check → Evolve per task | Evidence in Tier C paths, not chat |
| **Karpathy** | 6-layer governance · docs-only track until PB-9 Day 14 | No `src/` unless contract tests isolated |
| **Smoke** | `pytest -m smoke` 8 tests SMK-01..06c | Mandatory after API/`core/` touch |

**Drift guard:** Practice PASS ≠ auto-close `gates_remaining`. HTML Claude packets are **read-only snapshots** — reconcile via `*_RECONCILIATION.md`.

---

## 1. Executive summary

ACP has completed **engineering + governance documentation surface** for **0.x Public Beta**. Runtime (policy fail-closed, health, identity, governance UX, OpenAPI), CI (smoke + full suite + examples-minimal-smoke), legal artifacts, operator RUNBOOK, fork path (PB-7 CLEAN), security@ live test, release candidate tag, CHANGELOG body, and **dual-host PB-9 soak** (MSI + VPS) are **evidenced**.

**Critical path to public flip:** **PB-9 calendar only** → Day 14 review (~**2026-07-06**) → pre-flip refresh (~**2026-07-07**) → **PB-12 human GO** (~**2026-07-10**).

| Dimension | Status @ 2026-06-28 | Blocks PB-12 @ 0.x? |
|-----------|---------------------|---------------------|
| Milestones A, B, C, C+ | ✅ CLOSED | No |
| Public Beta engineering (PB-T) | ✅ DONE (#116–#118) | No |
| PB-7 CLEAN fork ≤15 min | ✅ PASS practice | No (catalog lists until bump) |
| security@ live | ✅ PASS | No |
| PB-8 `v0.1.0-rc.1` | ✅ @ `c58b4cc` (early) | No |
| CHANGELOG `0.1.0-rc.1` | ✅ merged #120 | No |
| go/no-go practice sync | ✅ merged #119 | No |
| PB-9 staging soak | 🔄 IN PROGRESS | **Yes** until Day 14 PASS |
| PB-12 human go/no-go | ⏳ ~07-10 | **Yes** |
| PB-10 production 30d | ❌ **Deferred GA** (#78 post-flip) | **No** @ 0.x beta |
| PB-11 branch protection API | Process-only (403) | No @ 0.x |

**pytest @ `20e4fc3`:** **177** collected · smoke **8/8** (SMK-01..06c) — re-verified 2026-06-28 MSI WSL @ `10:25Z`

---

## 2. Immediate actions — what Cursor can vs cannot do

### 2.1 ✅ Done by Cursor/operator (2026-06-27 → 28)

| Item | Evidence |
|------|----------|
| OpenAPI verify fix (`1d883ec`) | PR #118 |
| PB-7 CLEAN PASS | `pb-7-clean-machine-fork/RESULTS.md` |
| security@ PASS | `security-email-live-test/RESULTS.md` |
| CUR-04 VPS `--repo-log` + hourly verify | `vps-hourly-loop-verify-2026-06-28.md` |
| go-no-go + CHANGELOG | PR #119, #120 |
| Session anchor sync | `SESSION_ANCHOR_TEMPLATE.md` @ `20e4fc3` |
| This report | This file |

### 2.2 🔄 Operator only — NOW (continuous)

| ID | Action | Trigger |
|----|--------|---------|
| OP-01 | Daily PB-9 tick | *"đã tick ngày YYYY-MM-DD"* after 00:00 UTC |
| OP-02 | Maintain soak MSI + VPS | `restart_soak_loop.sh` · `acp-soak.service` |
| — | `git pull` on VPS/MSI | After doc commits (no restart if docs-only) |

### 2.3 ⏳ WAIT — calendar / human

| ID | Action | Target |
|----|--------|--------|
| OP-07 | Day 14 PB-9 review → `RESULTS.md` | ~**2026-07-06** |
| OP-09 | `export_openapi.py` commit if diff | ~**2026-07-07** post Day 14 |
| OP-10 | PB-12 public flip + **operator signature** | ~**2026-07-10** |
| OP-11 | PB-10 / #78 GA soak 30d | **After flip** |
| — | `governance_catalog.py` bump | Maintainer @ flip |

### 2.4 ❌ Cursor must NOT do now

- Close `gates_remaining` in catalog without maintainer
- Tick PB-9 future dates · claim PB-9 PASS before Day 14
- Re-tag `v0.1.0-rc.1` · public flip · start PB-10 pre-flip
- New `src/` feature work (Karpathy: docs-only track through PB-9 review)

---

## 3. Milestone & phase history (project start → present)

### 3.1 GitHub milestones (CLOSED)

| Milestone | Scope | Closed | Evidence |
|-----------|-------|--------|----------|
| **A** | PoC: core, api, mcp, cli | 2026-06-23 (#38) | ARCHITECTURE §Execution |
| **B** | Redis, persistence, CLI live | 2026-06-24 (PR #51) | Integration tests |
| **C** | SAPAL MVP, apex, telemetry file | 2026-06-24 (PR #63) | 156→177 pytest growth |
| **C+** | Governance depth, studies wiring | 2026-06-24 (PR #74) | Catalog convergence |

### 3.2 Public Beta sprint (IN_PROGRESS)

| Phase | Dates | Status |
|-------|-------|--------|
| Prep wave (legal, examples, OpenAPI CI) | 2026-06-24 → 27 | ✅ |
| Soak clock approve | 2026-06-22 | ✅ [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) |
| Evidence window | from 2026-06-26 | MSI + VPS logs |
| Day 14 review | ~2026-07-06 | ⏳ |
| Pre-flip | ~2026-07-07 | ⏳ |
| PB-12 flip | ~2026-07-10 | ⏳ human |
| GA / PB-10 | post-flip | ⏳ #78 |

### 3.3 OPEN_SOURCE_READINESS visibility phases

| Phase | Name | Status |
|-------|------|--------|
| 0 | Private build | ✅ complete |
| 1 | Trusted preview | ✅ studies / VPS |
| 2 | **Public beta 0.x** | 🔄 **IN_PROGRESS** (PB-9) |
| 3 | GA PyPI `1.0.0` | ⏳ post PB-10 |

---

## 4. Pipeline & roadmap (canonical)

```text
[DONE]  Milestones A → C+
[DONE]  PB-1..6, PB-7 practice, PB-8 tag, security@, #119/#120, CUR-01..04
[NOW]   PB-9 soak — ticks through 2026-06-28 · MSI + VPS hourly PASS
[WAIT]  ~07-06  OP-07 Day 14 → close #77 if PASS
[WAIT]  ~07-07  OP-09 export refresh · smoke + verify
[WAIT]  ~07-10  OP-10 PB-12 GO + operator signature (PB-10 defer in record)
[POST]  PB-10 / #78 production soak 30d → GA 1.0.0
```

**Target release:** `v0.1.0-beta.1` from existing `v0.1.0-rc.1` @ `c58b4cc`.

---

## 5. PB-1..12 gate matrix (practice vs catalog)

> Runtime `GET /governance/status` → `public_beta.gates_remaining` = **7** until flip bump.

| ID | Gate | Practice @ 2026-06-28 | In `gates_remaining` | Blocks 0.x flip? |
|----|------|-------------------------|----------------------|------------------|
| PB-1..4 | Legal | ✅ | closed (PB-11) | No |
| PB-5 | examples/minimal | ✅ CI smoke | — | No |
| PB-6 | OpenAPI runtime + static | ✅ synced; publish prominence @ flip | Yes | No (refresh only) |
| PB-7 | CLEAN fork ≤15 min | ✅ 2026-06-27 | Yes | No |
| PB-8 | rc.1 tag | ✅ `c58b4cc` 2026-06-28 | Yes | No |
| PB-9 | Staging soak ≥14d | 🔄 ticks 26–28 | Yes | **Yes** |
| PB-10 | Prod soak 30d | Deferred GA | Yes | **No** @ 0.x |
| PB-11 | Branch protection | Process-only | — | No |
| security@ | Live test | ✅ 2026-06-28 | Yes | No |
| PB-12 | Human go/no-go | ⏳ | Yes | **Yes** |

---

## 6. PB-9 soak state (no Scenario B/C fork)

| Concept | Value | SSOT |
|---------|-------|------|
| Calendar start | 2026-06-22 | `soak_started` |
| Day 14 review | ~2026-07-06 | calendar from approve |
| First machine evidence | 2026-06-26 | iteration logs |
| Gap 06-22→25 | Deploy deferred; SEV=0 | `PB9_STAGING_SOAK_LOG.md` § clock |
| Daily ticks | 26, 27, **28** | human table |
| MSI machine log | `PB9_SOAK_ITERATION_LOG.md` | 11 iterations through `10:20Z` 28/06 |
| VPS machine log | `vps-soak-iteration.log` + `/var/log/` | CUR-04 hourly PASS 08:29/09:29Z |

**Reject:** Claude Scenario B (Day 14 = 07-10) or C unless new SEV-1/2 after 2026-06-28.

---

## 7. Operator task register (OP / CUR)

| ID | Task | Status | Artifact |
|----|------|--------|----------|
| OP-01 | Daily PB-9 tick | 🔄 | `PB9_STAGING_SOAK_LOG.md` |
| OP-02 | Soak loop + logs | ✅ | `vps-hourly-loop-verify-2026-06-28.md` |
| OP-03 | Gap 06-22→25 | ✅ | soak log § clock |
| OP-04 | PB-7 CLEAN | ✅ | `pb-7-clean-machine-fork/RESULTS.md` |
| OP-05 | PB-7 waiver | ❌ cancelled | — |
| OP-06a/b | security@ | ✅ | `security-email-live-test/` |
| OP-07 | Day 14 review | ⏳ ~07-06 | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| OP-08 | PB-8 tag | ✅ early | `c58b4cc` |
| OP-09 | PB-6 export refresh | ⏳ pre-flip | `export_openapi.py` |
| OP-10 | PB-12 GO | ⏳ ~07-10 | human signature |
| OP-11 | PB-10 GA | ❌ deferred | #78 post-flip |
| CUR-01..04 | Soak persistence / VPS | ✅ | scripts + systemd |

Full detail: [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md).

---

## 8. Practice evidence index (Studies + ops)

| Study / pack | Status | Path |
|--------------|--------|------|
| 01 Profile A | ✅ | `study-01-profile-a/RESULTS.md` |
| 02 Profile B | ✅ | `study-02-profile-b/RESULTS.md` |
| 03 Profile C | ✅ | `study-03-profile-c/RESULTS.md` |
| 04 Ops edge | ✅ | `study-04-ops-edge/RESULTS.md` |
| 05 Advanced | ✅ | `study-05-advanced-surprises/RESULTS.md` |
| 06 Multi-host | ✅ | `study-06-multi-host/RESULTS.md` |
| 07 Cross-network | ✅ | `study-07-cross-network/RESULTS.md` |
| 08 Shipped remote | ✅ | `study-08-shipped-remote/RESULTS.md` |
| Governance v1.3.3 verify | ✅ | `governance-status-v13-verify/RESULTS.md` |
| PB-7 CLEAN | ✅ | `pb-7-clean-machine-fork/RESULTS.md` |
| security@ | ✅ | `security-email-live-test/RESULTS.md` |
| PB-9 Day 14 (pending) | ⏳ | `pb-9-day14-review/` (no `RESULTS.md` yet) |

`practice_evidence.studies_completed: 8` @ catalog.

---

## 9. Verification gates (PACE / Smoke / Karpathy / DEVELOPMENT_PROTOCOL)

### 9.1 Smoke gate (8 tests) — SMK-01..06c

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
```

| When verified | Host | Result |
|---------------|------|--------|
| 2026-06-28 | MSI WSL | **8/8 PASS** (~1.6s, `.venv`, ~10:25Z) |
| CI | GitHub Actions | `Smoke gate` job |

### 9.2 Runtime verify (L5)

```bash
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh   # 1.3.3 · 13 patterns
bash scripts/verify_openapi_runtime.sh               # 3.1.0 · 13 paths
```

| When | Host | Result |
|------|------|--------|
| 2026-06-28 | MSI WSL | governance ✅ · OpenAPI ✅ |
| 2026-06-26+ | VPS | governance 1.3.3 ✅ |

### 9.3 Full CI gate chain (DEVELOPMENT_PROTOCOL §5.4–5.5)

```text
L1 ruff → L2 mypy --strict → L3 pytest (177) → L4 integration → SMK smoke 8/8
```

Plus: `examples-minimal-smoke` · `shipped_config` parity · governance-memory CI.

### 9.4 Karpathy 6-layer (governance track)

| Layer | ACP implementation | Status |
|-------|-------------------|--------|
| L0 | `.cursorrules`, AGENTS.md, assumptions | ✅ |
| L1 | ARCHITECTURE, DATA_CLASSIFICATION | ✅ |
| L2 | CURSOR_RISK_POLICY.md | ✅ |
| L3 | Branch PR-only, file allowlists | ✅ process |
| L4 | ruff, mypy, pytest, smoke, verify scripts | ✅ |
| L5 | LESSONS P-01..13, session anchor, practice-evidence | ✅ ML5 |

**Rule:** Governance PRs = **docs + CI tests only** until PB-9 Day 14 PASS (~07-06).

### 9.5 PACE evidence (recent)

| Pack | P | A | C | E |
|------|---|---|---|---|
| CUR-04 VPS soak | separate path | unit + docs | smoke 8/8 | artifacts |
| #119 go-no-go | practice vs catalog | doc sync | — | merged |
| #120 CHANGELOG | audit draft | expand file | smoke | merged |
| VPS hourly | — | operator run | dual log | `vps-hourly-loop-verify` |

---

## 10. Engineering surface (frozen for beta)

| Module | Contract |
|--------|----------|
| `POST /policy/evaluate` | Fail-closed deny + reason |
| `GET /health` | config_loaded, rules, agents |
| `GET /governance/status` | catalog v1.3.3 mirror |
| OpenAPI | `docs/openapi/openapi.json` + `/openapi.json` runtime |
| `examples/minimal/` | PB-9 staging parity stack |
| Identity | SMK-06/06b/06c — 401 contract |

**Known 0.x limitations:** `apex/learn.py` empty proposals; MCP cyanheads E2E not CI; OTel stub; branch protection process-only.

---

## 11. Manual items requiring human action

| # | Item | Owner | When | Notes |
|---|------|-------|------|-------|
| 1 | PB-9 daily ticks 29/06 → 05/07 | Operator | Daily UTC | Chat: *"đã tick ngày …"* |
| 2 | Day 14 verdict + sign-off | Operator | ~07-06 | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| 3 | PB-12 **GO** + operator signature | Maintainer | ~07-10 | Include PB-10 defer text from go-no-go |
| 4 | GitHub public visibility | Org admin | @ PB-12 | Release `v0.1.0-beta.1` |
| 5 | Catalog `gates_remaining` bump | Maintainer | @ flip | Practice ≠ auto-close |
| 6 | PB-10 clock start | Operator | Post-flip | Issue #78 |
| 7 | Branch protection API | Org | Post-public or Team plan | PB-11 |

---

## 12. Claude session instructions

### 12.1 Read first (in order)

1. This report (`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`)
2. [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md) — canonical one-liner @ `20e4fc3`
3. [`CLAUDE_PROJECT_SETUP.md`](../prompts/CLAUDE_PROJECT_SETUP.md) — Claude Projects on claude.ai
4. [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)
5. [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)
6. `governance_catalog.py` + `GET /governance/status`

### 12.2 Claude role NOW → PB-12

| Do | Don't |
|----|-------|
| Q&A on Day 14 prep · soak logs | Generate new feature `src/` code |
| Draft PB-12 narrative support | Close catalog gates |
| Doc drift fixes (LOW) | Accelerate PB-9 calendar |
| Audit new HTML vs reconciliation | Copy stale HTML SHA/165 tests |
| Help fill `RESULTS.md` when operator shares logs | Claim PB-9 PASS before 07-06 |

### 12.3 Drift — reject claims

- `examples/docker-compose.yml` → `examples/minimal/docker-compose.yml`
- `examples-smoke` → `examples-minimal-smoke`
- `"165 tests"` → **177** @ `20e4fc3`
- `"PB-9 only gate"` → **7** `gates_remaining`
- MSI WARM = PB-7 PASS
- PB-10 blocks PB-12 @ 0.x beta
- `curl > docs/openapi.json` → `export_openapi.py` → `docs/openapi/openapi.json`
- Scenario B/C default for Day 14 date

---

## 13. Key commits & PRs (wave reference)

| Ref | Summary |
|-----|---------|
| `1d883ec` | OpenAPI verify `/openapi.json` fix |
| #118 | OpenAPI + examples CI merge |
| `fa71bd5` | PB-7 CLEAN evidence |
| `c58b4cc` | security@ PASS · tag `v0.1.0-rc.1` |
| `e76d203` | CUR-04 VPS soak parity |
| #119 | go-no-go practice sync |
| #120 | CHANGELOG expand |
| `20e4fc3` | Full technical audit report + second-pass drift fixes |
| `ac5f017` | VPS hourly verify + session anchor |

---

## 14. Second-pass audit (2026-06-28) — gaps, drift, surprises

### 14.1 Fixed in this wave

| Finding | Severity | Action |
|---------|----------|--------|
| `README.md` still **165** pytest (user-facing) | **HIGH** | → **177** + link to full report |
| `PROJECT_STATUS_AUDIT_FOR_CLAUDE.md` §5/8/10/11 stale (PB-7 ⏳, SHA `527eb5d`) | **HIGH** | Synced to practice @ 28/06 |
| `PB9_DAY14_REVIEW_TEMPLATE` "proceed PB-8" after tag done | **MED** | → PB-12 prep only |
| Sprint plan / TASK_AUDIT baseline SHA vague | **LOW** | → `20e4fc3` |
| Session anchor / operator plan | **LOW** | Patched in this wave |

### 14.2 By design — not bugs (document for Claude)

| Item | Explanation |
|------|-------------|
| `gates_remaining` lists PB-7, PB-8, security@ despite practice PASS | Maintainer catalog bump only @ PB-12 flip |
| Exact runtime list (7) | `PB-9`, `PB-7`, `PB-10`, `PB-6 publish`, `PB-8 tag`, `security@`, `PB-12` |
| `known_gaps` OPEN | **G-05 only** (PB-9 calendar) |
| PB-8 tag **early** @ `c58b4cc` | Human-approved; **do not re-tag** |
| PB-10 in `gates_remaining` | **Does not block** 0.x beta — deferred GA #78 |

### 14.3 Intentional snapshots — do not edit HTML

| Artifact | Stale content | Reconcile via |
|----------|---------------|---------------|
| `acp_status_audit_analysis.html` | 165 tests; PB-8 blocks PB-9 | `ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md` |
| `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` (Claude UI) | `527eb5d`, 165 tests, PB-7/8/security@ open | [`HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md`](HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md) |
| `karpathy_acp_rearchitecture_analysis.html` | 156 tests | `*_SNAPSHOT_README.md` |
| `pb_final_blockers_packet.html` | Pre-PB-7 era | `PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md` |

### 14.4 Operational surprises / watch items

| Item | Risk | Mitigation |
|------|------|------------|
| Smoke without `.venv` on MSI | False `ModuleNotFoundError` | `source .venv/bin/activate` |
| VPS @ `98f193c` until pull | Host doc drift | `git pull` after this commit — no soak restart |
| `nohup.out` in repo root | Accidental artifact | Do not commit |
| Three soak evidence layers | Conflation risk | Human table · MSI log · VPS log |

### 14.5 Re-verification stamp

```text
pytest --collect-only  → 177 tests (MSI WSL .venv, 2026-06-28 ~10:25Z)
pytest -m smoke        → 8 passed, 1 warning (~1.6s)
```

---

## 15. Sign-off

| Field | Value |
|-------|-------|
| Report prepared | Cursor operator session |
| Audit strictness | Practice + catalog + calendar cross-check |
| Next mandatory gate | **OP-07 Day 14 ~2026-07-06** |
| Public flip target | **~2026-07-10** contingent on OP-07 PASS + OP-10 human GO |

**Related:** [`TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) · [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

**Last updated:** 2026-06-28 @ `20e4fc3`
