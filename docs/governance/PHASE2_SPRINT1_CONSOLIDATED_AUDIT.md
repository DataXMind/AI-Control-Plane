# Phase 2 Sprint 1 — Consolidated Audit

**Document ID:** ACP-GOV-PHASE2-S1-AUDIT  
**Version:** 1.0  
**Date:** 2026-06-22  
**Sources:**

| Source | Role |
|--------|------|
| `phase2_execution_completion.html` (Claude artifact) | Planned pipeline, Cursor rules, master checklist |
| Prior Cursor audit (2026-06-22) | Harsh repo/state verification |
| `docs/DEVELOPMENT_PROTOCOL.md` v1.3 | Protocol truth |
| `origin/master` @ `7f5dcd5` | Production branch state |
| Branch `phase2/p2-0-tool-naming-and-p2-2` @ `43dfe1e` | Sprint 1 work-in-flight |

**Related:** [`PHASE2_SPRINT1_REPORT.md`](PHASE2_SPRINT1_REPORT.md) · [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md) · [`PHASE1_REPORT_V2.md`](PHASE1_REPORT_V2.md)

---

## 1. Executive verdict

| Dimension | Artifact claim | Reality (verified) | Match |
|-----------|----------------|-------------------|-------|
| Sprint 1 code complete | Steps 3–6 done | **Yes on branch** | ⚠️ Partial |
| Sprint 1 closed | Step 7 + 100% checklist | **Docs on branch; code not on master** | ❌ |
| Pipeline (1 task = 1 PR) | Rule 1 enforced | **Violated** — monolithic branch + partial merges | ❌ |
| Master gates | SMK 6/6 · ≥70% cov · 123 tests | **Branch only**; master ≈91 tests · SMK 5/5 | ❌ |
| GitHub issue sync | Close #8, #35, GAP-ABAC-2 | **#8, #35, #45 still OPEN** | ❌ |
| Technical quality (branch) | — | 123 pass · 82% cov · invariants OK | ✅ |

**One-line verdict:** Implementation quality on branch is **good**; governance/process state is **not Sprint-1-complete** until MB-S1-1..5 merge to `master` and issues/docs sync.

---

## 2. Artifact analysis — `phase2_execution_completion.html`

### 2.1 Purpose (5 tabs)

| Tab | Intent |
|-----|--------|
| Quy tắc Cursor | 5 rules: 1 branch/PR, @file refs, verify before commit, models.py only, fresh context |
| Flow Sprint 1 | Steps 0–7 linear pipeline from `master @ 83e3ab5` |
| Tín hiệu | Good / fix / reject patterns for Cursor output |
| Step 7 Archive | Docs-only after **all MB-S1 PRs merged** |
| Master checklist | 47 tick items = Definition of Done Sprint 1 |

### 2.2 Planned pipeline (artifact)

```text
master @ 83e3ab5
  → STEP 1  phase2/p2-0-tool-naming-and-p2-2     (PR merge)
  → STEP 2  phase2/p2-1-pii-gap-doc               (PR merge)
  → STEP 3  milestone-b/s1-1-guardrails           (PR merge)
  → STEP 4  milestone-b/s1-2-abac-full            (PR merge)
  → STEP 5a milestone-b/s1-3-coverage             (PR merge, before 5b)
  → STEP 5b milestone-b/s1-4-cli-tests            (PR merge)
  → STEP 6  milestone-b/s1-5-identity-jwt         (PR merge)
  → STEP 7  phase2/governance-archive             (PR merge)
  → SPRINT 1 DONE
```

### 2.3 Actual pipeline (verified)

```text
master @ 83e3ab5
  → PR #44 merge: dc83c2f (P2-0 only)                    ✅
  → PR #46 merge: 42b8366 (P2-1 doc) + 4bb2c70 (agent4)  ⚠️ wrong scope/timing
  → 8 commits remain on branch (7693c00 … 43dfe1e)         ❌ not merged
     includes MB-S1-1..5 + Step 7 report
```

**Critical ordering bug:** `agent4` (data-analyst, PII restrictions) merged to `master` **before** ABAC `role_not_in` code (MB-S1-2) exists on `master`.

