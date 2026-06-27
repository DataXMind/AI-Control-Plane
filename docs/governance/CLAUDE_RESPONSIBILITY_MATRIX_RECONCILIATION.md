# Claude responsibility matrix — Public Beta reconciliation

**Document ID:** ACP-GOV-CLAUDE-MATRIX-RECON-001  
**Audit date:** 2026-06-27  
**Baseline:** `master` @ `375ef14` (catalog v1.3.3 · post #118)  
**Source prompt:** Claude “Responsibility matrix → Public Beta” @ 2026-06-26  
**SSOT runtime:** `curl /governance/status` → `public_beta.gates_remaining` / `gates_closed`

---

## Verdict

| Question | Answer |
|----------|--------|
| Matrix still valid as execution plan? | **No** — TODAY + THIS WEEK rows mostly **DONE** |
| Core calendar constraint still valid? | **Yes** — PB-9 14-day soak until ~**2026-07-06** |
| Action now | **Operator gates only** — see [`TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) |
| C+ parallel track | **Non-blocking** — do not mix into PB-12 critical path |

---

## TODAY (2026-06-26) — reconciliation

| Matrix row | Owner | Status @ 2026-06-27 | Evidence |
|------------|-------|---------------------|----------|
| P0: `governance_catalog.py` sync | Cursor | ✅ **DONE** | v1.3.3 · #115; runtime #116–#117 |
| P1a: `RUNBOOK.md` Windows section | Cursor | ✅ **DONE** | #108; WSL/LAN § |
| Deploy 6-layer Karpathy docs | Cursor | ✅ **DONE** | `.cursorrules`, `CLAUDE.md`, `CURSOR_RISK_POLICY.md`, `LESSONS_LEARNED.md`, `AGENTS.md`, `.cursor/rules/` |
| Study 05g-r kill switch drill | Operator | ✅ **DONE** | G-01 CLOSED · [`study-05/artifacts/terminal-5g-g2-killswitch.md`](practice-evidence/study-05-advanced-surprises/artifacts/terminal-5g-g2-killswitch.md) · P-13 |

**Do not re-open** any TODAY row.

---

## THIS WEEK (2026-06-27 → 07-05) — reconciliation

| Matrix row | Owner | Status | Evidence |
|------------|-------|--------|----------|
| `SECURITY.md` (ACP AI scope) | Cursor | ✅ **DONE** | #112 · [`PB11_LEGAL_AUDIT.md`](PB11_LEGAL_AUDIT.md) |
| `CONTRIBUTING.md` | Cursor | ✅ **DONE** | #112 |
| `CODE_OF_CONDUCT.md` (CC 2.1) | Cursor | ✅ **DONE** | #112 |
| Study 08 Profile B remote VPS | Operator | ✅ **DONE** | G-06/G-07 CLOSED · [`study-08-shipped-remote/RESULTS.md`](practice-evidence/study-08-shipped-remote/RESULTS.md) |
| Monitor PB-9 soak log | Operator | 🔄 **IN PROGRESS** | G-05 OPEN · ticks 2026-06-26, 2026-06-27 |
| `examples/` docker-compose stub | Cursor | ✅ **DONE** | `examples/minimal/docker-compose.yml` · PB-5 |

---

## ~2026-07-06 PB-9 / PB-10 review — still valid

| Matrix row | Owner | When | Notes |
|------------|-------|------|-------|
| Audit PB-9 soak log | Claude / Cursor | ~2026-07-06 | Day 14 review — not before calendar |
| Verify all gates checklist | Claude / Cursor | ~2026-07-06 | Use `TASK_AUDIT` + `PUBLIC_BETA_GO_NO_GO.md` |
| `OPEN_SOURCE_READINESS` final review | Claude | ~2026-07-06 | |
| Approve/defer public flip | **You** | ~2026-07-06 | PB-12 human gate |
| Set announce date | **You** | Post go | |

---

## PUBLIC BETA FLIP (~2026-07-10 → 07-15) — reconciliation

| Matrix row | Owner | Status | Catalog / note |
|------------|-------|--------|----------------|
| Final doc sync check | Cursor | ⏳ At flip | Drift registry §10 |
| `v0.1.0-beta.1` tag | Cursor | ⏳ PB-8 | Catalog says **`v0.1.0-rc.1`** first — human approve |
| GitHub → Public | **You** | ⏳ PB-12 | #80 |
| Security Advisories + Dependabot | **You** | ⏳ PB-12 | Org settings |
| Announce | **You** | ⏳ PB-12 | |

**Naming drift:** Matrix `v0.1.0-beta.1` vs sprint `v0.1.0-rc.1` — follow [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md) PB-8 + human approve.

---

## PARALLEL (C+ — không block flip)

| Matrix row | Milestone | Block PB-12? | Status |
|------------|-----------|--------------|--------|
| MC-8 cyanheads E2E CI | C+ | No | Deferred / parallel |
| MC-10 otel-collector.yaml | C+ | No | Deferred |
| `apex/act.py` full PolicyEngine | C+ | No | Deferred |
| SAPAL external signal ingestion | C+ | No | Deferred |
| Redis ActionRegistry tests | C+ | No | Deferred |

`milestone_c_plus`: **CLOSED** in catalog — C+ hygiene done; these rows are **enhancement backlog**, not PB-12 blockers.

---

## Calendar constraint (still true)

```text
PB-9: 14-day soak = hard wait until ~2026-07-06
Soak cannot accelerate with more machines or code.
Everything else may run in parallel — but legal/docs/catalog fork-user are DONE.
```

---

## `gates_remaining` vs matrix (runtime @ v1.3.3)

| Gate | Matrix implied | Runtime |
|------|----------------|---------|
| PB-9 soak | THIS WEEK monitor | OPEN (G-05) |
| PB-7 fork | Implicit in flip prep | OPEN — CLEAN machine |
| Legal trio | THIS WEEK Cursor | **CLOSED** (`gates_closed`) |
| RUNBOOK | P1a TODAY | **CLOSED** |
| security@ live test | Pre-flip | OPEN |
| PB-10 / PB-8 / PB-6 | Post soak / flip | OPEN |

---

## Verify

```bash
bash scripts/verify_governance_status_runtime.sh
curl -s "$ACP_API_URL/governance/status" | jq '.public_beta'
```

**Drift:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) §10  
**Operator checklist:** [`TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md)
