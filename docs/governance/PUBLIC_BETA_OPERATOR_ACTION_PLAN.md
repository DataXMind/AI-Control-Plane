# Public Beta — Operator action plan (post Claude status audit)

**Document ID:** ACP-GOV-PB-OPERATOR-PLAN-001  
**Phase:** PB-9 staging soak → PB-12 flip  
**Baseline:** `master` @ `fa71bd5` · catalog v1.3.3  
**SSOT gates:** `governance_catalog.py` v1.3.3 · `GET /governance/status`  
**Source audit:** [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

---

## Pipeline position

```text
[DONE] Engineering surface (#116–#118, catalog v1.3.3, CI)
[DONE] PB-7 CLEAN PASS (fa71bd5)
[NOW]  PB-9 soak — ticks through 2026-06-28 · loop + repo log active
[PAR]  security@ — provisioned · live test pending (OP-06b)
[WAIT] ~07-06 Day 14 (OP-07)
[WAIT] ~07-07–09 pre-flip: PB-8 · PB-6 export (OP-08/09)
[WAIT] ~07-10 PB-12 (OP-10)
[POST] PB-10 GA track deferred @ 0.x beta (OP-11)
```

---

## Task register

| ID | Task | Owner | Target | Status | Verify / artifact |
|----|------|-------|--------|--------|-------------------|
| **OP-01** | Daily PB-9 tick | Operator | Daily | 🔄 | Tick **2026-06-28** ✅ — `PB9_STAGING_SOAK_LOG.md` |
| **OP-02** | Soak loop + repo log | Operator | Continuous | ✅ | PID 2408 @ 2026-06-28 · `PB9_SOAK_ITERATION_LOG.md` |
| **OP-03** | Gap 06-22→25 documented | Cursor | 2026-06-27 | ✅ | `PB9_STAGING_SOAK_LOG.md` § clock |
| **OP-04** | PB-7 CLEAN fork ≤15 min | Operator | 2026-06-27 | ✅ | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) |
| **OP-05** | PB-7 waiver | Human | — | ❌ **CANCELLED** | OP-04 PASS — no waiver |
| **OP-06a** | security@ mailbox setup | Operator | 2026-06-28 | ✅ | DNS/mailbox provisioned |
| **OP-06b** | security@ live test | Operator | Before PB-12 | ⏳ | [`security-email-live-test/RUNBOOK.md`](practice-evidence/security-email-live-test/RUNBOOK.md) |
| **OP-07** | Day 14 PB-9 review | Operator | **~2026-07-06** | ⏳ calendar | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| **OP-08** | PB-8 `v0.1.0-rc.1` tag | Human | Post OP-07 | ⏳ calendar | **Approve required** |
| **OP-09** | PB-6 static OpenAPI | Maintainer | Pre-flip ~07-07 | ⏳ calendar | `export_openapi.py` |
| **OP-10** | PB-12 go/no-go | Human | **~2026-07-10** | ⏳ calendar | **Approve required** |
| **OP-11** | PB-10 prod soak 30d | Operator | Post GA | ❌ deferred | 0.x beta policy |
| **CUR-01** | Soak `--repo-log` | Cursor | 2026-06-27 | ✅ | `soak_staging.sh` |
| **CUR-02** | Day 14 + action plan | Cursor | 2026-06-27 | ✅ | This file |
| **CUR-03** | `.gitattributes` scripts LF | Cursor | 2026-06-28 | ✅ | CRLF lesson PB-7 |

---

## Weekly calendar (updated 2026-06-28)

| Week | Dates | Focus | Status |
|------|-------|-------|--------|
| **W1** | 06-27 → 07-03 | OP-01/02 daily · OP-04 ✅ · OP-06b | 🔄 in progress |
| **W2** | 07-04 → 07-06 | OP-07 Day 14 · finish OP-06b | ⏳ |
| **W3** | 07-07 → 07-10 | OP-08/09 · OP-10 | ⏳ human gates |

---

## Phase 1 — Now (daily)

```bash
docker compose -f examples/minimal/docker-compose.yml up -d
bash scripts/restart_soak_loop.sh
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log \
  --repo-log docs/governance/PB9_SOAK_ITERATION_LOG.md
```

---

## Phase 2 — security@ live test (OP-06b)

See [`practice-evidence/security-email-live-test/RUNBOOK.md`](practice-evidence/security-email-live-test/RUNBOOK.md).

---

## Phase 3 — Pre-flip (~07-07) — **wait Day 14 PASS**

```bash
python scripts/export_openapi.py
# Human approve: git tag v0.1.0-rc.1
```

---

## Phase 4 — PB-12 — **human approve**

[`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)

---

**Last updated:** 2026-06-28