---

## 3. Master checklist — item-by-item verification

Legend: **✅** done & on correct branch · **⚠️** done on branch only or partial · **❌** not done or wrong · **N/A** cannot verify

### 3.1 Pre-sprint (3 items)

| # | Checklist item | Status | Evidence / gap |
|---|----------------|--------|----------------|
| P1 | Codecov token + secret | N/A | Assumed per PHASE1_REPORT §8; not re-verified |
| P2 | master @ 83e3ab5 baseline gates | ✅ | Was true at sprint start |
| P3 | Approve MB Sprint 1 scope (5 issues) | N/A | Process assumption |

### 3.2 P2 prep — Steps 1–2 (13 items)

| # | Checklist item | Branch | master | Notes |
|---|----------------|--------|--------|-------|
| 1 | Branch `phase2/p2-0-tool-naming-and-p2-2` | ✅ | ✅ | Used for entire sprint — **violates Rule 1** for Steps 2–7 |
| 2 | `core/tool_names.py` + 2 functions | ✅ | ✅ | PR #44 |
| 3 | `loader.py` no duplicate `normalize_tool_name` | ✅ | ✅ | Grep: no local def |
| 4 | `mcp/git_server.py` imports from `tool_names` | ✅ | ✅ | |
| 5 | `api/server.py` uses `resolve_policy_tool_name` | ✅ | ✅ | |
| 6 | ARCHITECTURE §Tool naming | ✅ | ✅ | |
| 7 | DEVELOPMENT_PROTOCOL P0-2b = CLOSED | ✅ | ✅ | |
| 8 | Gate: 91 · SMK 5/5 · parity 4 · ruff · mypy | ✅ | ✅ | At P2-0 merge time |
| 9 | PR merged · **#8 closed** · D3 closed | ⚠️ | ❌ | PR #44 merged; **#8 still OPEN** (S3a tool adapter) |
| 10 | Branch `phase2/p2-1-pii-gap-doc` | ❌ | — | Never created; P2-1 on same branch |
| 11 | ARCHITECTURE §Policy YAML loading | ✅ | ✅ | On master via PR #46 |
| 12 | GitHub GAP-ABAC-2 issue created | ✅ | ✅ | **#45 exists** |
| 13 | P2-1 PR merged · 91 tests pass | ⚠️ | ⚠️ | Merged via PR #46; issue **not closed** |

### 3.3 Milestone B Sprint 1 — Steps 3–6 (29 items)

