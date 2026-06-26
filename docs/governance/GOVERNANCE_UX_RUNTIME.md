# Governance UX — Runtime Features & Case Studies

**Document ID:** ACP-GOV-UX-RUNTIME-001  
**API:** `GET /governance/status`  
**CLI:** `agentctl gov status` (`--json`)  
**Catalog SSOT:** `src/ai_control_plane/core/governance_catalog.py`

---

## Why runtime governance UX?

Operators and integrators need **actionable governance state at runtime**, not only static markdown. The endpoint answers: *milestones, 6-layer map, verify commands, case studies, Public Beta gate* — in one JSON call.

```bash
curl -s http://localhost:8000/governance/status | python3 -m json.tool
export ACP_API_URL=http://localhost:8000
agentctl gov status
agentctl gov status --json
```

---

## Case studies (real project history)

### CS-01 — Monolithic PR risk (L3)

| Field | Value |
|-------|--------|
| **Occurred** | PR #48 (MB bulk), PR #63 (MC-1..11 single PR) |
| **Runtime check** | PR diff LOC + mixed risk levels before merge |
| **Action** | Split PR; HIGH max 300 LOC; see `CURSOR_RISK_POLICY.md` |
| **API field** | `case_studies[0]` |

### CS-02 — Doc-only scope creep (L3)

| Field | Value |
|-------|--------|
| **Occurred** | agent4 config merged in doc-only PR #46 |
| **Runtime check** | PR file allowlist — docs-only must not touch `src/` |
| **Action** | Reclassify as MEDIUM if `src/` needed |

### CS-03 — GitHub auto-close (L5)

| Field | Value |
|-------|--------|
| **Occurred** | `Closes #52..#62` only closed #52 |
| **Runtime check** | PR template individual `Closes #N` |
| **Action** | Never use issue ranges |

### CS-04 — Silent ABAC assumption (L0)

| Field | Value |
|-------|--------|
| **Occurred** | GAP-ABAC-2 during `config/loader.py` work |
| **Runtime check** | L0 pre-flight: list condition keys handled vs skipped |
| **Action** | Ask before editing `core/policies.py` / loader |

### CS-05 — Staging soak PB-9 (L4)

| Field | Value |
|-------|--------|
| **Occurred** | Public Beta blocked until soak ≥14 days (started 2026-06-22) |
| **Runtime check** | `/health` + `scripts/soak_staging.sh` + `PB9_STAGING_SOAK_LOG.md` |
| **Action** | Review target **2026-07-06** before PB-10 |

### CS-06 — Fail-closed policy (L4)

| Field | Value |
|-------|--------|
| **Occurred** | SMK-04 unknown agent → deny with reason |
| **Runtime check** | `POST /policy/evaluate` + smoke gate |
| **Action** | TS PolicyClient DENY when API unreachable |

---

## Process-layer case studies (CS-01, CS-03, CS-04)

CS-01, CS-03, and CS-04 describe **process governance** (PR review, GitHub hygiene, L0 assumptions). They are **not** validated by operator `curl` drills — there is no runtime HTTP proof path.

| ID | Validation path |
|----|-----------------|
| **CS-01** | PR template LOC + risk levels; `CURSOR_RISK_POLICY.md` |
| **CS-03** | Individual `Closes #N` in PR body; `LESSONS_LEARNED.md` P-07 |
| **CS-04** | L0 pre-flight before loader edits; `LESSONS_LEARNED.md` P-04 |

Runtime `case_studies[]` in `/governance/status` lists these for **onboarding visibility** only. Hands-on runtime evidence covers CS-02, CS-05, CS-06 via practice studies and smoke gate.

**Gap G-04:** Addressed by this section — do not claim CS-01/03/04 as operator-drill PASS.

---

## Response schema (summary)

