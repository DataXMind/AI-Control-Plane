# AI Control Plane — Project Status Audit (Claude Handoff)

**Document ID:** ACP-GOV-PROJECT-STATUS-AUDIT-CLAUDE-001  
**Audience:** Claude (Anthropic) — architecture, governance, and Public Beta planning sessions  
**Prepared by:** Cursor operator session · reconciled against runtime evidence  
**Audit date:** 2026-06-27 (UTC)  
**Repository:** [DataXMind/AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane)  
**Baseline:** `master` @ `527eb5d` · governance catalog **v1.3.3**

---

## Executive summary

AI Control Plane (ACP) has completed its **technical and documentation surface** for Public Beta preparation. The control plane runtime, governance UX (`GET /governance/status`), legal artifacts, operator RUNBOOK, examples stack, OpenAPI verification, and CI smoke paths are **implemented and evidenced**. What remains is predominantly **operator calendar work** and **human approval gates** — not missing Cursor deliverables.

| Dimension | Status | Confidence |
|-----------|--------|------------|
| Core runtime (policy, health, quota, identity) | ✅ Proven | High — smoke 8/8, CI green |
| Governance catalog 3-stream convergence | ✅ v1.3.3 live | High — runtime verify scripts |
| Practice studies 01–08 | ✅ PASS | High — artifacts in repo |
| Legal / trust (PB-11) | ✅ Closed | High — PR #112–#113 |
| Fork surface (examples, OpenAPI) | ✅ Closed @ #118 | High — CI `examples-minimal-smoke` |
| Staging soak (PB-9 / G-05) | 🔄 In progress | Medium — ticks 06-26/27; Day 14 ~07-06 |
| Clean-machine fork (PB-7) | ⏳ Pending | None on MSI WARM |
| Public flip (PB-12) | ⏳ Pending | Human gate ~07-10 target |

**Critical instruction for Claude:** Do not treat HTML artifact verdicts that state *"KHÔNG CÒN GÌ ĐỂ DELIVER"* as globally true. They are accurate **only for Cursor-coded packets** already merged. **Seven** `public_beta.gates_remaining` entries are still open in `governance_catalog.py` and at runtime.

---

## 1. System anchors (read before any prompt)

These files are the **single source of truth**. Prefer runtime + verify scripts over static JSON samples or HTML copy-paste blocks.

| Anchor | Role |
|--------|------|
| `src/ai_control_plane/core/governance_catalog.py` | Catalog SSOT — gates, gaps, lessons, case studies |
| `GET /governance/status` | Runtime mirror of catalog (+ doc_links) |
| `scripts/verify_governance_status_runtime.sh` | L5 gate — expects `1.3.3`, 13 patterns, 7 gaps / 1 OPEN |
| `scripts/verify_openapi_runtime.sh` | OpenAPI gate — ≥10 paths, key paths (not `/openapi.json` in `paths{}`) |
| `docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md` | Open vs closed task audit |
| `docs/prompts/SESSION_ANCHOR_TEMPLATE.md` | L5 session pin — PB-12 operator checklist |
| `docs/governance/CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md` | Matrix rows DONE vs operator-only |
| Reconciliation docs (`*_RECONCILIATION.md`) | Harsh audit of each Claude HTML packet |

