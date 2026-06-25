# Governance next phase — Pre-approval audit (harsh)

**Document ID:** ACP-GOV-PRE-APPROVAL-AUDIT-001  
**Audit date:** 2026-06-25  
**Auditor role:** Independent re-read of plan + evidence + master @ `c6e8cc1` (PR #90 merged)  
**Purpose:** Operator review **before** approving execution of G1–G4 / PB continuation  
**Plan under review:** [`GOVERNANCE_NEXT_PHASE_PLAN.md`](GOVERNANCE_NEXT_PHASE_PLAN.md)

---

## 1. Executive verdict

| Question | Answer |
|----------|--------|
| **G0 complete?** | **YES** — PR [#90](https://github.com/DataXMind/AI-Control-Plane/pull/90) merged 2026-06-25; `master` @ `c6e8cc1` |
| **Safe to start G1 now?** | **CONDITIONAL** — see §4; recommend **one meta-drift PR** (§6) before or bundled with G1-1 |
| **Safe to start G2?** | **OPTIONAL** — no PB-12 blocker; operator bandwidth only |
| **PB-9 on track?** | **NO** — daily soak log has **zero** checked days (§5) |
| **PB-12 ready?** | **NO** — PB-9 + PB-10 + G3 items open (§8) |
| **Over-claim risk for Claude?** | **HIGH** if CS-01/03/04 or PB-9 treated as PASS (§7) |

**Harsh summary:** G0 closed the **documentation drift packet**; it did **not** close operational soak, process drills, or several **doc↔doc** inconsistencies. Do not conflate “G0 merged” with “governance program complete.”

---

## 2. G0 closure verification (#90)

| G0 ID | Deliverable | Verified on `c6e8cc1` | Notes |
|-------|-------------|------------------------|-------|
| G0-1 | `GOVERNANCE_DRIFT_RECONCILIATION.md` | ✅ Exists | ⚠️ §1/§5/§6 still describe **pre-G0** gaps — meta-drift (§6) |
| G0-2 | `GOVERNANCE_NEXT_PHASE_PLAN.md` | ✅ Exists | ⚠️ Stray broken row at end (fixed in same audit packet) |
| G0-3 | `LESSONS_LEARNED.md` P-01..P-12 | ✅ | Rich registry; P-11/P-12 present |
| G0-4 | `CURSOR_RISK_POLICY.md` F8–F10 + template + waiver | ✅ | Implemented as forbidden ops **#7–#11** + §PR template + §Waiver (not labeled “F8” in prose — acceptable) |
| G0-5 | Root `CLAUDE.md` | ✅ | Karpathy 4 + governance paths |
| G0-6 | `.cursorrules` L1/L5 refresh | ✅ | Date 2026-06-25; practice-evidence pointers |
| G0-7 | `ACP_ARTIFACT_PUZZLE_MAP.md` | ✅ | Cross-links present |
| G0-8 | `ACP_KARPATHY_REARCHITECTURE_PLAN.md` | ✅ | ⚠️ §3.3 “Still to create” table **stale** — R1-B, R3-B marked open though delivered (§6) |

**CI:** PR #90 passed Smoke + Full suite + codecov before merge (same bar as #88/#89).

---

## 3. SSOT hierarchy (re-stated for approval)

When documents conflict, resolve in this order:

```text
code + ARCHITECTURE.md
  > practice-evidence/*/RESULTS.md + PRACTICE_STUDIES_AUDIT_01-07.md
  > GOVERNANCE_UX_RUNTIME.md (CS catalog)
  > GOVERNANCE_DRIFT_RECONCILIATION.md (historical + closure notes)
  > HTML artifacts (karpathy_acp_artifacts_fixed.html, lessons_learned_md.html) — HISTORICAL ONLY
```

**Audit rule:** Any doc claiming pytest **156** or “CLAUDE.md missing” without a **pre-#90** banner is **stale** and must not drive decisions.

---

## 4. Phase G1 — Karpathy close-out (harsh task review)

| ID | Plan claim | Actual state | Severity | Recommendation |
|----|------------|--------------|----------|----------------|
| **G1-1** | Verify `DEVELOPMENT_PROTOCOL.md` Evolve requires LESSONS update | **GAP** — §5.6 Evolve lists issue/ARCHITECTURE/CHANGELOG/pitfall→debt; **no** mandatory `LESSONS_LEARNED.md` row | **Medium** | **Blocker for “R4 sprint-close loop” sign-off** — add explicit Evolve bullet + link to P-05/P-07 before marking G1 done |
| **G1-2** | Prompt template v2 audit | **Largely DONE** — `docs/prompts/_TEMPLATE.md` has risk, allowlist, assumptions, verify | **Low** | Change task to **“adoption audit”**: CONTRIBUTING + sample prompts reference template |
| **G1-3** | Quarterly LESSONS review calendar | **Not started** (target 2026-09) | **Info** | Calendar only — no action until September |
| **G1-4** | `GOV_6LAYER_AUDIT_PASS.md` addendum post-studies | **Missing** — doc ends @ 2026-06-22, no Studies 01–07 L4 proof link | **Medium** | Add § “Post-studies addendum” linking practice-evidence + CS-05/06 |

**G1 scope creep risk:** Karpathy plan §3.3 still lists R1-A (6-layer rewrite) as pending though `.cursorrules` is already 6-layer — **do not re-open R1-A** unless a diff audit proves regression.

**CONTRIBUTING gap:** Links `CURSOR_RISK_POLICY` but **not** `CLAUDE.md` — minor G1 hygiene.

---

## 5. Phase PB — PB-9 soak (CRITICAL ops gap)

**Source:** [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md)

| Check | Expected | Actual @ audit | Verdict |
|-------|----------|----------------|---------|
| Clock start | 2026-06-22 approved | Stated in doc | ✅ |
| Day 0 deploy commands | Documented | Present | ✅ |
| Daily checklist 2026-06-22 … 2026-07-06 | Health, policy, quota, apex, SEV | **All ☐ unchecked** | ❌ **FAIL discipline** |
| Study 07 remote soak | One iteration | Documented in Study 07 | ✅ slice only |
| Replaces 14-day calendar? | No | Plan + audit pack agree | ✅ |

**Harsh finding:** Maintainer approved PB-9 start 2026-06-22, but the **official log shows no operator attestation** for any day. Study 07’s one-shot `soak_staging.sh` on VPS **does not** satisfy PB-9.

**Blocks PB-12:** **YES** (by definition).  
**Blocks G1 docs PRs:** **NO** (parallel track rule stands).

**Required operator action (not agent):** Check daily rows + paste health/soak evidence or point to `/tmp/acp-soak-staging.log` excerpts until Day 14 review ~2026-07-06.

---

## 6. Meta-drift inventory (docs claiming wrong state)

| Location | Stale claim | Truth @ `c6e8cc1` | Fix priority |
|----------|-------------|-------------------|--------------|
| `GOVERNANCE_DRIFT_RECONCILIATION.md` §1 table | CLAUDE missing; F8–F10 missing; HIGH drift | Closed in #90 | **P0** — add §“Post-G0 closure” or refresh §1 |
| `GOVERNANCE_DRIFT_RECONCILIATION.md` §6 | “R1-B still open” | `CLAUDE.md` exists | **P0** |
| `ACP_KARPATHY_REARCHITECTURE_PLAN.md` §3.3 | R1-B, R3-B “to create” | Delivered | **P1** |
| `PUBLIC_BETA_GO_NO_GO.md` | Baseline `de931b5` | Master `c6e8cc1` | **P1** — refresh baseline + PB-9 status |
| `PRACTICE_STUDIES_AUDIT_01-07.md` header | “baseline post #86” | Should note #87–#90 | **P2** |
| `GOVERNANCE_NEXT_PHASE_PLAN.md` §8 | “G0 drift reconciliation merged” | ✅ Now true | Update §3 status banner |

**Verdict:** Merging G0 **without** refreshing the reconciliation doc’s executive table creates a **self-contradicting governance pack** — Claude or a new operator can “prove” drift still HIGH using the reconciliation doc itself.

---

## 7. Practice evidence — what is NOT proven

From [`PRACTICE_STUDIES_AUDIT_01-07.md`](practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md) §7, §14.2:

| Case study | Claim allowed | Claim forbidden |
|------------|---------------|-----------------|
| **CS-01** PR LOC + risk | Listed in `gov status` | Hands-on drill PASS |
| **CS-02** doc-only allowlist | Path in gov response | Enforced in live PR |
| **CS-03** individual `Closes #N` | Catalog visibility | Process validated |
| **CS-04** ABAC key pre-flight | Catalog visibility | Operator drill PASS |
| **CS-05** soak / health | Local ×2 + remote ×1 | 14-day PB-9 PASS |
| **CS-06** fail-closed | Strong — cite Studies 01,05,06,07 | — |

**Documented soft gaps (non-blocking for Studies sign-off):**

| Gap | Study | Plan mapping |
|-----|-------|--------------|
| G-01 kill switch 5g SKIPPED | 05 | G2-1 |
| G-02 stale Docker image 5e partial | 05 | G2-2 |
| G-03 Study 07 negative LAN log missing | 07 | G2-4 |
| G-04 CS-01/03/04 no hands-on drill | 01–07 | G1 process / optional future study |

---

## 8. PB-12 precondition matrix (harsh)

**Checklist source:** [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)

| Precondition | Required for PB-12 | Status | Blocker? |
|--------------|-------------------|--------|----------|
| PB-9 staging soak ≥14d | Yes | **IN PROGRESS — log empty** | **YES** |
| PB-10 production soak ≥30d | Yes | Not started | **YES** |
| PB-7 README ≤15 min fork | Yes | Not operator-verified | **YES** |
| PB-8 `v0.1.0-rc.1` tag | Yes | Plan only | **YES** |
| G0 drift merged | Plan §8 | ✅ #90 | No |
| Practice audit on master | Plan §8 | ✅ #89 | No |
| CONTRACT_TESTS + CI | G3-3 | `docs/CONTRACT_TESTS.md` + `tests/test_api_contract_snapshot.py` exist | Verify green on `master` — **likely OK** |
| PB-11 branch protection API | Documented | 403 private repo — process-only waiver | Accepted until flip |
| No open HIGH governance drift | Plan §8 | **Meta-drift in §6** — arguable **YES** until reconciliation refresh | **SOFT YES** |
| Human explicit approve | Always | Pending | **YES** |

**Earliest realistic PB-12 window:** After **2026-07-06** PB-9 review **if** daily logs are backfilled and pass — then PB-10 clock (+30d) unless waiver changes scope.

---

## 9. Phase G2 — Optional gaps (approve explicitly or defer)

| ID | Effort | Touches `src/`? | Value | Harsh opinion |
|----|--------|-----------------|-------|---------------|
| G2-1 5g kill switch | ~1h | Possible MEDIUM if wiring | Closes G-01 | **Worth it** before public flip |
| G2-2 5e stale image | Low | No | Docker hygiene | Nice-to-have |
| G2-3 07b Mac witness | Low | No | Redundant with Study 06 LAN | **Skip unless audit audience demands** |
| G2-4 07 negative LAN log | Low | No | Closes G-03 over-claim risk | **Cheap insurance** |
| G2-5 Study 08 shipped remote | Medium | No | Profile B rules=10 on VPS | Optional confidence |

**Recommendation:** If approving G2 at all, prioritize **G2-1 + G2-4** only.

---

## 10. Phase G3 — Pre-flip technical

| ID | Status | Harsh note |
|----|--------|------------|
| G3-1 PB-7 README | **Not done** | Real fork test on clean machine — no substitute |
| G3-2 PB-8 rc tag | **Not done** | Requires CHANGELOG + human |
| G3-3 CONTRACT_TESTS | Doc + test file exist | Run `pytest tests/test_api_contract_snapshot.py -v` on release candidate |
| G3-4 PB-11 | Deferred | Documented waiver — OK |

---

## 11. Recommended approval gates (operator)

Use explicit approve per track:

| Gate | Approve phrase (example) | Unlocks |
|------|--------------------------|---------|
| **A** | “Approve G1 execution” | DEVELOPMENT_PROTOCOL Evolve patch, CONTRIBUTING+CLAUDE link, G1-4 addendum |
| **B** | “Approve G2-{ids}” | Named practice studies only |
| **C** | “Approve meta-drift PR” | Reconciliation §1 refresh, Karpathy §3.3, PB GO/NO-GO baseline |
| **D** | “PB-9 backfill + continue” | Operator daily logging — **not** agent-automated |
| **E** | “PB-12 go” | **CRITICAL** — only after §8 all hard blockers cleared |

**Do not execute G1–G4 code/docs PRs until at least Gate **A** or **C** is explicitly given.**

---

## 12. Suggested first PR after approval (LOW risk)

If operator approves **C** (recommended before or with **A**):

```text
Branch: low/gov-post-g0-meta-drift-refresh
Risk: LOW (docs-only)
Contents:
  - GOVERNANCE_DRIFT_RECONCILIATION.md §1 post-G0 table + banner
  - ACP_KARPATHY_REARCHITECTURE_PLAN.md §3.3 status refresh
  - PUBLIC_BETA_GO_NO_GO.md baseline bump
  - GOVERNANCE_NEXT_PHASE_PLAN.md §3 G0 COMPLETE banner
  - (optional) PRACTICE_STUDIES_AUDIT header baseline #90
```

---

## 13. Sign-off (operator)

| Role | Name | Date | Decision |
|------|------|------|----------|
| Maintainer | | | ☐ Approve Gate A / B / C / D / E (circle) |
| Notes | | | |

---

**Last updated:** 2026-06-25 @ post PR #90 merge
