# Public Beta — Operator action plan (post Claude status audit)

**Document ID:** ACP-GOV-PB-OPERATOR-PLAN-001  
**Phase:** PB-12 **SHIPPED** @ 2026-07-06 → PB-10 GA track  
**Baseline:** `master` @ **`a5d5776`** · catalog **v1.6.0**  
**SSOT gates:** `governance_catalog.py` v1.6.0 · `GET /governance/status` · `gates_remaining=1` (PB-10)  
**Source audit:** [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

---

## Pipeline position

```text
[DONE] Engineering surface · CI · pytest 221
[DONE] PB-7 CLEAN PASS · PB-8 rc @ c58b4cc
[DONE] PB-9 soak + Day 14 PASS @ 2026-07-06 (#77 closed)
[DONE] C1-02 pre-flip @ 2026-07-06 (export · smoke · verify · 221 pytest)
[DONE] PB-12 GO @ 2026-07-06 — PUBLIC · v0.1.0-beta.1 · catalog v1.6.0
[NOW]  POST_FLIP @ 07-07: coverage ≥85% verify · Codecov · Tier 3 backlog
[NOW]  PB-10 GA clock (#78) · PB-11 branch protection probe
```

---

## Task register

| ID | Task | Owner | Target | Status | Verify / artifact |
|----|------|-------|--------|--------|-------------------|
| **OP-01** | Daily PB-9 tick | Operator | Daily | ✅ **ENDED** 07-06 | Last tick **2026-07-06** Day 14 — `PB9_STAGING_SOAK_LOG.md` |
| **OP-02** | Soak loop + machine log | Operator | Continuous | ✅ | MSI repo log · VPS hourly PASS — [`vps-hourly-loop-verify-2026-06-28.md`](practice-evidence/pb-9-day14-review/artifacts/vps-hourly-loop-verify-2026-06-28.md) |
| **OP-03** | Gap 06-22→25 documented | Cursor | 2026-06-27 | ✅ | `PB9_STAGING_SOAK_LOG.md` § clock |
| **OP-04** | PB-7 CLEAN fork ≤15 min | Operator | 2026-06-27 | ✅ | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) |
| **OP-05** | PB-7 waiver | Human | — | ❌ **CANCELLED** | OP-04 PASS — no waiver |
| **OP-06a** | security@ mailbox setup | Operator | 2026-06-28 | ✅ | DNS/mailbox provisioned |
| **OP-06b** | security@ live test | Operator | 2026-06-28 | ✅ | [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) PASS |
| **OP-07** | Day 14 PB-9 review | Operator | **2026-07-06** | ✅ PASS | [`pb-9-day14-review/RESULTS.md`](practice-evidence/pb-9-day14-review/RESULTS.md) · #77 closed |
| **OP-08** | PB-8 `v0.1.0-rc.1` tag | Human | Pre-flip | ✅ @ `c58b4cc` | Do not re-tag |
| **OP-09** | PB-6 static OpenAPI | Maintainer | **2026-07-06** | ✅ | `export_openapi.py` @ pre-flip |
| **OP-10** | PB-12 go/no-go | Human | **2026-07-06** | ✅ GO | [`pb-12-public-flip/RESULTS.md`](practice-evidence/pb-12-public-flip/RESULTS.md) |
| **OP-11** | PB-10 prod soak 30d | Operator | Post-flip | 🔄 **NOW** | #78 — deferred GA policy |
| **CUR-01** | Soak `--repo-log` | Cursor | 2026-06-27 | ✅ | `soak_staging.sh` |
| **CUR-02** | Day 14 + action plan | Cursor | 2026-06-27 | ✅ | This file |
| **CUR-03** | `.gitattributes` scripts LF | Cursor | 2026-06-28 | ✅ | CRLF lesson PB-7 |
| **CUR-04** | VPS soak `--repo-log` parity | Cursor | 2026-06-28 | ✅ | Separate path — `acp-soak.service` + `pb-9-day14-review/artifacts/` |

---

## Weekly calendar (updated 2026-07-07)

| Week | Dates | Focus | Status |
|------|-------|-------|--------|
| **W1** | 06-27 → 07-03 | OP-01/02 daily · OP-04 ✅ · OP-06b | ✅ |
| **W2** | 07-04 → 07-06 | OP-07 Day 14 · OP-09/10 flip | ✅ SHIPPED |
| **W3** | 07-07+ | POST_FLIP coverage · PB-10 #78 · PB-11 | 🔄 in progress |

---

## Phase 1 — Post-flip ops (2026-07-07+)

- **MSI/VPS:** `git pull origin master` → sync **`a5d5776`+**
- **Coverage:** run checklist in [`POST_FLIP_COVERAGE_REMINDER.md`](POST_FLIP_COVERAGE_REMINDER.md)
- **PB-10:** track [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78)
- **Optional:** keep MSI soak loop for ops — no new PB-9 human ticks

*(Historical Phase 1 daily soak commands archived — see git history @ 2026-06-28.)*

---

## Phase 2 — security@ live test (OP-06b)

See [`practice-evidence/security-email-live-test/RUNBOOK.md`](practice-evidence/security-email-live-test/RUNBOOK.md).

---

## Phase 3 — Pre-flip — **DONE @ 2026-07-06**

See [`pb-12-public-flip/RESULTS.md`](practice-evidence/pb-12-public-flip/RESULTS.md) · residual coverage verify @ [`POST_FLIP_COVERAGE_REMINDER.md`](POST_FLIP_COVERAGE_REMINDER.md).

---

## Phase 4 — PB-12 — **DONE @ 2026-07-06**

[`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`pb-12-public-flip/RESULTS.md`](practice-evidence/pb-12-public-flip/RESULTS.md)

---

**Last updated:** 2026-07-07 · PB-12 SHIPPED · post-flip coverage reminder open