**PACE verify (operator):**

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
docker compose -f examples/minimal/docker-compose.yml up --build -d
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log
```

---

## 2. Artifact chain map (Claude HTML → repo reality)

### 2.1 `practice_studies_architecture_review.html`

| Tab | Intent | Status @ 2026-06-27 |
|-----|--------|---------------------|
| ① Verdict | Operator confidence program; studies maturity | ✅ **Validated** — Studies 01–08 PASS |
| ② Architecture | Governance UX, network topology | ✅ Wired — `/governance/status`, Profile A/B |
| ③ Gap analysis G-01..G-07 | Prioritized gaps | ✅ G-01..G-04, G-06, G-07 **CLOSED**; **G-05 OPEN** (PB-9) |
| ④ Governance UX | Catalog significance | ✅ v1.3.3 · 13 `lessons_patterns` incl. P-13 |
| ⑤ Public Beta readiness | ~78% after studies | ⚠️ **Stale %** — use `gates_remaining` count, not HTML % |
| ⑥ Next steps P0→P3 | Roadmap | ✅ P0/P1 largely done; operator track active |

**Claude action:** Reference study artifacts under `docs/governance/practice-evidence/`. Do not re-prioritize closed gaps.

---

### 2.2 `practice_evidence_action_packets.html`

| Tab | Intent | Status |
|-----|--------|--------|
| P0 catalog sync | `governance_catalog.py` ← 3 streams | ✅ v1.3.3 @ #115 |
| P1a RUNBOOK Windows | netsh portproxy | ✅ #108 |
| P1b LESSONS P-08 | Study 05g-r kill switch | ✅ G-01 CLOSED · P-13 |
| P2 Legal | SECURITY, CONTRIBUTING, CoC | ✅ PB-11 closed #112–#113 |

**Claude action:** No new P0/P1 Cursor prompts unless catalog version bump is explicitly requested.

---

### 2.3 `pb_integration_timeline.html`

| Tab | Intent | Status |
|-----|--------|--------|
| ① Integration map | 3 streams → catalog | ✅ `gates_closed` includes convergence |
| ② Timeline PB flip | 2026-06-26 → 07-15 | 🔄 On track — soak review **~2026-07-06**, flip **~2026-07-10** |
| ③ One-curl demo | Post-P0 JSON shape | ✅ `curl /governance/status` matches |
| ④ Owner matrix | Cursor / Operator / Claude | ✅ Matrix reconciled — Cursor week **DONE** |

---

### 2.4 `pb_final_blockers_packet.html`

| Tab | Intent | Status |
|-----|--------|--------|
| examples/ | docker-compose + README | ✅ `examples/minimal/` + `examples/README.md` — **reject** root `examples/docker-compose.yml` |
| README + maintainer | Status, governance, contact | ✅ #118 — 165 pytest, `security@dataxmind.com` |
| PB gate check | 8/12 done | ⚠️ **Stale framing** — use catalog: **4 closed / 7 remaining** |
| Final checklist 14 items | Tickable | 🔄 Operator items open — see §5 |
| RUNBOOK ops | deploy/rollback/reload/incident | ✅ #118 |

**Reconciliation:** [`PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md`](PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md)

---

### 2.5 `pb_openapi_and_examples_ci.html`

| Tab | Intent | Status |
|-----|--------|--------|
| OpenAPI | Verify `/docs` `/redoc` `/openapi.json` | ✅ `verify_openapi_runtime.sh`, README, OPEN_SOURCE_READINESS |
| examples CI | `examples-smoke` job | ✅ **`examples-minimal-smoke`** @ `examples/minimal/docker-compose.yml` |
| Verdict | "Nothing left to deliver" | ⚠️ **Partial truth** — verdict tab stamped post-merge; Public Beta gates remain |

**Known bug fixed:** Script initially asserted `/openapi.json` inside OpenAPI `paths{}` — incorrect for FastAPI. Fixed @ `1d883ec`.

**Reconciliation:** [`PB_OPENAPI_AND_EXAMPLES_CI_RECONCILIATION.md`](PB_OPENAPI_AND_EXAMPLES_CI_RECONCILIATION.md)

---

## 3. Architecture snapshot

```text
┌─────────────────────────────────────────────────────────────┐
│  L0–L5 Governance (Karpathy)                                 │
│  CLAUDE.md · .cursorrules · CURSOR_RISK_POLICY · LESSONS     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  FastAPI bridge (api/server.py)                              │
│  /health · /policy/evaluate · /governance/status · /apex/*   │
│  OpenAPI 3.1 auto-gen · 13 paths                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   YAML config        ACP_DATA_DIR         Redis (optional)
   ACP_CONFIG_DIR     persistence          quota/tasks
```

**Deployment profiles:**

| Profile | Host | Evidence |
|---------|------|----------|
| A — local Docker | MSI WSL, CI | `examples/minimal/docker-compose.yml` |
| B — remote VPS | ubuntu-vps | Study 08 · `acp-staging.service` |
| CLEAN fork | Separate machine | PB-7 **not** MSI WARM |

---

## 4. Runtime truth (`governance_catalog.py` v1.3.3)

```yaml
public_beta:
  phase: "PB-9 staging soak"
  soak_started: "2026-06-22"
  soak_review_target: "2026-07-06"
  gates_closed:  # 4
    - PB-11 legal artifacts
    - docs/RUNBOOK.md operator SSOT
    - Governance catalog 3-stream convergence
    - GitHub Discussions enabled
  gates_remaining:  # 7
    - PB-9 calendar soak (G-05)
    - PB-7 clean-machine fork ≤15 min
    - PB-10 production soak ≥30d
    - PB-6 OpenAPI publish on flip
    - PB-8 v0.1.0-rc.1 tag
    - security@ mailbox live test (pre-PB-12)
    - PB-12 human go/no-go

known_gaps: 7 total · 1 OPEN (G-05)
lessons_patterns: 13 (incl. P-13 kill switch)
practice_evidence.studies_completed: 8
```

**Verified outputs (2026-06-27):**

| Check | Result | Host |
|-------|--------|------|
| Smoke pytest | 8/8 PASS | MSI WSL |
| Governance runtime | `1.3.3` · 13 patterns | MSI + VPS |
| OpenAPI runtime | `3.1.0` · 13 paths | MSI |
| PB-9 soak iter | PASS @ 11:53Z | MSI Docker |
| CI full suite | PASS | GitHub Actions |
| CI examples-minimal-smoke | PASS ~41s | GitHub Actions |

Artifacts: [`post-merge-runtime-verify-msi-2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/post-merge-runtime-verify-msi-2026-06-27.md)

---

## 5. Public Beta work items (PB-1..12)

| ID | Item | Status | Notes |
|----|------|--------|-------|
| PB-1..4 | Legal docs | ✅ | LICENSE, SECURITY, CONTRIBUTING, CoC |
| PB-5 | examples/minimal | ✅ | SSOT path; CI smoke |
| PB-6 | OpenAPI | ✅ export/runtime · ⏳ **publish on flip** |
| PB-7 | Fork ≤15 min CLEAN | ⏳ | MSI WARM partial only |
| PB-8 | CHANGELOG + rc tag | ⏳ | Human approve @ PB-12 |
| PB-9 | Staging soak ≥14d | 🔄 | Ticks: 06-26, 06-27; gap 06-22→25 no evidence |
| PB-10 | Production soak 30d | ❌ | After PB-9 |
| PB-11 | Branch protection API | ❌ deferred | Free tier 403 → PB-12 |
| PB-12 | Public flip + disclaimer | ❌ | Human go/no-go |

---

## 6. CI pipeline (current)

```text
governance-memory (ML5)
        │
        ▼
     smoke (pytest -m smoke, 8 tests)
        ├──────────────────┐
        ▼                  ▼
     test (full suite)   examples-minimal-smoke
                         (docker compose + verify scripts, timeout 5m)
```

Do **not** add a duplicate `examples-smoke` job at `examples/docker-compose.yml` — path does not exist.

---

## 7. Drift catalog (reject in Claude prompts)

| Stale claim | Correct SSOT |
|-------------|--------------|
| `examples/docker-compose.yml` | `examples/minimal/docker-compose.yml` |
| Job name `examples-smoke` | `examples-minimal-smoke` |
| `/openapi.json` in OpenAPI `paths{}` | URL of spec, not an operation |
| OPEN_SOURCE_READINESS PB-6 ✅ published | Runtime ✅ · static ✅ · **flip publish** ⏳ |
| "PB-9 only gate remaining" | **7** `gates_remaining` |
| "8/12 PB gates done" | **4 closed / 7 remaining** (different taxonomy) |
| MSI WARM verify = PB-7 PASS | PB-7 requires **CLEAN** machine evidence |
| PB-9 PASS before Day 14 | Review target **~2026-07-06** |
| Literal JSON in old Claude samples | Use `verify_*` scripts + live curl |
| 156 tests / old dates in README prompts | **165** pytest @ master |

---

## 8. Operator procedures (Claude must not auto-execute)

| Gate | Trigger for agent | Procedure |
|------|-------------------|-----------|
| PB-9 daily tick | User says *"đã tick ngày YYYY-MM-DD"* | Update [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) |
| PB-9 soak loop | Operator / on request | `bash scripts/restart_soak_loop.sh` or `nohup … --loop 3600` |
| PB-7 | CLEAN machine only | [`pb-7-clean-machine-fork/RUNBOOK.md`](practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md) |
| security@ | Human | [`PB11_LEGAL_AUDIT.md`](PB11_LEGAL_AUDIT.md) §Contact |
| PB-8 tag | Human approve | Post PB-9 |
| PB-12 flip | Human go/no-go | [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) |

**PB-9 soak @ 2026-06-27 PM:** Hourly loop restarted (PID logged in operator session); log `/tmp/acp-soak-staging.log`.

---

## 9. What Claude should do next

### Do

1. **Read** this document + `TASK_AUDIT_REMAINING_2026-06-27.md` at session start.
2. **Audit** any new prompt against §7 Drift catalog before suggesting code changes.
3. **Prepare** Day 14 PB-9 review materials (~2026-07-06): soak log analysis, SEV criteria, gate checklist.
4. **Draft** PB-12 go/no-go narrative from `PUBLIC_BETA_GO_NO_GO.md` — human decides.
5. **Support** PB-7 CLEAN runbook Q&A — do not claim PASS without artifacts.

### Do not

1. Re-open merged Cursor packets (catalog sync, legal, OpenAPI CI, examples).
2. Create duplicate compose files or CI jobs.
3. Close `gates_remaining` in catalog without human approval + evidence.
4. Accelerate PB-9 calendar soak.
5. Treat HTML artifact *"HOÀN TẤT"* as Public Beta completion.

---

## 10. Recent merge history (context)

| Commit | Summary |
|--------|---------|
| `81357d3` | PR #118 — PB-12 checklist, reconciliations, RUNBOOK ops, OpenAPI CI |
| `1d883ec` | Fix OpenAPI runtime verify (`/openapi.json` paths bug) |
| `375ef14` | Verdict stamp on `pb_openapi_and_examples_ci.html` |
| `527eb5d` | PB-9 PM tick + post-merge doc baseline sync |

Prior wave: #116–#117 runtime evidence, #112–#113 legal, #104–#109 governance UX.

---

## 11. Canonical one-liner for Claude sessions

> **AI Control Plane @ `master` `527eb5d`:** Milestones A–C+ closed; Public Beta **IN_PROGRESS** (PB-9 soak). Governance catalog **v1.3.3** live. Technical Cursor packets **merged**. **Seven** operator gates remain until ~**2026-07-06** review and ~**2026-07-10** flip target. Trust runtime `verify_*` scripts and reconciliation docs — not stale HTML prompts.

---

**Related documents**

- [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md)
- [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) §10
- [`practice-evidence/governance-status-v13-verify/RESULTS.md`](practice-evidence/governance-status-v13-verify/RESULTS.md)
- In-repo HTML snapshots: `docs/governance/pb_*.html`

**Last updated:** 2026-06-27 — post PB-9 PM tick · soak loop restart · PR #118 merged
