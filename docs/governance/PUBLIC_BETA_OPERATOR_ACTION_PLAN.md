# Public Beta — Operator action plan (post Claude status audit)

**Document ID:** ACP-GOV-PB-OPERATOR-PLAN-001  
**Phase:** PB-9 staging soak → PB-12 flip  
**Baseline:** `master` @ post `ACP_STATUS_AUDIT_ANALYSIS` reconciliation  
**SSOT gates:** `governance_catalog.py` v1.3.3 · `GET /governance/status`  
**Source audit:** Claude `acp_status_audit_analysis.html` — reconciled in [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

---

## Pipeline position

```text
[DONE] Engineering surface (#116–#118, catalog v1.3.3, CI)
   │
   ▼
[NOW]  PB-9 operator soak + evidence persistence
   │
   ├── parallel: PB-7 CLEAN · security@ prep
   ▼
[~07-06] Day 14 review (#77)
   │
   ▼
[~07-07–09] PB-8 rc · PB-6 static refresh · pre-flip checklist
   │
   ▼
[~07-10] PB-12 human go/no-go → public flip
   │
   ▼
[POST] PB-10 production soak (GA track — deferred for 0.x beta)
```

---

## Task register

| ID | Task | Owner | Target | Status | Verify / artifact |
|----|------|-------|--------|--------|-------------------|
| **OP-01** | Daily PB-9 tick | Operator | Daily | 🔄 | *"đã tick ngày …"* → `PB9_STAGING_SOAK_LOG.md` |
| **OP-02** | Soak loop + repo log | Operator | Continuous | 🔄 | `bash scripts/restart_soak_loop.sh` · `PB9_SOAK_ITERATION_LOG.md` |
| **OP-03** | Gap 06-22→25 documented | Cursor | 2026-06-27 | ✅ | `PB9_STAGING_SOAK_LOG.md` § clock |
| **OP-04** | PB-7 CLEAN fork ≤15 min | Operator | 2026-06-30–07-05 | ⏳ | `practice-evidence/pb-7-clean-machine-fork/` |
| **OP-05** | PB-7 waiver (if no CLEAN) | Human | Before PB-12 | ⏳ | `PB7_WAIVER_TEMPLATE.md` |
| **OP-06** | security@ live test | Operator | Before PB-12 | ⏳ | `PB11_LEGAL_AUDIT.md` §Contact |
| **OP-07** | Day 14 PB-9 review | Operator | ~2026-07-06 | ⏳ | `PB9_DAY14_REVIEW_TEMPLATE.md` |
| **OP-08** | PB-8 `v0.1.0-rc.1` tag | Human | Post OP-07 PASS | ⏳ | `CHANGELOG.md` + git tag |
| **OP-09** | PB-6 static OpenAPI refresh | Maintainer | Pre-flip | ⏳ | `python scripts/export_openapi.py` |
| **OP-10** | PB-12 go/no-go | Human | ~2026-07-10 | ⏳ | `PUBLIC_BETA_GO_NO_GO.md` |
| **OP-11** | PB-10 prod soak 30d | Operator | Post GA path | ❌ | **Deferred** for 0.x beta — see § PB-10 |
| **CUR-01** | Soak `--repo-log` | Cursor | 2026-06-27 | ✅ | `soak_staging.sh` |
| **CUR-02** | Day 14 + action plan docs | Cursor | 2026-06-27 | ✅ | This file |

---

## Weekly calendar

| Week | Dates | Focus |
|------|-------|-------|
| **W1** | 2026-06-27 → 07-03 | OP-01/02 daily · start OP-04 CLEAN attempt |
| **W2** | 2026-07-04 → 07-06 | OP-07 Day 14 review · OP-06 security@ |
| **W3** | 2026-07-07 → 07-10 | OP-08/09 pre-flip · OP-10 PB-12 decision |

---

## Phase 1 — Now (daily)

```bash
docker compose -f examples/minimal/docker-compose.yml up -d
bash scripts/restart_soak_loop.sh
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log \
  --repo-log docs/governance/PB9_SOAK_ITERATION_LOG.md
```

Operator: *"đã tick ngày YYYY-MM-DD"* → agent updates daily row only.

---

## Phase 2 — PB-7 CLEAN (parallel)

```bash
# CLEAN machine only — see practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md
git clone https://github.com/DataXMind/AI-Control-Plane
cd AI-Control-Plane
docker compose -f examples/minimal/docker-compose.yml up --build -d
export ACP_API_URL=http://localhost:8000
bash scripts/verify_governance_status_runtime.sh
# wall clock ≤15 min → save artifact
```

**SSOT path:** `examples/minimal/docker-compose.yml` from repo root — **not** `cd examples/` + root compose.

---

## Phase 3 — Pre-flip (~07-07)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
python scripts/export_openapi.py
git add docs/openapi/openapi.json
pytest tests/test_smoke.py -v -m smoke
bash scripts/verify_openapi_runtime.sh
# Human: git tag v0.1.0-rc.1 && git push origin v0.1.0-rc.1
```

**Reject:** `curl … > docs/openapi.json` — use `scripts/export_openapi.py` → `docs/openapi/openapi.json`.

---

## Phase 4 — PB-12 flip (human)

See [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) § Pre-flip checklist.

---

## PB-10 scope (0.x beta)

**Policy @ 2026-06-27:** PB-10 (production soak ≥30d) is **required for GA (1.0.0)** per `OPEN_SOURCE_READINESS.md`, **not** a hard blocker for **0.x Public Beta flip** if explicitly accepted in PB-12 go/no-go record.

`gates_remaining` still lists PB-10 until human closes or reclassifies at catalog bump — do not remove from runtime without maintainer approve.

---

## Drift guard (Claude sessions)

Always read [`PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`](PROJECT_STATUS_AUDIT_FOR_CLAUDE.md) + this plan before suggesting new code.

---

**Last updated:** 2026-06-27
