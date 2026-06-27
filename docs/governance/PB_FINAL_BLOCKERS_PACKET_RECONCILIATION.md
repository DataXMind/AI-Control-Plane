# Claude PB final blockers packet — reconciliation

**Document ID:** ACP-GOV-PB-FINAL-BLOCKERS-RECON-001  
**Audit date:** 2026-06-27  
**Baseline:** `master` @ `8114f0d` (catalog v1.3.3)  
**Source artifact:** [`pb_final_blockers_packet.html`](pb_final_blockers_packet.html) (Claude HTML tabs)  
**Operator gates not done:** PB-9 daily · PB-7 CLEAN · security@ live · PB-10/8/6/12

---

## Verdict

| Question | Answer |
|----------|--------|
| Execute HTML prompts literally? | **No** — ~70% rows **DONE** or **superseded** |
| Any new Cursor code/docs work? | **RUNBOOK** ops sections (deploy/rollback/reload/incident) — wired @ recon PR |
| Block PB-12 today? | **Operator calendar + human gates only** |

---

## Tab: examples/ docker-compose

| HTML claim | Current project | Action |
|------------|-----------------|--------|
| `examples/` root + `.env.example` | **`examples/minimal/`** SSOT + **`examples/README.md`** index | ✅ Recon PR (no duplicate compose) |
| `COPY config/` in Dockerfile | **Invalid** — use `tests/fixtures/config` | ❌ Do not apply Claude Dockerfile |
| `ACP_DEV_MODE` / `ACP_LOG_LEVEL` | **Not in codebase** | ❌ Ignore |
| `cd examples/` + compose | Use `examples/minimal/` or `-f examples/minimal/docker-compose.yml` | ✅ Documented |
| Fork ≤15 min | PB-7 RUNBOOK Path A + MSI WARM partial | ⏳ PB-7 **CLEAN** pending |
| `governance/status` + verify script | `examples/minimal/README.md` | ✅ |

**Do not** duplicate `examples/docker-compose.yml` at repo root — SSOT is `examples/minimal/`.

### Claude `examples/` prompt — harsh audit (@ 2026-06-27)

| Element | Verdict | Reason |
|---------|---------|--------|
| New `examples/Dockerfile` | **REJECT** | Breaks build: no `config/` dir; SSOT `examples/minimal/Dockerfile` copies `tests/fixtures/config` |
| `version: "3.9"` compose | **REJECT** | Compose v2; minimal file has no obsolete `version` key |
| `.env.example` with fake vars | **PARTIAL** | Added `examples/minimal/.env.example` with **real** `ACP_*` only |
| `examples/README.md` hub | **ACCEPT** | Index → `minimal/`; satisfies OPEN_SOURCE_READINESS wording |
| README status banner | **PARTIAL** | Added accurate banner — **165** pytest, PB-9 ~2026-07-06 (not stale 156 / 07-10) |
| README governance section | **PARTIAL** | Already in quick start; dedicated § with `verify_governance_status_runtime.sh` |
| README maintainer | **DONE** | `security@dataxmind.com` + Discussions — no `[MAINTAINER_EMAIL]` |
| `cd examples/` + `.env` compose | **REJECT** | Use `examples/minimal/` — see [`examples/README.md`](../../examples/README.md) |
| `150+` → `156` tests | **REJECT** | CI truth: **165** pytest @ `master` |

### Claude README prompt — harsh audit (@ 2026-06-27)

| # | Claude row | Verdict |
|---|------------|---------|
| 1 | Status: C CLOSED · **156** tests | **REJECT count** — use **165**; C+ also CLOSED in catalog |
| 2 | PB target **~2026-07-10** | **REJECT** — catalog `soak_review_target` **2026-07-06** |
| 3 | Governance after install w/o `ACP_CONFIG_DIR` | **REJECT** — fails wiring; SSOT quick start + verify script |
| 4 | `cd examples/` docker compose | **REJECT** — `examples/minimal/` + `-f` or `cd examples/minimal` |
| 5 | Maintainer + SECURITY | **DONE** @ #112–#113 |
| 6 | Fill `[MAINTAINER_EMAIL]` | **STALE** — already `security@dataxmind.com` |

