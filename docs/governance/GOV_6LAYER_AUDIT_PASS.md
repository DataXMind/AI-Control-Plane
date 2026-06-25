# 6-Layer Governance — Audit Pass Record

**Document ID:** ACP-GOV-6LAYER-PASS-001  
**Date:** 2026-06-22  
**Target:** `master` via PR consolidation (`low/gov-6layer-audit-complete`)

---

## Checklist (items 1–6)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | 6-layer `.cursorrules` on master | ✅ PR branch | `## L0` … `## L5` in `.cursorrules` |
| 2 | Post-merge verify | ✅ | This doc + puzzle map links |
| 3 | Pilot session (L0 pre-flight) | ✅ | Chat pilot 2026-06-22; branch `low/gov-ux-runtime` for L3 fix |
| 4 | Audit reconcile artifact | ✅ | `audit_reconcile_final.html` + `ACP_AUDIT_RECONCILE_FINAL_STATUS.md` |
| 5 | Phase R2 | ✅ | `docs/DATA_CLASSIFICATION.md`, ARCHITECTURE §Module ownership, DEVELOPMENT_PROTOCOL L2 |
| 6 | Phase R3 + harden | ✅ | `CONTRACT_TESTS.md`, `test_api_contract_snapshot.py`, PR template |
| 7 | Governance UX runtime | ✅ | `GET /governance/status`, `agentctl gov status`, `GOVERNANCE_UX_RUNTIME.md` |
| 8 | L5 ML5 memory pack | ✅ | `AGENTS.md`, `.cursor/rules/`, `SESSION_ANCHOR_TEMPLATE`, GP-01, CI `governance-memory` |

---

## L3 / L5 audit @ `low/gov-ux-runtime`

| Layer | Check | Result |
|-------|-------|--------|
| L3 | Branch `low/gov-ux-runtime` from master | ✅ |
| L3 | PR template risk + verify checklist | ✅ |
| L5 | Patterns 6–7 in LESSONS_LEARNED | ✅ |
| L5 | GOV_6LAYER item #7 + pilot #3 closed | ✅ |

## Layer live map @ merge

| Layer | Authority file |
|-------|----------------|
| L0 | `.cursorrules` §L0 |
| L1 | `ARCHITECTURE.md`, `docs/DATA_CLASSIFICATION.md` |
| L2 | `docs/governance/CURSOR_RISK_POLICY.md` |
| L3 | `.cursorrules` §L3, `CONTRIBUTING.md` |
| L4 | CI + `docs/CONTRACT_TESTS.md` + `GET /governance/status` |
| L5 | `LESSONS_LEARNED.md`, `AGENTS.md`, `.cursor/rules/`, GP-01 |

---

## Not mechanically enforced (honor system + review)

- LOC limits per risk tier
- File allowlists per task type
- L0 assumption block before code

Track violations in [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md).

**Supersedes:** Informal audit FAIL @ flat `.cursorrules` on `c5d52e5`.
