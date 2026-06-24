# Snapshot notice — `audit_reconcile_final.html`

**Imported:** 2026-06-22 from Claude + Cursor combined reconcile packet  
**Baseline code:** `master` @ `6dfffdf` (post PR #63 — Milestone C boundary)  
**Upstream audits:** Claude `acp_full_audit_report.html` @ `fc296d4` + Cursor post-#63 audit

This HTML is a **historical snapshot**. It correctly describes the **hygiene + governance lag** moment immediately after PR #63. Most pane ③④⑥ tasks are **executed** on current `master`.

## Live truth (use these instead)

| Question | Document |
|----------|----------|
| Reconcile artifact → current status | [`ACP_AUDIT_RECONCILE_FINAL_STATUS.md`](ACP_AUDIT_RECONCILE_FINAL_STATUS.md) @ `c5d52e5` |
| Full audit reconciliation | [`ACP_FULL_AUDIT_RECONCILIATION.md`](ACP_FULL_AUDIT_RECONCILIATION.md) |
| Cursor prompts 1–3 | [`ACP_AUDIT_PROMPTS_1_3_FINAL.md`](ACP_AUDIT_PROMPTS_1_3_FINAL.md) |
| Artifact puzzle map | [`ACP_ARTIFACT_PUZZLE_MAP.md`](ACP_ARTIFACT_PUZZLE_MAP.md) |
| Public Beta execution | [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md) |
| Staging soak (PB-9) | [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) |
| Public flip decision | [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) |

## Stale claims in HTML (do not use for planning)

| HTML claim @ `6dfffdf` | Current @ `c5d52e5` |
|------------------------|---------------------|
| 15 OPEN issues | **4 OPEN** — PB-9..12 (#77–#80) only |
| Governance 40% | **~95%** — hygiene #64, C+ #74, B+ #75, docs #76, PB prep #81–#82 |
| MC-8/MC-10/#9 debt open | **CLOSED** — C+ #74, #9/#39 PR #75 |
| Public Beta 0/8 legal | **Done** — LICENSE, SECURITY, CONTRIBUTING, CoC PR #81 |
| 156 tests | **165 pytest**, smoke **8/8** |
| Pane ⑥ hygiene PR pending | **Done** — PR #64 + follow-on PRs |

**Rule:** When this HTML conflicts with `ARCHITECTURE.md` or `master`, **master wins**.