| `pip install ai-control-plane` | **REJECT** | Pre–public beta; use `pip install -e ".[dev]"` |
| CLI assign/status | **ACCEPT** (fixed) | `agentctl assign PROJECT AGENT TASK` · `status --project` |
| Verify block | **ACCEPT** | Uses `verify_governance_status_runtime.sh` not stale JSON sample |


---

## Tab: README + maintainer

| HTML row | Status | Notes |
|----------|--------|-------|
| Milestone B / 150+ tests | **Stale** | README: **165 pytest**, Milestone C CLOSED |
| Governance check section | Partial | CONTRIBUTING + PB-7; optional README pointer |
| `examples/` link | ✅ | `examples/minimal/README.md` |
| Maintainer + SECURITY | ✅ | #112–#113 · `security@dataxmind.com` in README |
| `[MAINTAINER_EMAIL]` placeholder | **Stale** | Filled in SECURITY.md @ #113 |

---

## Tab: PB gate final check

| HTML "REMAINING" | Reality @ v1.3.3 |
|------------------|------------------|
| PB-9 soak | ⏳ **OPEN** (G-05) — operator |
| PB-11 legal trio | ✅ **CLOSED** (`gates_closed`) |
| RUNBOOK complete | Partial — Windows/Docker ✅; Linux ops sections added in recon PR |
| G-01 kill switch | ✅ **CLOSED** (Study 05g-r, P-13) |
| G-06 Study 08 | ✅ **CLOSED** |
| 8/12 gates DONE | **Stale count** — use `curl …/governance/status \| jq .public_beta` |

---

## Tab: Final checklist (14 items)

| Group | HTML items | Status |
|-------|------------|--------|
| Hôm nay Cursor | examples/, README, RUNBOOK | examples ✅ · README mostly ✅ · RUNBOOK ops ⏳→✅ recon |
| Hôm nay Bạn | MAINTAINER_EMAIL, docker compose verify | Email ✅ · operator verify optional |
| Tuần này | legal, 05g, 08, catalog, 6-layer | **All DONE** |
| ~07-06 | soak 14d, OSR review, approve flip | ⏳ calendar |
| ~07-10 | tag beta.1, GitHub public | ⏳ PB-8/12 — use **rc.1** per sprint plan |

---

## Task mới thực sự cần làm (2026-06-27)

### Operator — chờ bạn (không Cursor)

| # | Task | Cách làm |
|---|------|----------|
| 1 | **PB-9 daily tick** | Mỗi ngày soak PASS → nói *"đã tick ngày YYYY-MM-DD"* → [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) |
| 2 | **PB-7 CLEAN fork** | Laptop sạch → [`pb-7-clean-machine-fork/RUNBOOK.md`](practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md) ≤15 min |
| 3 | **security@ live test** | Provision mailbox → gửi email thử → [`PB11_LEGAL_AUDIT.md`](PB11_LEGAL_AUDIT.md) |
| 4 | **~2026-07-06** | Review soak Day 14 → go/no-go prep |
| 5 | **PB-10 → PB-8 → PB-6 → PB-12** | Sau PB-9 / human approve |

### Cursor — đã xử lý trong recon PR

| # | Task | Artifact |
|---|------|----------|
| R1 | RUNBOOK: Linux deploy, rollback, config reload, incident | [`docs/RUNBOOK.md`](../RUNBOOK.md) |
| R2 | `examples/minimal/README` — governance verify | [`examples/minimal/README.md`](../../examples/minimal/README.md) |
| R3 | HTML + this recon in repo | Historical + SSOT pointer |
| R4 | `examples/README.md` index + `minimal/.env.example` + expanded minimal README | No duplicate compose/Dockerfile |
| R5 | README status banner + governance § (audit-safe) | No stale 156/07-10; links Discussions |

### Không làm (stale / done)

- Tạo `examples/` root tree từ HTML (Dockerfile `COPY config/`, fake env vars)
- SECURITY / CONTRIBUTING / CoC packets
- Study 05g-r, 08, catalog P0, 6-layer PR
- Đếm gate "8/12" từ HTML

---

## Verify

```bash
bash scripts/verify_governance_status_runtime.sh
curl -s "$ACP_API_URL/governance/status" | jq '.public_beta'
```

**Related:** [`CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md`](CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md) · [`TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md)
