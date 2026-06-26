# Governance catalog — Claude sync prompt audit

**Document ID:** ACP-GOV-CATALOG-CLAUDE-SYNC-AUDIT-001  
**Audit date:** 2026-06-26  
**Baseline:** `master` catalog v1.3.1  
**Prompt:** Claude 3-stream sync task (pre-Studies closure artifact)

---

## Verdict

| Question | Answer |
|----------|--------|
| Prompt still valid as-is? | **No** — stale gap statuses and field names |
| Core intent achieved? | **Yes** — superseded by PR #99–#104 + v1.3 verify |
| Action taken | v1.3.1 additive aliases + `practice_evidence` metadata |

---

## Step-by-step matrix

| Claude step | Prompt (stale) | Current @ v1.3.1 | Status |
|-------------|----------------|------------------|--------|
| **1** doc_links | Add 5 keys | ✅ + aliases `behavioral_constitution`, `cursor_risk_policy`, `practice_evidence_index`; path fix `docs/governance/CURSOR_RISK_POLICY.md` | **DONE** |
| **2** known_gaps | All OPEN / SKIPPED text | ✅ G-01..04,06,07 **CLOSED**; G-05 **OPEN**; field `title`+`status` not `gap` | **DONE** (better) |
| **3** practice_evidence | 7 studies, `open_gaps: 7` | ✅ 8 studies, `open_gaps_count: 1`, hosts/topologies/note | **DONE** |
| **4** layers nested lessons | Embed in L0/L3/L5 dict | ✅ `lessons_patterns[]` P-01..P-12 + layer one-liners point to it | **DONE** (better) |
| **5** GOVERNANCE_UX_RUNTIME | Schema rows + stale note | ✅ Updated; G-01 CLOSED note | **DONE** |

---

## Drift warnings (do NOT apply prompt literally)

| Prompt claim | Reality @ 2026-06-26 |
|--------------|----------------------|
| G-01 kill switch SKIPPED | **CLOSED** G2-1 |
| G-02 5e not done | **CLOSED** G2-2 / 05e-r |
| G-03 7-0n soft | **CLOSED** G2-4 |
| G-06/G-07 Profile B open | **CLOSED** Study 08 |
| `open_gaps: 7` | **1** (G-05 PB-9 only) |
| `studies_executed: 7` | **8** (incl. Study 08) |
| `docs/CURSOR_RISK_POLICY.md` | Wrong — use `docs/governance/CURSOR_RISK_POLICY.md` |

---

## 3-stream convergence (runtime)

```text
Stream 1 Practice  → known_gaps[] + practice_evidence
Stream 2 Karpathy  → doc_links + lessons_patterns[] (P-01..P-12)
Stream 3 Runtime   → case_studies[] CS-01..06 + verify_gate
```

**Verify:** `bash scripts/verify_governance_status_runtime.sh` → `1.3.1` · `12 patterns` · VPS PASS @ `a43524a`.

---

**SSOT:** `src/ai_control_plane/core/governance_catalog.py`
