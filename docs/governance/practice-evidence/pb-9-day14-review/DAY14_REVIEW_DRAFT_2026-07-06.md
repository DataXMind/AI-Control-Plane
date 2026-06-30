# PB-9 Day 14 soak review — DRAFT (operator sign-off pending)

**Document ID:** ACP-GOV-PRACTICE-PB9-DAY14-DRAFT-001  
**Status:** **DRAFT** — complete on review date ~**2026-07-06**, then copy to `RESULTS.md`  
**Template:** [`PB9_DAY14_REVIEW_TEMPLATE.md`](../../PB9_DAY14_REVIEW_TEMPLATE.md)  
**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Prepared:** 2026-06-30 (pre-fill from evidence through 06-30 tick)

> **Operator:** Fill `___` blanks on review day. Check boxes only after live verify on **2026-07-06** (or chosen review date).

---

## Soak summary

| Field | Value |
|-------|-------|
| Calendar start | 2026-06-22 |
| First evidence | 2026-06-26 |
| Review date | **2026-07-06** _(target)_ |
| Calendar days claimed | **15** (22→06 inclusive; gap 22→25 documented) |
| Iterations in `PB9_SOAK_ITERATION_LOG.md` (MSI) | **21 PASS** / **0 ERROR** _(through 2026-06-29T11:26:07Z; re-count on review day)_ |
| Iterations in VPS `vps-soak-iteration.log` | ___ PASS / ___ ERROR _(paste excerpt on review day)_ |
| `master` SHA @ review | ___ _(target: post–07-05 ticks)_ |
| Catalog @ review | **v1.5.0** · **17** patterns _(expected until PB-12 bump)_ |

---

## Evidence inventory

- [x] [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) — daily rows **2026-06-26 → 2026-06-30** _(07-01..05: operator tick before review)_
- [x] [`PB9_SOAK_ITERATION_LOG.md`](../../PB9_SOAK_ITERATION_LOG.md) — MSI hourly iterations persisted (21 lines through 06-29)
- [ ] VPS [`artifacts/vps-soak-iteration.log`](artifacts/vps-soak-iteration.log) — host-local; paste excerpt below on review day
- [x] Gap 06-22→25 explained in soak log § clock vs evidence
- [x] Hosts: MSI Docker (`minimal-acp-api-1`) · ubuntu-vps _(hourly PASS 2026-06-28 — [vps-hourly-loop-verify](artifacts/vps-hourly-loop-verify-2026-06-28.md))_

### VPS log excerpt (paste on 2026-07-06)

```text
# tail -5 $ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log
___
```

---

## Daily checklist status @ 2026-06-30 (pre-review)

| Date | Health | Policy | Quota | Apex | SEV-1/2 | Notes (summary) |
|------|--------|--------|-------|------|---------|-----------------|
| 06-26 | ☑ | ☑ | ☑ | ☑ | 0 | First local evidence; hourly loop |
| 06-27 | ☑ | ☑ | ☑ | ☑ | 0 | PACE 8/8 post #118 |
| 06-28 | ☑ | ☑ | ☑ | ☑ | 0 | MSI + VPS hourly PASS |
| 06-29 | ☑ | ☑ | ☑ | ☑ | 0 | 13h gap → restart 01:20Z; SEV-3 reconciled 06-30 |
| 06-30 | ☑ | ☑ | ☑ | ☐ | 0 | Live verify; manual restart PR #163–168; Apex last good 06-29 |
| 07-01..05 | ☐ | ☐ | ☐ | ☐ | 0 | **Operator: tick before review** |
| 07-06 | — | — | — | — | — | Day 14 review row |

---

## Anomalies (SEV criteria)

| SEV | Definition |
|-----|------------|
| **SEV-1** | Blocks PB-12: crash + data loss, policy bypass, fail-open |
| **SEV-2** | Requires analysis: repeated 5xx, memory leak >20%, unexpected restart |
| **SEV-3** | Document only: planned restart, config reload |

