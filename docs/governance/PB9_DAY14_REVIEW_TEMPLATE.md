# PB-9 Day 14 soak review template

**Document ID:** ACP-GOV-PB9-DAY14-001  
**Target review date:** ~**2026-07-06** (calendar from soak start 2026-06-22)  
**Evidence window:** logged iterations from **2026-06-26**  
**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)

Copy this file to `docs/governance/practice-evidence/pb-9-day14-review/RESULTS.md` when complete.

---

## Soak summary

| Field | Value |
|-------|-------|
| Calendar start | 2026-06-22 |
| First evidence | 2026-06-26 |
| Review date | YYYY-MM-DD |
| Calendar days claimed | ___ |
| Iterations in `PB9_SOAK_ITERATION_LOG.md` (MSI) | ___ PASS / ___ ERROR |
| Iterations in VPS `vps-soak-iteration.log` | ___ PASS / ___ ERROR (excerpt only) |

## Evidence inventory

- [ ] [`PB9_STAGING_SOAK_LOG.md`](../PB9_STAGING_SOAK_LOG.md) — daily rows complete since 2026-06-26
- [ ] [`PB9_SOAK_ITERATION_LOG.md`](../PB9_SOAK_ITERATION_LOG.md) — MSI hourly iterations persisted
- [ ] VPS [`practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log`](../practice-evidence/pb-9-day14-review/artifacts/README.md) — host-local; paste excerpt into `RESULTS.md`
- [ ] Gap 06-22→25 explained in soak log § clock vs evidence
- [ ] Hosts: MSI Docker · ubuntu-vps · (other: ___)

## Anomalies (SEV criteria)

| SEV | Definition |
|-----|------------|
| **SEV-1** | Blocks PB-12: crash + data loss, policy bypass, fail-open |
| **SEV-2** | Requires analysis: repeated 5xx, memory leak >20%, unexpected restart |
| **SEV-3** | Document only: planned restart, config reload |

| Date | Anomaly | SEV | Resolution |
|------|---------|-----|------------|
| | none / list | | |

## Smoke gate (review day)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
curl -sf "$ACP_API_URL/governance/status" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(len(d['public_beta']['gates_remaining']))"
```

Expected: smoke **8/8** · governance **1.3.3** · **7** `gates_remaining`.

## Verdict

- [ ] **PASS** — proceed PB-8 rc tag + PB-12 prep
- [ ] **CONDITIONAL** — waiver: ___
- [ ] **FAIL** — extend soak ___ days

**Operator:** ___  
**Date:** ___  
**Next:** PB-8 · security@ · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) phase 3
