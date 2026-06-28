# Public Beta — Operator action plan (post Claude status audit)

**Document ID:** ACP-GOV-PB-OPERATOR-PLAN-001  
**Phase:** PB-9 staging soak → PB-12 flip  
**Baseline:** `master` @ **`ac5f017`** · catalog v1.3.3  
**SSOT gates:** `governance_catalog.py` v1.3.3 · `GET /governance/status`  
**Source audit:** [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

---

## Pipeline position

```text
[DONE] Engineering surface (#116–#118, catalog v1.3.3, CI)
[DONE] PB-7 CLEAN PASS (fa71bd5)
[DONE] PB-8 tag @ c58b4cc · CHANGELOG #120 · go/no-go #119
[NOW]  PB-9 soak — ticks through 2026-06-28 · MSI + VPS hourly verified
[WAIT] ~07-06 Day 14 (OP-07)
[WAIT] ~07-07–09 pre-flip: PB-6 export refresh (OP-09) · tag rc.1 already @ c58b4cc (OP-08 ✅)
[WAIT] ~07-10 PB-12 (OP-10)
[POST] PB-10 GA track deferred @ 0.x beta (OP-11)
```

---

## Task register

| ID | Task | Owner | Target | Status | Verify / artifact |
|----|------|-------|--------|--------|-------------------|
| **OP-01** | Daily PB-9 tick | Operator | Daily | 🔄 | Tick **2026-06-28** ✅ — `PB9_STAGING_SOAK_LOG.md` |
| **OP-02** | Soak loop + machine log | Operator | Continuous | ✅ | MSI repo log · VPS hourly PASS — [`vps-hourly-loop-verify-2026-06-28.md`](practice-evidence/pb-9-day14-review/artifacts/vps-hourly-loop-verify-2026-06-28.md) |
| **OP-03** | Gap 06-22→25 documented | Cursor | 2026-06-27 | ✅ | `PB9_STAGING_SOAK_LOG.md` § clock |
| **OP-04** | PB-7 CLEAN fork ≤15 min | Operator | 2026-06-27 | ✅ | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) |
| **OP-05** | PB-7 waiver | Human | — | ❌ **CANCELLED** | OP-04 PASS — no waiver |
| **OP-06a** | security@ mailbox setup | Operator | 2026-06-28 | ✅ | DNS/mailbox provisioned |
| **OP-06b** | security@ live test | Operator | 2026-06-28 | ✅ | [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) PASS |
| **OP-07** | Day 14 PB-9 review | Operator | **~2026-07-06** | ⏳ calendar | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| **OP-08** | PB-8 `v0.1.0-rc.1` tag | Human | Post OP-07 | ✅ early @ `c58b4cc` | Pushed 2026-06-28 — record in PB-12 |
| **OP-09** | PB-6 static OpenAPI | Maintainer | Pre-flip ~07-07 | ⏳ calendar | `export_openapi.py` |
| **OP-10** | PB-12 go/no-go | Human | **~2026-07-10** | ⏳ calendar | **Approve required** |
| **OP-11** | PB-10 prod soak 30d | Operator | Post GA | ❌ deferred | 0.x beta policy |
| **CUR-01** | Soak `--repo-log` | Cursor | 2026-06-27 | ✅ | `soak_staging.sh` |
| **CUR-02** | Day 14 + action plan | Cursor | 2026-06-27 | ✅ | This file |
| **CUR-03** | `.gitattributes` scripts LF | Cursor | 2026-06-28 | ✅ | CRLF lesson PB-7 |
| **CUR-04** | VPS soak `--repo-log` parity | Cursor | 2026-06-28 | ✅ | Separate path — `acp-soak.service` + `pb-9-day14-review/artifacts/` |

---

## Weekly calendar (updated 2026-06-28)

| Week | Dates | Focus | Status |
|------|-------|-------|--------|
| **W1** | 06-27 → 07-03 | OP-01/02 daily · OP-04 ✅ · OP-06b | 🔄 in progress |
| **W2** | 07-04 → 07-06 | OP-07 Day 14 · finish OP-06b | ⏳ |
| **W3** | 07-07 → 07-10 | OP-08/09 · OP-10 | ⏳ human gates |

---

## Phase 1 — Now (daily)

**MSI (WSL):**

```bash
docker compose -f examples/minimal/docker-compose.yml up -d
bash scripts/restart_soak_loop.sh
# → /tmp/acp-soak-staging.log + docs/governance/PB9_SOAK_ITERATION_LOG.md
```

**VPS (after `git pull` + unit install):**

```bash
export ACP_REPO=/root/AI-Control-Plane
sudo cp "$ACP_REPO/examples/minimal/systemd/acp-soak.service" /etc/systemd/system/
sudo sed -i "s|/root/AI-Control-Plane|$ACP_REPO|g" /etc/systemd/system/acp-soak.service
sudo systemctl daemon-reload
sudo systemctl restart acp-staging.service acp-soak.service
tail -3 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
```

Operator daily tick: *"đã tick ngày YYYY-MM-DD"* → [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) only.

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

**Last updated:** 2026-06-28 (VPS hourly verify · #119/#120 merged)
