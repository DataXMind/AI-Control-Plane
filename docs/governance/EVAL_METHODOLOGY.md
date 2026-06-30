# Evaluation Methodology — pass@k and pass^k

**Document ID:** ACP-GOV-EVAL-001  
**Layer:** L4 — Evaluation  
**Related:** [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) §5.5 · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)

---

## Definitions

| Metric | Meaning | Use when |
|--------|---------|----------|
| **pass@k** | At least **1 of k** attempts succeeds | Exploratory fix, prototype, “any path works once” |
| **pass^k** | **All k** attempts must succeed | Production gates, soak, merge criteria |

**Rule:** Public beta and merge gates use **pass^k** unless explicitly labeled exploratory.

---

## ACP gate mapping

| Gate | Metric | k | Command / artifact |
|------|--------|---|-------------------|
| Smoke (pre-merge) | pass^8 | 8 | `pytest tests/test_smoke.py -v -m smoke` |
| Full CI suite | pass^1 per job | 1 | GitHub Actions Full suite |
| Shipped config parity | pass^1 | 1 | `pytest -m shipped_config` |
| PB-7 clean fork | pass^1 | 1 | health + allow + deny ≤15 min |
| PB-9 calendar soak | pass^14 | 14 | daily human tick + machine log |
| PB-10 production soak | pass^30 | 30 | calendar days (post-flip) |
| Policy evaluate SLO | pass^k load | fleet RPS | `LOAD_CHARACTERISTICS.md` (P-15) |

---

## Examples

**Smoke gate (pass^8):** One failing SMK → **do not merge** (not pass@8).

**Soak day tick (pass^1 per day):** Each calendar day needs operator PASS row — missing day breaks pass^14 chain.

**Harness try-once (pass@1):** Acceptable for local Docker first pull; **not** sufficient for PB-12.

---

## ECC cross-reference

Industry harness practice (pass@k for exploration vs pass^k for reliability) is adopted here as **named vocabulary** only — no external tooling import. See [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md).

---

**Last updated:** 2026-06-30 · Catalog v1.5.0
