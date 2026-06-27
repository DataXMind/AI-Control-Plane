# Governance catalog — Claude 3-stream convergence audit

**Document ID:** ACP-GOV-CATALOG-CLAUDE-SYNC-AUDIT-001  
**Audit date:** 2026-06-27  
**Baseline:** `master` catalog **v1.3.3**  
**Prompt:** Claude 3-stream integration diagram (pre–Study 08 / pre–legal delta artifact)

---

## Verdict

| Question | Answer |
|----------|--------|
| Prompt still valid as-is? | **No** — JSON sample and gap counts stale |
| Core intent (3-stream → catalog)? | **Yes — DONE** |
| `GET /governance/status` = full state? | **Yes** (+ live wire fields) |
| Action @ v1.3.3 | `public_beta.gates_remaining` / `gates_closed` + artifact audit sync |

---

## 3-stream architecture (current)

```text
STREAM 1 — Practice Evidence
  Studies 01–08 → practice-evidence/*/artifacts (45 files)
  PRACTICE_STUDIES_AUDIT_01-07.md
       ↓
  G-01..G-07 known_gaps[] (6 CLOSED, G-05 OPEN)
  practice_evidence{} (studies_completed: 8, open_gaps_count: 1)
       ↓
  governance_catalog.py → doc_links.practice_audit

STREAM 2 — 6-layer Karpathy Governance
  CLAUDE.md (L0) + CURSOR_RISK_POLICY.md (L2) + LESSONS_LEARNED.md (L5)
       ↓
  P-01..P-13 lessons_patterns[] (not nested layers{} — better schema)
       ↓
  doc_links.{behavioral_constitution,cursor_risk_policy,lessons_learned,...}

STREAM 3 — Runtime Governance UX
  GET /governance/status (api/server.py)
       ↓
  case_studies CS-01..06, verify_gate, milestones, public_beta
       ↓
  config_loaded + policy_rules_count (live wire)

CONVERGENCE: governance_catalog.py @ v1.3.3
```

---

## Claude JSON sample vs runtime (do NOT apply literally)

| Field | Claude prompt | Current @ v1.3.3 |
|-------|---------------|------------------|
| `milestones.C+` | PLANNED | **CLOSED** |
| `layers` | nested `{name, doc, lessons}` | `dict[str, str]` + `lessons_patterns[]` |
| `practice_evidence.studies` | 7 | **8** (Study 08) |
| `practice_evidence.gaps` | 7 | **`open_gaps_count: 1`** |
| `known_gaps` | all open | **G-05 only OPEN** |
| `lessons` | P-01..P-08 | **P-01..P-13** |
| `public_beta.gates_remaining` | PB-9, PB-11, PB-12 runbook | **Runtime list** — PB-11/RUNBOOK in `gates_closed` |
| `doc_links.cursor_risk_policy` | `docs/CURSOR_RISK_POLICY.md` | **`docs/governance/...`** |
| `verify_gate` | 4 commands | **5** (+ shipped_config) |

---

## Verify

```bash
bash scripts/verify_governance_status_runtime.sh
# OK: governance/status runtime verify 1.3.3 13 patterns

curl -s "$ACP_API_URL/governance/status" | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['governance_version']=='1.3.3'
assert len(d['public_beta']['gates_remaining'])>=5
print('gates_remaining:', d['public_beta']['gates_remaining'])
"
```

**SSOT:** `src/ai_control_plane/core/governance_catalog.py`  
**Drift:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) §10
