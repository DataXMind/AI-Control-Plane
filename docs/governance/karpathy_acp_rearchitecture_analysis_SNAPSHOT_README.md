# Snapshot notice — `karpathy_acp_rearchitecture_analysis.html`

**Imported:** 2026-06-22 from Claude architect packet (Karpathy 4 principles × 6-layer governance)  
**Baseline referenced in HTML:** `master` @ `6dfffdf` (post PR #63)  
**Code truth @ import:** `master` @ `c5d52e5` (Milestones A/B/C/C+ CLOSED; Public Beta IN PROGRESS)

This HTML is a **design proposal** — not executed code. It recommends governance restructure (`.cursorrules` 6-layer, `CURSOR_RISK_POLICY.md`, `LESSONS_LEARNED.md`).

## Live truth (use these instead)

| Question | Document |
|----------|----------|
| Rearchitecture plan + pipeline | [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) |
| Cursor risk policy (L2) | [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) |
| Failure patterns → rules loop (L5) | [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md) |
| Artifact puzzle map | [`ACP_ARTIFACT_PUZZLE_MAP.md`](ACP_ARTIFACT_PUZZLE_MAP.md) |
| Public Beta (parallel track) | [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md) |

## Stale claims in HTML @ import

| HTML claim | Current @ `c5d52e5` |
|------------|---------------------|
| 156 tests | **165** pytest, smoke **8/8** |
| L4 missing security scan | **Dependabot + pip-audit** in CI (PB prep) |
| MC/C+ debt open | **CLOSED** PR #74, #75 |
| `.cursorrules` has surgical rules | **Partial** — file is ~50 lines, flat; still has stale Milestone A apex stub guard |

**Rule:** Rearchitecture is **additive governance** — does not replace `ARCHITECTURE.md` invariants or milestone delivery.
