# PB-12 — Public Beta go/no-go — RESULTS

**Document ID:** ACP-GOV-PRACTICE-PB12-FLIP-001  
**Status:** **GO — SIGNED**  
**Date:** **2026-07-06**  
**Related:** [`PUBLIC_BETA_GO_NO_GO.md`](../../PUBLIC_BETA_GO_NO_GO.md) · [`pb-9-day14-review/RESULTS.md`](../pb-9-day14-review/RESULTS.md)

---

## Verdict

| Question | Answer |
|----------|--------|
| **GO** — flip repository public? | **YES** |
| **GO** — ship `v0.1.0-beta.1`? | **YES** |
| PB-10 production soak 30d | **DEFERRED GA** — explicit accept for 0.x |

---

## Preconditions (all met)

| Gate | Evidence |
|------|----------|
| PB-9 Day 14 PASS | [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) closed · [`pb-9-day14-review/RESULTS.md`](../pb-9-day14-review/RESULTS.md) |
| Pre-flip C1-02 | OpenAPI export · smoke 8/8 · gov 1.6.0·17 · 221 pytest @ 2026-07-06 |
| PB-7 clean fork | PASS 2026-06-27 |
| PB-8 rc tag | `c58b4cc` — do not re-tag |
| security@ live | PASS 2026-06-28 |
| Legal PB-1..4 | LICENSE, SECURITY, CONTRIBUTING, CoC |

---

## PB-12 acceptance text (recorded)

*AI Control Plane **0.1.0-beta** ships without 30-day production soak (PB-10 deferred). Operator-facing disclaimer: **0.x API may change; not recommended for production workloads without independent validation.***

---

## Flip actions (@ 2026-07-06)

| # | Action | Status |
|---|--------|--------|
| 1 | Catalog bump `governance_catalog.py` v1.6.0 | ✅ this PR |
| 2 | GitHub visibility → **Public** | ✅ @ flip |
| 3 | Release **`v0.1.0-beta.1`** | ✅ @ flip |
| 4 | PB-10 clock [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) | ✅ comment @ flip |

---

**Decision:** **GO**  
**Operator / maintainer:** mobilexmind  
**Date:** 2026-07-06  
**Signature:** PB-12 GO memo — PB-10 deferred GA; 0.x public beta approved