| Field | Purpose |
|-------|---------|
| `framework` | `6-layer-karpathy` |
| `milestones` | A/B/C/C+ CLOSED; Public Beta IN_PROGRESS |
| `layers` | L0–L5 one-line summary |
| `verify_gate` | Commands from `.cursorrules` L4 |
| `doc_links` | Paths to governance markdown (incl. `behavioral_constitution`, `cursor_risk_policy`, `lessons_learned`, `practice_evidence_index`) |
| `public_beta` | PB-9 soak metadata |
| `case_studies` | CS-01..CS-06 with `runtime_check` + `action` |
| `lessons_patterns` | P-01..P-12 from `LESSONS_LEARNED.md` (summary; `case_study_id` links P→CS where applicable) |
| `known_gaps` | G-01..G-07 from practice evidence audit (OPEN/CLOSED) |
| `practice_evidence` | Studies 01–08 summary, hosts, topologies, `open_gaps_count`, index URLs |
| `config_loaded`, `policy_rules_count` | Live wire proof (like `/health`) |

---

## Verify gate (PACE L4) — two layers

| Layer | Where | Commands |
|-------|-------|----------|
| **Repo** (pre-merge) | WSL or VPS clone | `ruff check src/ tests/` then `mypy src/ai_control_plane/ --strict` — **not** `ruff + mypy` |
| | | `pytest tests/ -v` · `pytest -m smoke` (8/8) |
| | | `bash scripts/verify_governance_memory.sh` (ML5 doc links) |
| **Runtime** (post-deploy) | API host | `export ACP_API_URL=http://127.0.0.1:8000` |
| | | `bash scripts/verify_governance_status_runtime.sh` (catalog v1.3+) |

**Run scripts from repo root** (`~/AI-Control-Plane`), not from `scripts/`:

```bash
cd ~/AI-Control-Plane
bash scripts/verify_governance_status_runtime.sh   # correct
# bash scripts/verify_governance_status_runtime.sh   # wrong if cwd = scripts/
```

**Do not hand-edit** `verify_governance_status_runtime.sh` — it is not the same as `verify_governance_memory.sh`. If you created the file with `nano`, remove it before `git pull`:

```bash
rm -f scripts/verify_governance_status_runtime.sh
git pull origin master
```

**Expected runtime output:**

```text
OK: governance/status runtime verify 1.3.1 12 patterns
```

After every merge touching `src/`: `git pull` + `sudo systemctl restart acp-staging.service` (VPS) or `docker compose up -d --build` (local).

Evidence: [`practice-evidence/governance-status-v13-verify/RESULTS.md`](practice-evidence/governance-status-v13-verify/RESULTS.md).

---

## When to use vs `/health`

| Endpoint | Use when |
|----------|----------|
| `/health` | CI smoke, config wire proof, k8s liveness |
| `/governance/status` | On-call governance checklist, pre-merge review, onboarding |

**Operator verify (catalog v1.3):** After merges touching `src/`, rebuild Docker staging then:

```bash
bash scripts/verify_governance_status_runtime.sh   # ACP_API_URL defaults to http://127.0.0.1:8000
```

See also [`practice-evidence/governance-status-v13-verify/RESULTS.md`](practice-evidence/governance-status-v13-verify/RESULTS.md) (v1.3) and [`governance-status-v12-verify/RESULTS.md`](practice-evidence/governance-status-v12-verify/RESULTS.md) (v1.2).

**Hands-on evidence (operator runs):** [`practice-evidence/`](practice-evidence/) — Studies 01–08 PASS.  
**Audit pack:** [`practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md).  
**Drift / next phase:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) · [`GOVERNANCE_NEXT_PHASE_PLAN.md`](GOVERNANCE_NEXT_PHASE_PLAN.md).

**Last updated:** 2026-06-26 — catalog v1.3.1: doc_links aliases + practice_evidence metadata

**Note on CS-01/03/04:** Process-layer governance — validated via `LESSONS_LEARNED.md` P-01..P-04 and `lessons_patterns[]`, not operator runtime drill. **G-01..G-04, G-06, G-07: CLOSED** @ 2026-06-26. **G-05 OPEN** — PB-9 calendar soak until ~2026-07-06. Supersedes stale Claude sync prompt (pre-PR #99).
