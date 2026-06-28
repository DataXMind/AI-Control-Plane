# Governance task audit — remaining work @ 2026-06-27

**Document ID:** ACP-GOV-TASK-AUDIT-REMAINING-001  
**Baseline:** `master` @ `65dc089` · catalog **v1.3.3**  
**Purpose:** Rà soát task đã đóng vs còn mở — sync với 3-stream convergence.

---

## Closed since wave start (do not re-open)

| Track | ID | Evidence | Status |
|-------|-----|----------|--------|
| G0–G2 | Practice gaps | Studies + G2-1..G2-5 | ✅ CLOSED |
| Gov UX | Catalog v1.3.x | PR #104–#109; v1.3.3 gates_remaining | ✅ |
| OpenAPI + examples CI | PB-T packet | PR #118 merged @ `375ef14` | ✅ |
| Claude status audit | Operator phase plan | `ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md` | ✅ |
| Soak repo persistence | `--repo-log` + iteration log | `soak_staging.sh` @ 2026-06-27 | ✅ |
| PB-7 CLEAN fork | Ubuntu @ MSI Path A Docker | [`pb-7-clean-machine-fork/RESULTS.md`](../../practice-evidence/pb-7-clean-machine-fork/RESULTS.md) | ✅ |
| security@ mailbox | Provisioned + live test | [`security-email-live-test/RESULTS.md`](../../practice-evidence/security-email-live-test/RESULTS.md) PASS @ 2026-06-28 |
| Lessons | P-13 kill switch | G2-1 + CURSOR_RISK §10 | ✅ |
| Legal | PB-11 | PR #112–#113, sign-off | ✅ |
| RUNBOOK | Operator SSOT | PR #108 | ✅ |
| Discussions | GitHub feature | Enabled @ 2026-06-27 | ✅ |
| 3-stream | Claude convergence | `gates_closed` in catalog | ✅ |

**`known_gaps` runtime:** 7 total · **1 OPEN** (`G-05` PB-9 only).

---

## Runtime v1.3.3 evidence (closed @ 2026-06-27)

| Host | Artifact |
|------|----------|
| WSL local | [`local-runtime-v133-pass.md`](local-runtime-v133-pass.md) |
| ubuntu-vps | [`vps-runtime-v133-pass.md`](vps-runtime-v133-pass.md) |

---

## OPEN — blocks PB-12 (`public_beta.gates_remaining`)

> **Execution detail:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../../../PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) (OP-01..11)

| Priority | ID | Owner | Target |
|----------|-----|-------|--------|
| **P0** | PB-9 / G-05 | Operator daily tick | ~2026-07-06 |
| **P1** | PB-7 clean fork | **CLEAN** — Ubuntu @ MSI 2026-06-27 | ✅ PASS — [`RESULTS.md`](../../pb-7-clean-machine-fork/RESULTS.md) |
| **P1** | PB-10 prod soak 30d | Operator | After PB-9 |
| **P2** | PB-6 OpenAPI publish | Maintainer on flip | PB-12 |
| **P2** | PB-8 rc tag | Human approve | Post PB-9 |
| **Pre-flip** | security@ live test | Operator | 2026-06-28 | ✅ PASS |
| **CRITICAL** | PB-12 flip | Human go/no-go | End |

**PB-9 ticks:** `2026-06-26`, `2026-06-27`, `2026-06-28` — see [`PB9_STAGING_SOAK_LOG.md`](../../../PB9_STAGING_SOAK_LOG.md).

---

## Operator checklist — PB-12 gates (chờ bạn / calendar)

> **Pin:** copy block này vào session anchor · SSOT: file này + `curl /governance/status` → `public_beta.gates_remaining`

### Chờ calendar / operator

- [ ] **PB-9** — daily tick (*"đã tick ngày YYYY-MM-DD"* → [`PB9_STAGING_SOAK_LOG.md`](../../../PB9_STAGING_SOAK_LOG.md)); review **~2026-07-06** (Day 14)
- [x] **PB-7** — CLEAN fork ≤15 min — **PASS** Ubuntu @ MSI 2026-06-27 — [`pb-7-clean-machine-fork/RESULTS.md`](../../pb-7-clean-machine-fork/RESULTS.md)
- [x] **security@** — live test **PASS** 2026-06-28 — [`security-email-live-test/RESULTS.md`](../../practice-evidence/security-email-live-test/RESULTS.md)

### Sau PB-9 / lúc flip

- [ ] **PB-10** — production soak ≥30d
- [ ] **PB-8** — tag `v0.1.0-rc.1` (human approve)
- [ ] **PB-6** — OpenAPI publish on flip
- [ ] **PB-12** — human go/no-go

### Không claim sớm

- PB-7 PASS chỉ với evidence **CLEAN** (MSI WARM ≠ PB-7)
- PB-9 PASS trước Day 14 (~2026-07-06)
- CS-01/03/04 — process-layer; không operator runtime drill

**PB-9 ticks done:** 2026-06-26, 2026-06-27, 2026-06-28

---

## Reminders (agent rules)

| Reminder | Rule |
|----------|------|
| **PB-9 daily** | Agent tick **only** on *"đã tick ngày YYYY-MM-DD"* |
| **PB-7** | Không ghi PASS nếu không có CLEAN artifacts |
| **Code/docs fork-user** | **Done** @ #117 — không mở lại Claude JSON sample |
| **Claude responsibility matrix** | **Done** @ matrix recon doc — TODAY/THIS WEEK closed; chờ operator |
| **PB final blockers HTML** | **Reconciled** — see [`PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md`](../../../PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md) |

**Matrix SSOT:** [`CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md`](../../../CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md)

**Claude handoff (full audit):** [`PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`](../../../PROJECT_STATUS_AUDIT_FOR_CLAUDE.md)

**Operator action plan:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../../../PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · Claude audit recon: [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](../../../ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

**Do not claim:** ~~PB-7 PASS without CLEAN evidence~~ PB-7 practice PASS @ Ubuntu MSI; catalog may still list until bump; PB-9 PASS before Day 14; CS-01/03/04 runtime drill.
