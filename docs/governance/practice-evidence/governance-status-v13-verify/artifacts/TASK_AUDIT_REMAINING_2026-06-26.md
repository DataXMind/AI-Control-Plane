# Governance task audit — remaining work @ 2026-06-26

**Document ID:** ACP-GOV-TASK-AUDIT-REMAINING-001  
**Baseline:** `master` @ `68ae48e` · VPS runtime **PASS** `1.3.2` · `13 patterns`  
**Purpose:** Rà soát chặt các task đã đóng vs còn mở sau wave post-Claude + P-13.

---

## Closed since wave start (do not re-open)

| Track | ID | Evidence | Status |
|-------|-----|----------|--------|
| G0 | Drift reconcile | PR #90 | ✅ CLOSED |
| G1 | Karpathy R-track | PR #91–#96 | ✅ CLOSED |
| G2 | Kill switch 5g | G2-1 `terminal-5g-g2-killswitch.md` | ✅ CLOSED → G-01 |
| G2 | Stale Docker 5e | G2-2 `terminal-5e-r-g2-docker.md` | ✅ CLOSED → G-02 |
| G2 | Study 07 negative LAN | G2-4 | ✅ CLOSED → G-03 |
| G2 | Study 08 shipped remote | G2-5 | ✅ CLOSED → G-06, G-07 |
| Gov UX | Catalog v1.3.x | PR #104–#106, #109 | ✅ v1.3.2 |
| Gov UX | VPS runtime verify | `vps-runtime-v132-pass.md` | ✅ PASS |
| Lessons | P-13 kill switch contract | `LESSONS_LEARNED.md` + `CURSOR_RISK_POLICY.md` §10 | ✅ ENCODED |
| Docs | Operator RUNBOOK SSOT | PR #108 `docs/RUNBOOK.md` | ✅ MERGED |
| PB-7 scaffold | Runbook + checklist | PR #107 `pb-7-clean-machine-fork/` | ✅ on master (not PASS) |

**`known_gaps` runtime:** 7 total · **1 OPEN** (`G-05` PB-9 calendar only).

---

## OPEN — blocks or gates PB-12

| Priority | ID | What | Owner | Target | Verify |
|----------|-----|------|-------|--------|--------|
| **P0** | G-05 / PB-9 | 14-day calendar soak | Operator daily | ~2026-07-06 | [`PB9_STAGING_SOAK_LOG.md`](../../../PB9_STAGING_SOAK_LOG.md) — only **2026-06-26** ticked |
| **P1** | G3-1 / PB-7 | Clean-machine fork ≤15 min | Operator other laptop | Before PB-12 | [`pb-7-clean-machine-fork/RESULTS.md`](../../pb-7-clean-machine-fork/RESULTS.md) **PAUSED** |
| **P1** | G3-2 / PB-8 | `v0.1.0-rc.1` tag | Human approve | Post PB-9 | `CHANGELOG.md` |
| **P2** | G3-3 | CONTRACT_TESTS parity | Dev | Pre-rc | `docs/CONTRACT_TESTS.md` + CI |
| **P2** | G1-3 | Quarterly LESSONS review | Calendar | 2026-09 | `LESSONS_LEARNED.md` |
| **CRITICAL** | G4 / PB-12 | Public flip | Human go/no-go | After above | [`PUBLIC_BETA_GO_NO_GO.md`](../../../PUBLIC_BETA_GO_NO_GO.md) |

---

## Ops hygiene (non-blocking)

| Item | Note | Action |
|------|------|--------|
| PB-9 duplicate soak PIDs | MSI WSL — prior session warning | Ensure **one** `soak_staging.sh --loop` per host |
| PB-9 VPS vs local | Study 07 one-shot ≠ calendar | Tick **each UTC day** on both stacks if running dual soak |
| HTML artifacts | `practice_studies_architecture_review.html` | Reconcile at PB-12 (P-11) — do not cite stale pytest counts |
| Pre-approval audit | `GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md` | §5 PB-9 log was empty — **partially stale**; use this audit + soak log |

---

## Next steps (ordered)

1. **PB-9 daily** — operator tick `PB9_STAGING_SOAK_LOG.md` when soak PASS for that UTC date (agent only on explicit *"đã tick ngày YYYY-MM-DD"*).
2. **~2026-07-06** — Day 14 review → close #77 if criteria met → open PB-10 (#78).
3. **PB-7** — run on **CLEAN** machine (not MSI WARM); fill `pb-7-clean-machine-fork/RESULTS.md`.
4. **PB-8** — human approve rc tag after PB-9 PASS.
5. **PB-12** — `PUBLIC_BETA_GO_NO_GO.md` checklist; no agent flip.

---

**Do not claim:** CS-01/03/04 hands-on runtime; PB-9 PASS until Day 14; PB-7 PASS until clean-machine evidence.
