# VPS runtime verify v1.3.2 — PASS

**Captured:** 2026-06-26 (UTC)  
**Host:** `ubuntu-vps` (`root@~/AI-Control-Plane`)  
**Master:** `68ae48e` (PR #109 P-13 + PR #108 RUNBOOK)  
**Prior on host:** `dbf3079` → fast-forward `68ae48e`  
**Stack:** Docker + `acp-staging.service` (Profile A fixture, rules=8)

## Procedure

```bash
export ACP_REPO=/root/AI-Control-Plane
cd "$ACP_REPO"
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
```

## Operator output

```text
From github.com:DataXMind/AI-Control-Plane
 * branch            master     -> FETCH_HEAD
   dbf3079..68ae48e  master     -> origin/master
Updating dbf3079..68ae48e
Fast-forward
 ... (27 files, incl. P-13, kill-switch JSON, docs/RUNBOOK.md, pb-7 scaffold)

OK: governance/status runtime verify 1.3.2 13 patterns
```

## Assertions (v1.3.2)

| ID | Check | Expected | Result |
|----|-------|----------|--------|
| V132-1 | `governance_version` | `1.3.2` | ✅ |
| V132-2 | `len(known_gaps)` | `7` | ✅ (implicit via script) |
| V132-3 | OPEN gaps | `G-05` only | ✅ (implicit via script) |
| V132-4 | `len(lessons_patterns)` | `≥ 13` (incl. P-13 kill switch) | ✅ **13** |
| V132-5 | `practice_evidence.studies_completed` | `8` | ✅ (implicit via script) |
| V132-6 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ (implicit via script) |

## Delta from v1.3.0 pass (@ `a43524a`)

| Field | v1.3.0 | v1.3.2 |
|-------|--------|--------|
| `governance_version` | `1.3.0` | `1.3.2` |
| `lessons_patterns` | 12 | **13** (P-13 kill switch HTTP contract) |
| Merged since | — | #107 PB-7 scaffold, #109 P-13, #108 `docs/RUNBOOK.md` |

**Verdict:** **PASS** — catalog v1.3.2 + P-13 runtime-visible on VPS staging.
