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

## Response schema (summary)

| Field | Purpose |
|-------|---------|
| `framework` | `6-layer-karpathy` |
| `milestones` | A/B/C/C+ CLOSED; Public Beta IN_PROGRESS |
| `layers` | L0–L5 one-line summary |
| `verify_gate` | Commands from `.cursorrules` L4 |
| `doc_links` | Paths to governance markdown |
| `public_beta` | PB-9 soak metadata |
| `case_studies` | CS-01..CS-06 with `runtime_check` + `action` |
| `config_loaded`, `policy_rules_count` | Live wire proof (like `/health`) |

---

## When to use vs `/health`

| Endpoint | Use when |
|----------|----------|
| `/health` | CI smoke, config wire proof, k8s liveness |
| `/governance/status` | On-call governance checklist, pre-merge review, onboarding |

**Hands-on evidence (operator runs):** [`practice-evidence/`](practice-evidence/) — Studies 01–06 PASS; Study 07 cross-network (Tailscale) PENDING.

**Last updated:** 2026-06-25
