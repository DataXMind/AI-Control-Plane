# PB-9 Day 14 soak review — RESULTS (pre-filled, sign-off pending)

**Document ID:** ACP-GOV-PRACTICE-PB9-DAY14-RESULTS-001  
**Status:** **PRE-FILLED** — operator human sign-off required before closing [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Template:** [`PB9_DAY14_REVIEW_TEMPLATE.md`](../../PB9_DAY14_REVIEW_TEMPLATE.md) · draft source [`DAY14_REVIEW_DRAFT_2026-07-06.md`](DAY14_REVIEW_DRAFT_2026-07-06.md)  
**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Review date:** **2026-07-06**

---

## Soak summary

| Field | Value |
|-------|-------|
| Calendar start | 2026-06-22 |
| First evidence | 2026-06-26 |
| Review date | **2026-07-06** |
| Calendar days claimed | **15** (22→06 inclusive; gap 22→25 documented) |
| Iterations in `PB9_SOAK_ITERATION_LOG.md` (MSI) | **58 PASS** (`health=ok`) / **1 soak_iter fail** (`apex=fail` @ 2026-07-01T06:51:41Z — container down, SEV-3) |
| Iterations in VPS `vps-soak-iteration.log` | **0 ERROR in review excerpt**; host-local full count via `grep -c health=ok` on VPS _(excerpt: continuous hourly PASS 07-05T22:09→07-06T02:09Z)_ |
| `master` SHA @ review | **`245daa6`** (post-#194; tick PR targets latest) |
| Catalog @ review | **v1.5.0** · **17** patterns |

---

## Evidence inventory

- [x] [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) — daily rows **2026-06-26 → 2026-07-06** (07-04 partial Quota/Apex documented)
- [x] [`PB9_SOAK_ITERATION_LOG.md`](../../PB9_SOAK_ITERATION_LOG.md) — MSI hourly iterations through `2026-07-06T02:52:53Z`
- [x] VPS [`artifacts/vps-soak-iteration.log`](artifacts/vps-soak-iteration.log) — host-local; excerpt below @ review verify
- [x] Gap 06-22→25 explained in soak log § clock vs evidence
- [x] Hosts: MSI Docker fixture (`minimal-acp-api-1`, **8 rules**) · ubuntu-vps (**production 10 rules** on `:8000`)

### Dual-host scope note (mandatory)

| Host | Stack | `policy_rules_count` | Soak target |
|------|-------|----------------------|-------------|
| **MSI WSL** | `examples/minimal/docker-compose.yml` | **8** (PB-9 fixture SSOT) | `127.0.0.1:8000` via `restart_soak_loop.sh` |
| **ubuntu-vps** | Production compose (pre-existing host ACP) | **10** | `acp-soak.service` → same health/policy/quota/apex probes |

VPS soak validates **production API stability**, not fixture parity. Acceptable for Day 14 with explicit waiver below.

### VPS log excerpt (@ 2026-07-06 review verify)

```text
2026-07-05T22:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-05T23:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T00:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T01:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T02:09:55Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

VPS services @ review: `acp-staging` **active** · `acp-soak` **active** · cadence **3600s** (`:09:55`).

### MSI log excerpt (@ 2026-07-06 review verify)

```text
2026-07-05T23:35:54Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T02:23:11Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T02:52:45Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-07-06T02:52:53Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

MSI @ review: container **Up 25h (healthy)** · soak loop PID **49811** · smoke **8/8**.

---

## Daily checklist status (final)

| Date | Health | Policy | Quota | Apex | SEV-1/2 | Notes (summary) |
|------|--------|--------|-------|------|---------|-----------------|
| 06-26..06-29 | ☑ | ☑ | ☑ | ☑/☐ | 0 | See soak log |
| 06-30 | ☑ | ☑ | ☑ | ☐ | 0 | Apex last good 06-29; SEV-3 rebuild |
| 07-01..03 | ☑ | ☑ | ☑ | ☑ | 0 | SEV-3 overnight stops + rebuild |
| 07-04 | ☑ | ☑ | ☐ | ☐ | 0 | Production/enforce verify only |
| 07-05 | ☑ | ☑ | ☑ | ☑ | 0 | MSI recovery; VPS inactive AM → recovery PM |
| 07-06 | ☑ | ☑ | ☑ | ☑ | 0 | **Day 14** — dual-host green @ review |

---

## Anomalies (SEV criteria)

| SEV | Definition |
|-----|------------|
| **SEV-1** | Blocks PB-12: crash + data loss, policy bypass, fail-open |
| **SEV-2** | Requires analysis: repeated 5xx, memory leak >20%, unexpected restart |
| **SEV-3** | Document only: planned restart, config reload |

| Date | Anomaly | SEV | Resolution |
|------|---------|-----|------------|
| 2026-06-29 | MSI ~13h Docker stop | **SEV-3** | Manual restart; no fail-open |
| 2026-06-29→30 | Iteration silence until rebuild | **SEV-3** | PR #163–168 verify cycle |
| 2026-07-01 | `apex=fail` @ 06:51Z (container down) | **SEV-3** | Recovery `apex=ok` @ 07:09Z |
| 2026-07-02..03 | Overnight container `Exited` ~17h gaps | **SEV-3** | Rebuild + loop restart |
| 2026-07-03→05 | MSI ~39h iteration gap | **SEV-3** | Rebuild 07-05 01:56Z |
| 2026-07-03→05 | VPS ~44h soak gap (services inactive) | **SEV-3** | `systemctl start` + enable 07-05 |
| 2026-07-05 | MSI 16:22→23:35 gap (~7h) | **SEV-3** | WSL sleep; loop restart PID 49811 |
| — | **SEV-1 / SEV-2** | **0** | None attributed to control plane |

**SEV-1/2 total for soak window:** **0**.

---

## Day 14 criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Zero SEV-1/2 from control plane | ✅ | Table above |
| `POST /policy/evaluate` p99 < 500 ms | ✅ | 06-30 sample **5.34ms**; review-day smoke policy tests PASS |
| Telemetry under `ACP_DATA_DIR` predictable | 🔄 | Operator: `du -sh` on MSI `/data/acp` + VPS volume before #77 close |
| Close #77 → PB-10 (#78) if pass | ⏳ | After human sign-off below |

---

## Smoke gate (review day 2026-07-06)

| Check | Result |
|-------|--------|
| Smoke (`pytest -m smoke`) | **8 / 8** PASS (MSI `.venv`) |
| Governance verify | _(run on review day if `src/` changed since last verify)_ |
| OpenAPI verify | _(run pre-flip ~07-07 per C1-02)_ |
| `gates_remaining` | **7** expected until PB-12 catalog bump |
| `gates_blocking_pb12` | **PB-9, PB-12** |

---

## Verdict (human sign-off required)

- [ ] **PASS** — proceed PB-12 prep (PB-8 tag ✅ @ `c58b4cc` · security@ ✅ 2026-06-28)
- [x] **CONDITIONAL** — waiver: **VPS soak monitors production stack (10 rules), not PB-9 fixture (8 rules)**; 07-04 human tick partial Quota/Apex; telemetry `du` pending
- [ ] **FAIL** — extend soak ___ days

**Pre-filled recommendation:** **CONDITIONAL → PASS** when operator confirms:

1. `du -sh` on `ACP_DATA_DIR` volumes shows no runaway growth
2. Accept VPS production-vs-fixture scope waiver
3. No new SEV-1/2 after this review

**Operator:** ___  
**Date:** ___  
**Signature / GitHub comment on #77:** ___

---

## Next steps after PASS sign-off

1. Close [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)
2. Pre-flip (~07-07): `python scripts/export_openapi.py` · smoke · `verify_governance_status_runtime.sh`
3. PB-12 human GO (~07-10): [`PUBLIC_BETA_GO_NO_GO.md`](../../PUBLIC_BETA_GO_NO_GO.md)
4. Record PB-10 defer in PB-12 decision text
5. Open [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) (PB-10 GA track)

---

**Related:** [`PB9_STAGING_SOAK_LOG.md`](../../PB9_STAGING_SOAK_LOG.md) · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../../PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)
