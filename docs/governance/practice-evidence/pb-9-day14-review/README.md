# PB-9 Day 14 review — practice evidence

**Document ID:** ACP-GOV-PRACTICE-PB9-DAY14-001  
**Status:** **IN PROGRESS** — review target ~**2026-07-06**  
**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Template:** [`PB9_DAY14_REVIEW_TEMPLATE.md`](../../PB9_DAY14_REVIEW_TEMPLATE.md)

---

## Evidence layers (ML5)

| Layer | MSI (WSL) | VPS (`ubuntu-vps`) |
|-------|-----------|---------------------|
| Daily human | [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) | Operator tick (same SSOT file in repo) |
| Machine hourly | [`PB9_SOAK_ITERATION_LOG.md`](../../PB9_SOAK_ITERATION_LOG.md) via `restart_soak_loop.sh` | [`artifacts/vps-soak-iteration.log`](artifacts/vps-soak-iteration.log) via `acp-soak.service` |
| Local debug | `/tmp/acp-soak-staging.log` | `/var/log/acp-soak-staging.log` |

**VPS repo-log path is host-local** (gitignored). Do not merge into `PB9_SOAK_ITERATION_LOG.md` — paste excerpts into `RESULTS.md` on review day.

---

## Deliverables

| File | When |
|------|------|
| `RESULTS.md` | After Day 14 review (~2026-07-06) — copy from template |
| `artifacts/vps-soak-iteration.log` | Runtime on VPS only (not committed) |
| `artifacts/*-excerpt-*.md` | Optional operator paste for Day 14 |

**Verdict:** Not recorded until operator sign-off on review date.
