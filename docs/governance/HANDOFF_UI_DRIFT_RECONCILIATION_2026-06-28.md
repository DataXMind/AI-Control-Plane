# Claude UI Handoff — drift reconciliation

**Document ID:** ACP-GOV-HANDOFF-UI-DRIFT-RECON-2026-06-28  
**Audit date:** 2026-06-28 (UTC)  
**Rejected source:** `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` (Claude Sonnet UI export)  
**Source metadata:** audit 2026-06-27 · baseline `527eb5d` · catalog v1.3.3  
**Canonical repo SSOT:** `master` @ **`47cb630`** · catalog **v1.3.3**  
**Companion:** [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md) · [`CLAUDE_PROJECT_SETUP.md`](../prompts/CLAUDE_PROJECT_SETUP.md)

> **Use:** Claude Projects must **not** treat the UI handoff as ops SSOT. Use this reconciliation + repo knowledge files. Architecture sections of the UI handoff remain useful as **reference only**.

---

## 1. Executive verdict

| Layer | UI handoff @ `527eb5d` | Repo @ `47cb630` (Cursor + operator) |
|-------|------------------------|--------------------------------------|
| Architecture (Parts 2–9, 15) | ~90% accurate | Still valid — cite repo for test counts |
| Ops / gates / timeline (Parts 1, 10–14, 17–18) | **STALE** | Superseded by FULL report + operator docs |
| **Recommendation** | Appendix only | **Reject** as primary knowledge upload |

```text
UI handoff frozen @ 2026-06-27 / 527eb5d
Cursor wave through 2026-06-28: PB-7, security@, PB-8, #119/#120,
  CUR-04 VPS soak, full audit, manual playbook → 47cb630
```

---

## 2. Canonical one-liner (replace UI Part 1)

```text
AI Control Plane @ master 47cb630: Milestones A–C+ CLOSED.
Public Beta IN_PROGRESS (PB-9 soak). Catalog v1.3.3 live.
Practice: PB-7 PASS · security@ PASS · tag v0.1.0-rc.1 @ c58b4cc · CHANGELOG/go-no-go #119/#120.
Runtime: 7 gates_remaining until maintainer bump @ PB-12 flip.
Critical path: PB-9 daily tick → Day 14 ~2026-07-06 → PB-12 ~2026-07-10.
PB-10 deferred GA (#78 post-flip). 177 pytest · smoke 8/8.
Trust verify_* scripts — not stale UI handoff @ 527eb5d.
```

---

## 3. Critical drift (reject in Claude Project)

### 3.1 Baseline & metadata

| UI handoff | Correct @ 2026-06-28 |
|------------|----------------------|
| `master @ 527eb5d` | **`master @ 47cb630`** (pull before cite) |
| Audit date 2026-06-27 only | Evidence through **2026-06-28** + commits below |

### 3.2 Test count (multiple UI sections)

| UI claim | Correct |
|--------|---------|
| 165 pytest (MC-11, CI, L4, drift table) | **177** pytest @ `47cb630` |
| Drift: "156 → 165" | **177** @ master (`pytest tests/ --collect-only -q`) |
| Smoke | **8/8** SMK-01..06c — unchanged |

### 3.3 Milestone C+

| UI Part 5 | Correct |
|-----------|---------|
| "Milestone C+ (not started — next after PB)" | **CLOSED** — PR #74 · governance depth |

### 3.4 Gates — practice vs UI `gates_remaining` table (Part 10.1)

> Catalog may still list **7** `gates_remaining` until maintainer bump @ flip.  
> **Practice PASS ≠ auto-remove from catalog.**

| Gate | UI @ 27/06 | Practice @ 28/06+ | Blocks PB-12 @ 0.x? |
|------|------------|-------------------|---------------------|
| PB-9 | IN PROGRESS; gap "must clarify" | Ticks **26–28**; gap **documented**; MSI+VPS soak | **Yes** |
| PB-7 | **Pending** CLEAN | **PASS** 2026-06-27 MSI Ubuntu | **No** |
| PB-8 | After PB-9; human ~07-07 | **Done** @ `c58b4cc` 2026-06-28 early | **No** |
| security@ | Not tested; ~07-08 | **PASS** 2026-06-28 | **No** |
| PB-10 | Defer (direction OK) | **Deferred GA** #78 post-flip | **No** @ 0.x |
| PB-6 | Publish on flip | Static synced; refresh pre-flip | No (refresh) |
| PB-12 | Human ~07-10 | Pending | **Yes** |

### 3.5 Pre-flip checklist (UI Part 10.4) — wrong commands

| UI handoff (reject) | SSOT |
|---------------------|------|
| `curl …/openapi.json > docs/openapi.json` | `python scripts/export_openapi.py` → `docs/openapi/openapi.json` |
| `git tag v0.1.0-rc.1` at pre-flip | Tag **exists** @ `c58b4cc` — **do not re-tag** |
| security@ in pre-flip steps | **Done** — repeat only on regression |
| Create rc tag at flip | Release **`v0.1.0-beta.1`** from existing rc.1 |

### 3.6 Timeline (UI Part 10.3)