| # | Checklist item | Branch @ 43dfe1e | master @ 7f5dcd5 |
|---|----------------|------------------|------------------|
| 14 | Branch `milestone-b/s1-1-guardrails` | ❌ | — | Not separate branch |
| 15 | `KillSwitch` in `core/models.py` + `__all__` | ✅ | ❌ | |
| 16 | `load_guardrails()` + `load_kill_switch()` | ✅ | ❌ | |
| 17 | `PolicyEngine` accepts `kill_switch` | ✅ | ❌ | |
| 18 | `create_app()` wires guardrails + kill_switch | ✅ | ❌ | |
| 19 | Fixture policies.yml guardrails + kill_switch | ✅ | ❌ | |
| 20 | `test_guardrails.py` — **5 tests** pass | ⚠️ **6 tests** | ❌ | Count exceeds plan (OK) |
| 21 | Gate 96+ · SMK 5/5 · PR merged | ⚠️ 123 pass | ❌ | **#35 MB7 still OPEN** |
| 22 | Branch `milestone-b/s1-2-abac-full` | ❌ | — | |
| 23 | `eval_role_not_in()` | ✅ | ❌ | |
| 24 | `eval_approval_status()` | ✅ | ❌ | |
| 25 | `eval_read_only()` | ✅ | ❌ | |
| 26 | `load_policies()` loads ABAC keys | ✅ | ❌ | |
| 27 | `test_policies.py` regression + new cases | ✅ | ❌ | |
| 28 | Gate · PR merged | ⚠️ | ❌ | **#45 still OPEN** |
| 29 | `policies.py` coverage ≥ 80% | ✅ **99%** | ❌ | |
| 30 | `fail_under = 70` in pyproject.toml | ✅ | ❌ | |
| 31 | Total coverage ≥ 70% | ✅ **82%** | ~64–70% | |
| 32 | `test_cli_assign.py` 3 cases | ✅ | ❌ | |
| 33 | `test_cli_status.py` 1 case | ✅ | ❌ | |
| 34 | cli/ coverage ≥ 60% | ⚠️ **~67–68%** | ❌ | assign/status only |
| 35 | Invariant #4 intact | ✅ | ✅ | No `core.policies` in cli |
| 36 | 5a+5b PRs merged (5a first) | ❌ | — | Single branch, no PRs |
| 37 | Branch `milestone-b/s1-5-identity-jwt` | ❌ | — | |
| 38 | `core/identity.py` HS256 stub | ✅ | ❌ | File absent on master |
| 39 | `/identity/verify` invalid/unknown → 401 | ✅ | ❌ | |
| 40 | SMK-06a + SMK-06b in test_smoke | ✅ | ❌ | Also **SMK-06c** (unknown agent) |
| 41 | ARCHITECTURE identity 401 vs policy 200+deny | ✅ | ❌ | |
| 42 | DEVELOPMENT_PROTOCOL SMK matrix 01..06 | ✅ | ⚠️ | master protocol lacks Sprint 1 merges |
| 43 | Gate SMK 6/6 · PR merged | ⚠️ **8 smoke tests** | ❌ | master has no SMK-06 |

### 3.4 Close — Step 7 (5 items)

| # | Checklist item | Status | Notes |
|---|----------------|--------|-------|
| 44 | `docs/governance/` HTML archives | ✅ | Already archived Milestone A; Step 7 skipped move |
| 45 | `PHASE2_SPRINT1_REPORT.md` | ⚠️ | Created on branch; close commit should be **post-merge SHA** |
| 46 | `MILESTONE_B_BACKLOG.md` Sprint 1 DONE | ⚠️ | On branch only |
| 47 | pytest pass after archive · PR merged | ⚠️ | 123 pass branch; **PR not merged** |
| 48 | SPRINT 1 COMPLETE 100% | ❌ | **Step 7 ran before MB-S1 PRs on master** — violates artifact tab Archive |

### 3.5 Checklist score

| Section | Done (branch) | Done (master) | Total items |
|---------|---------------|---------------|-------------|
| Pre-sprint | 1 verified | 1 | 3 |
| P2 Steps 1–2 | 11 | 9 | 13 |
| MB Steps 3–6 | 26 | 0 | 29 |
| Step 7 close | 2 | 0 | 5 |
| **Approx.** | **~40/47 (85%)** | **~10/47 (21%)** | **47** |

---

## 4. Phase & target alignment

### 4.1 Project phases (from OPEN_SOURCE_READINESS + protocol)

| Phase | Target | Sprint 1 contribution | Gap |
|-------|--------|----------------------|-----|
| Milestone A | PoC scaffold | Already closed #38 | — |
| Phase 2 entry | P0-2b tool naming | ✅ on master | #8 not closed |
| Milestone B Sprint 1 | Guardrails, ABAC, cov, CLI tests, JWT stub | ✅ branch / ❌ master | **Merge blocker** |
| Milestone B Sprint 2 | Redis, CLI live, MCP factory | Not started | #29–34 open |
| Milestone C | apex SAPAL | Stubs only | #37 open |
| Public Beta | Legal, soak, OpenAPI | Far | — |

### 4.2 Sprint 1 vs Milestone B scope

Sprint 1 ≈ **40–50% of Milestone B** (loader/governance path). Remaining MB: persistence, Redis quota, CLI approve/quota/logs, MCP HTTP, apex.

### 4.3 Artifact rules vs execution