| Date | Anomaly | SEV | Resolution |
|------|---------|-----|------------|
| 2026-06-29 | MSI ~13h Docker stop; restart 01:20Z | **SEV-3** | Planned/manual restart; VPS continuous |
| 2026-06-29 → 2026-06-30 | Iteration log silence until `StartedAt=2026-06-30T10:32:30Z` | **SEV-3** | Manual rebuild during PR #163–168 verify; `RestartCount=0`; no fail-open |
| — | **SEV-1 / SEV-2** | **0** | None attributed to control plane |

**SEV-1/2 total for soak window:** **0** _(confirm on review day)_.

---

## Day 14 criteria ([`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md))

| Criterion | Draft status | Review-day action |
|-----------|--------------|-------------------|
| Zero SEV-1/2 from control plane | ✅ draft (0 counted) | Re-confirm from logs |
| `POST /policy/evaluate` p99 < 500 ms | 🔄 | Sample from soak log / live curl on 07-06 _(06-30 sample: 5.34ms single)_ |
| Telemetry under `ACP_DATA_DIR` predictable | 🔄 | `du -sh` volume on review day |
| Close #77 → open PB-10 (#78) if pass | ⏳ | After sign-off |

---

## Smoke gate (review day — run on 2026-07-06)

```bash
cd /path/to/AI-Control-Plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke                    # expect 8/8

docker compose -f examples/minimal/docker-compose.yml up -d --build
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh          # expect 1.5.0 · 17 patterns
bash scripts/verify_openapi_runtime.sh
curl -sf "$ACP_API_URL/governance/status" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); pb=d['public_beta']; print(pb['gates_remaining'], pb.get('gates_blocking_pb12'))"
```

**Expected @ 0.x pre-flip:** smoke **8/8** · governance **1.5.0** · **17** patterns · **7** `gates_remaining` · blocking **PB-9, PB-12**.

| Check | Result (fill 07-06) |
|-------|---------------------|
| Smoke | ___ / 8 |
| Governance verify | ___ |
| OpenAPI verify | ___ |
| `gates_remaining` count | ___ |

---

## p99 sample (optional attachment)

```text
# Review day: grep policy latency from iteration log or run:
# curl -w '%{time_total}\n' -sf -X POST $ACP_API_URL/policy/evaluate ...
p99 estimate: ___ ms (threshold < 500 ms)
```

---

## Verdict (DRAFT — do not merge as PASS until signed)

- [ ] **PASS** — proceed PB-12 prep (PB-8 tag ✅ @ `c58b4cc` · security@ ✅ 2026-06-28)
- [ ] **CONDITIONAL** — waiver: ___ _(e.g. Apex not re-tested 06-30 — acceptable if 07-01..05 ticks ☑ Apex or waiver documented)_
- [ ] **FAIL** — extend soak ___ days

**Draft recommendation (2026-06-30):** **CONDITIONAL → PASS** if:

1. Daily ticks **07-01 through 07-05** complete (or waiver for Apex only with last-known-good ≤48h),
2. Review-day smoke + verify green,
3. VPS excerpt shows no SEV-1/2 since 06-28,
4. No new fail-open or policy bypass evidence.

**Operator:** ___  
**Date:** ___  
**Signature / GitHub comment:** ___

---

## Next steps after PASS

1. Copy this file → `RESULTS.md` (remove DRAFT header)
2. Close [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)
3. Pre-flip (~07-07): `python scripts/export_openapi.py` (OP-09)
4. PB-12 human GO (~07-10): [`PUBLIC_BETA_GO_NO_GO.md`](../../PUBLIC_BETA_GO_NO_GO.md)
5. Record PB-10 defer in PB-12 decision text
6. Open [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) (PB-10 GA track)

---

**Related:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../../PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · [`DAY14_REVIEW_DRAFT`](DAY14_REVIEW_DRAFT_2026-07-06.md) _(this file)_