| UI | Correct |
|----|---------|
| 06-30..07-05 PB-7 CLEAN | **Done** 2026-06-27 |
| ~07-07 PB-8 + CHANGELOG | **Done** 2026-06-28 (#120, tag `c58b4cc`) |
| ~07-08 security@ | **Done** 2026-06-28 |
| Part 18 Q1: Day 14 = 07-10 (Scenario B) | **Reject** — Day 14 **~2026-07-06** (start 2026-06-22) |

### 3.7 PB-9 soak — UI gaps

| UI | Correct |
|----|---------|
| Gap 06-22→25 "operator must clarify" | **Resolved** — [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) § clock vs evidence |
| MSI-only soak | **Dual-host:** MSI `PB9_SOAK_ITERATION_LOG.md` + VPS `vps-soak-iteration.log` (CUR-04) |
| Ticks 06-26/27 | **+2026-06-28**; VPS hourly PASS — [`vps-hourly-loop-verify-2026-06-28.md`](practice-evidence/pb-9-day14-review/artifacts/vps-hourly-loop-verify-2026-06-28.md) |
| Profile table: CLEAN **pending** | CLEAN **PASS** |

---

## 4. UI Part 18 open questions — resolution

| # | UI question | Status @ 2026-06-28 |
|---|-------------|---------------------|
| 1 | PB-9 gap continuous? Scenario B 07-10? | **Closed** — deploy deferred; Day 14 ~07-06 |
| 2 | PB-10 block PB-12? | **Closed** — defer GA; does **not** block 0.x beta |
| 3 | PB-7 which machine? | **Closed** — Ubuntu MSI Path A Docker PASS |
| 4 | CHANGELOG draft before tag? | **Closed** — #120 merged; tag @ `c58b4cc` |
| 5 | security@ live? | **Closed** — PASS [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) |

---

## 5. UI Part 13 Claude role — phase update

| UI still says | Current role |
|---------------|--------------|
| Support PB-7 CLEAN Q&A | **Done** — do not re-open |
| PB-9 gap 3 scenarios | **Closed** — Day 14 prep only |
| Confirm PB-10 scope | **Decided** — record defer @ PB-12 |
| PB-8 human post PB-9 | **Done early** @ `c58b4cc` |

**Now → PB-12:** PB-9 daily tick support · Day 14 `RESULTS.md` · PB-12 narrative · doc drift LOW. **No** new `src/` features.

---

## 6. Commit history — UI stops at `527eb5d`

UI Part 17 missing (Cursor/operator after 2026-06-27):

| Ref | Summary |
|-----|---------|
| `fa71bd5` | PB-7 CLEAN evidence |
| `c58b4cc` | security@ PASS · tag `v0.1.0-rc.1` |
| `e76d203` | CUR-04 VPS soak `--repo-log` |
| #119 | go-no-go practice sync |
| #120 | CHANGELOG expand |
| `ac5f017` | VPS hourly verify + session anchor |
| `20e4fc3` | Full technical audit report |
| `5dc565b` | Claude Project setup guide |
| `47cb630` | Manual operator playbook |

---

## 7. Critical path comparison

**Implied by UI @ 27/06:**

```text
PB-9 → PB-7 → security@ → PB-8 tag → PB-12
```

**Actual @ 47cb630:**

```text
[DONE] PB-7 · security@ · PB-8 @ c58b4cc · CHANGELOG · go-no-go
[NOW]  PB-9 — ticks 29/06+ → Day 14 ~07-06
[WAIT] Pre-flip export_openapi (~07-07) — no re-tag
[WAIT] PB-12 human GO (~07-10)
[POST] PB-10 #78 · catalog bump @ flip
```

**True blockers @ 0.x:** **PB-9 calendar** + **PB-12 human** only.

---

## 8. What remains valid in UI handoff (reference only)

Keep for architecture Q&A — verify against repo if unsure:

- Parts 2–3: concept, 8 invariants, package identity
- Part 4: module tree, 13 endpoints, HTTP contracts, Option A tool naming
- Parts 6–7: Karpathy layers (fix test count if cited), ABAC, telemetry hash-chain
- Part 8: CI topology, `examples/minimal/`, `examples-minimal-smoke`
- Part 9: Studies 01–08 (G-05 OPEN = PB-9 still correct)
- Part 11: path/job drift rows (add: reject `527eb5d`, `165 tests`)
- Parts 14–15: key decisions, env vars

---

## 9. SSOT file priority (Claude Project knowledge)

**Upload from repo — not UI export:**

| Priority | File |
|----------|------|
| 1 | [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md) |
| 2 | [`MANUAL_OPERATOR_PLAYBOOK.md`](MANUAL_OPERATOR_PLAYBOOK.md) |
| 3 | [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) |
| 4 | [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) |
| 5 | [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md) |
| 6 | [`CLAUDE_PROJECT_SETUP.md`](../prompts/CLAUDE_PROJECT_SETUP.md) |
| 7 | This file |

**Do not upload** `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` as primary SSOT.

---

## 10. Paste block for Claude Project (reconciliation stamp)

```xml
<handoff_reconciliation date="2026-06-28">
  <reject_source>ACP_HANDOFF_FOR_NEW_CONVERSATION.md @ 527eb5d — ops/timeline STALE</reject_source>
  <canonical_ssot>PROJECT_STATUS_FULL_TECHNICAL_REPORT · MANUAL_OPERATOR_PLAYBOOK · HANDOFF_UI_DRIFT_RECONCILIATION (this file)</canonical_ssot>
  <cursor_vs_ui>Cursor executed PB-7/security@/PB-8/#119/#120/CUR-04 through 47cb630; UI handoff still lists those gates OPEN.</cursor_vs_ui>
  <mandatory_corrections>47cb630; 177 tests; C+ CLOSED; Day 14 ~07-06; export_openapi.py; no re-tag rc.1; practice≠catalog until bump</mandatory_corrections>
</handoff_reconciliation>
```

---

**Related:** [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md) (HTML drift) · [`PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`](PROJECT_STATUS_AUDIT_FOR_CLAUDE.md)

**Last updated:** 2026-06-28 @ `47cb630`