| Rule | Planned | Actual | Severity |
|------|---------|--------|----------|
| Rule 1: 1 task = 1 branch = 1 PR | 7 PRs | 2 merged PRs + 8 commits unpushed to master | **Critical** |
| Rule 3: Human verify before commit | Human runs gates | Gates passed locally (123/8/4) | OK |
| Rule 4: Types in models.py | KillSwitch in models.py | ✅ `KillSwitch` in `models.py` | OK |
| Step 7 timing | After all MB PRs merged | Ran on branch **before** master merge | **Critical** |
| Reject signals (identity 401, kill_switch 200+deny) | — | Implementation matches reject rules on branch | OK |

---

## 5. Technical audit (branch @ 43dfe1e) — merged with prior review

### 5.1 Gates (local WSL venv)

| Gate | Result |
|------|--------|
| pytest full | 123 pass |
| smoke | 8 pass (SMK-01..06 incl. 06b, 06c) |
| shipped_config parity | 4 pass |
| coverage | 82.16% (fail_under 70) |
| ruff + mypy --strict | clean |

### 5.2 Strengths

- 8 invariants intact; CLI HTTP-only; MCP facade; fail-closed policy path
- `policies.py` 99%; guardrails + kill_switch wired; ABAC condition adapter complete
- Identity contract: auth fail → 401 (distinct from policy 200+deny)
- Tool naming Option A centralized in `core/tool_names.py`

### 5.3 Residual risks (post-merge recommendations)

| Risk | Detail | Priority |
|------|--------|----------|
| Shipped PII parity gap | `config/policies.yml` has `role_not_in`; no shipped test for Restrict-PII exemption | P1 |
| Fixture vs shipped drift | Fixture Restrict-PII lacks `role_not_in` (intentional regression) — document clearly | P2 |
| Issue drift | #8, #35, #45 open despite code done | P0 process |
| `PHASE1_REPORT_V2.md` stale | §4.2 still lists closed gaps as open | P1 docs |
| Weak coverage pockets | `mcp/git_server.py` 53%; `cli/main.py` 0% | P2 Sprint 2 |
| JWT production readiness | HS256 stub only; JWKS deferred Milestone C | Expected |
| `agent4` on master early | Config ahead of ABAC enforcement on master | **P0 until merge** |

---

## 6. Consolidated action list (before declaring Sprint 1 DONE)

### 6.1 Blockers (must do)

1. **Open PR** branch → `master`: 8 commits (`7693c00` … `43dfe1e`); title reflects MB-S1-1..5 + governance close.
2. **CI green** on that PR (Smoke + Full suite + shipped parity).
3. **Close or comment** GitHub: #35 (MB7), #45 (GAP-ABAC-2), #8 (S3a) with merge SHA evidence.
4. **Update** `PHASE2_SPRINT1_REPORT.md` close commit = merge commit on `master` (not `41ccf65`).

### 6.2 Strongly recommended (same PR or immediate follow-up)

5. Add `test_shipped_config_parity.py` case: Restrict-PII + `role_not_in: reviewer` on shipped config.
6. Update `PHASE1_REPORT_V2.md` §4.2 → move GAP-GR-*, GAP-ABAC-*, GAP-ID-1 to closed.
7. Sync `DEVELOPMENT_PROTOCOL.md` §4.1 smoke count (8 tests / SMK-06) on master after merge.

### 6.3 Process fixes (Sprint 2 onward)

8. Enforce Rule 1: one branch per MB task; no config scope creep in doc-only PRs.
9. Do not run Step 7 “Sprint closed” until merge SHA exists on `master`.
10. Evolve step: every task closes/links GitHub issue in same PR.

---

## 7. Sign-off matrix

| Stakeholder | Sprint 1 code | Sprint 1 process | Ready for master merge |
|-------------|---------------|------------------|------------------------|
| Cursor executor | ✅ branch | ❌ pipeline drift | **Conditional** — merge pending |
| Claude architect artifact | Defines correct DoD | Execution deviated | Checklist **21% on master** |
| Human maintainer | — | Must approve PR + issue close | **Action required** |

---

**Last updated:** 2026-06-22  
**Next action:** PR `phase2/p2-0-tool-naming-and-p2-2` → `master` (8 commits) + issue hygiene + optional shipped PII test.
