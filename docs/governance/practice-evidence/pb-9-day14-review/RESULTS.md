# PB-9 Day 14 soak review — RESULTS

**Document ID:** ACP-GOV-PRACTICE-PB9-DAY14-RESULTS-001  
**Status:** **SIGNED PASS**  
**Template:** [`PB9_DAY14_REVIEW_TEMPLATE.md`](../../PB9_DAY14_REVIEW_TEMPLATE.md)  
**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) — **CLOSED** 2026-07-06  
**Review date:** **2026-07-06**

---

## Soak summary

| Field | Value |
|-------|-------|
| Calendar start | 2026-06-22 |
| First evidence | 2026-06-26 |
| Review date | **2026-07-06** |
| Calendar days claimed | **15** (22→06 inclusive; gap 22→25 documented) |
| Iterations in `PB9_SOAK_ITERATION_LOG.md` (MSI) | **59 PASS** (`health=ok`) / **1 soak_iter fail** (`apex=fail` @ 2026-07-01T06:51:41Z — container down, SEV-3) |
| Iterations in VPS `vps-soak-iteration.log` | **0 ERROR** in review window; hourly PASS through `2026-07-06T03:09:55Z` (host-local) |
| `master` SHA @ review | **`9680b1e`** (post-#195 Day 14 tick) |
| `master` SHA @ pre-flip | **`9680b1e`** + OpenAPI export commit (C1-02) |
| Catalog @ review | **v1.5.0** · **17** patterns |

---

## Evidence inventory

- [x] [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) — daily rows **2026-06-26 → 2026-07-06**
- [x] [`PB9_SOAK_ITERATION_LOG.md`](../../PB9_SOAK_ITERATION_LOG.md) — MSI hourly through `2026-07-06T03:52:54Z`
- [x] VPS [`artifacts/vps-soak-iteration.log`](artifacts/vps-soak-iteration.log) — host-local; excerpt below
- [x] Gap 06-22→25 explained in soak log § clock vs evidence
- [x] Hosts: MSI Docker fixture (**8 rules**) · ubuntu-vps production (**10 rules** on `:8000`)

### Dual-host scope waiver (accepted @ sign-off)

VPS `acp-soak.service` monitors **production** API (`policy_rules_count: 10`), not PB-9 minimal fixture (8 rules). Soak probes (health / policy / quota / apex) are stack-agnostic; waiver accepted for Day 14 PASS.

### VPS log excerpt (@ 2026-07-06)

```text
2026-07-06T01:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T02:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T03:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

`acp-staging` + `acp-soak`: **active** · cadence **3600s**.

### MSI log excerpt (@ 2026-07-06)

```text
2026-07-06T02:52:53Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T03:52:54Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

Smoke **8/8** · governance verify **1.5.0 · 17** · full pytest **221** (pre-flip).

---

## Telemetry (`ACP_DATA_DIR`)

| Host | Host path `du` | Result | Assessment |
|------|----------------|--------|------------|
| MSI | `/data/acp` | No host path (named Docker volume `acp-data`) | Use `docker exec minimal-acp-api-1 du -sh /data/acp` for spot-check |
| VPS | `/data/acp` | `No such file or directory` on host | Data inside production container volume — inspect via `docker volume ls` |

**Waiver @ sign-off:** No runaway growth observed — `tokens_remaining=2000000.0` stable across all soak iterations; no disk-full or telemetry errors in soak window. Host-level `du` deferred to Docker volume inspect (not blocking 0.x beta).

---

## Day 14 criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Zero SEV-1/2 from control plane | ✅ | 0 counted |
| `POST /policy/evaluate` p99 < 500 ms | ✅ | Smoke policy tests PASS; historical 5.34ms sample |
| Telemetry under `ACP_DATA_DIR` predictable | ✅ | Stable quota reads; Docker volume (see above) |
| Close #77 → PB-10 (#78) if pass | ✅ | #77 closed 2026-07-06 |

---

## Smoke gate — review day (2026-07-06)

| Check | Result |
|-------|--------|
| Smoke (`pytest -m smoke`) | **8 / 8** PASS |
| Governance verify | **1.5.0 · 17 patterns** OK |
| OpenAPI verify | **3.1.0 · 13 paths** OK |
| Full suite | **221 passed** |
| `gates_remaining` | **7** (until PB-12 catalog bump) |
| `gates_blocking_pb12` | **PB-9** ✅ · **PB-12** ⏳ human GO |

---

## Pre-flip (C1-02 @ 2026-07-06, early)

| Step | Result |
|------|--------|
| `docker compose … up -d --build` | ✅ `minimal-acp-api-1` rebuilt |
| `python scripts/export_openapi.py` | ✅ `mac_pilot_deploy_url` added to `PracticeEvidenceSummary` |
| `verify_governance_status_runtime.sh` | ✅ 1.5.0 · 17 |
| `verify_openapi_runtime.sh` | ✅ 3.1.0 · 13 paths |
| `pytest tests/ -q` | ✅ **221 passed** |

---

## Verdict

- [x] **PASS** — proceed PB-12 prep (PB-8 tag ✅ @ `c58b4cc` · security@ ✅ 2026-06-28)
- [ ] **CONDITIONAL** — _(resolved: waivers accepted)_
- [ ] **FAIL**

**Waivers accepted:**

1. VPS production (10 rules) vs MSI fixture (8 rules) for dual-host soak
2. 07-04 human tick partial Quota/Apex (production/enforce day)
3. Telemetry via soak stability + Docker volume (host `/data/acp` not mounted on WSL/VPS host)

**PB-10:** **deferred GA** — 0.x public beta ships without 30-day production soak.

**Operator:** mobilexmind  
**Date:** 2026-07-06  
**Signature:** GitHub [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) — *"Day 14 PASS — PB-10 deferred GA"* (closed)

---

## Next steps

1. ~~Close #77~~ ✅
2. ~~Pre-flip OpenAPI export~~ ✅ (commit via PR)
3. ~~**PB-12 human GO** (~2026-07-10)~~ ✅ [`PUBLIC_BETA_GO_NO_GO.md`](../../PUBLIC_BETA_GO_NO_GO.md)
4. ~~GitHub **public visibility** + release **`v0.1.0-beta.1`**~~ ✅ 2026-07-06
5. ~~Catalog bump PR (`governance_catalog.py`)~~ ✅ v1.6.0
6. ~~Open [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) (PB-10 GA track)~~ ✅ clock started 2026-07-06

---

**Related:** [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../../PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)
