# Governance task audit — remaining work @ 2026-06-27

**Document ID:** ACP-GOV-TASK-AUDIT-REMAINING-001  
**Baseline:** `master` catalog **v1.3.3** @ `375ef14` (post #118 merge + verdict stamp) · runtime PASS local + VPS (#116–#117)  
**Purpose:** Rà soát task đã đóng vs còn mở — sync với 3-stream convergence.

---

## Closed since wave start (do not re-open)

| Track | ID | Evidence | Status |
|-------|-----|----------|--------|
| G0–G2 | Practice gaps | Studies + G2-1..G2-5 | ✅ CLOSED |
| Gov UX | Catalog v1.3.x | PR #104–#109; v1.3.3 gates_remaining | ✅ |
| OpenAPI + examples CI | PB-T packet | PR #118 merged @ `375ef14` | ✅ |
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

| Priority | ID | Owner | Target |
|----------|-----|-------|--------|
| **P0** | PB-9 / G-05 | Operator daily tick | ~2026-07-06 |
| **P1** | PB-7 clean fork | **CLEAN machine** — not MSI WARM | Before PB-12 |
| **P1** | PB-10 prod soak 30d | Operator | After PB-9 |
| **P2** | PB-6 OpenAPI publish | Maintainer on flip | PB-12 |
| **P2** | PB-8 rc tag | Human approve | Post PB-9 |
| **Pre-flip** | security@ live test | DNS/mailbox | Before PB-12 |
| **CRITICAL** | PB-12 flip | Human go/no-go | End |

**PB-9 ticks:** `2026-06-26`, `2026-06-27` (PM post-merge tick @ `375ef14`) — see [`PB9_STAGING_SOAK_LOG.md`](../../../PB9_STAGING_SOAK_LOG.md).

---

## Operator checklist — PB-12 gates (chờ bạn / calendar)

> **Pin:** copy block này vào session anchor · SSOT: file này + `curl /governance/status` → `public_beta.gates_remaining`

### Chờ calendar / operator

- [ ] **PB-9** — daily tick (*"đã tick ngày YYYY-MM-DD"* → [`PB9_STAGING_SOAK_LOG.md`](../../../PB9_STAGING_SOAK_LOG.md)); review **~2026-07-06** (Day 14)
- [ ] **PB-7** — CLEAN laptop/VM (≤15 min); **không** MSI WARM — [`pb-7-clean-machine-fork/RUNBOOK.md`](../../pb-7-clean-machine-fork/RUNBOOK.md)
- [ ] **security@** — mailbox + email thử — [`PB11_LEGAL_AUDIT.md`](../../../PB11_LEGAL_AUDIT.md) §Contact setup

### Sau PB-9 / lúc flip

- [ ] **PB-10** — production soak ≥30d
- [ ] **PB-8** — tag `v0.1.0-rc.1` (human approve)
- [ ] **PB-6** — OpenAPI publish on flip
- [ ] **PB-12** — human go/no-go

### Không claim sớm

- PB-7 PASS chỉ với evidence **CLEAN** (MSI WARM ≠ PB-7)
- PB-9 PASS trước Day 14 (~2026-07-06)
- CS-01/03/04 — process-layer; không operator runtime drill

**PB-9 ticks done:** 2026-06-26, 2026-06-27 (incl. post-merge PM tick)

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

**Do not claim:** PB-7 PASS without CLEAN evidence; PB-9 PASS before Day 14; CS-01/03/04 runtime drill.
