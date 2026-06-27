# VPS runtime verify v1.3.3 — PASS

**Captured:** 2026-06-27 (UTC)  
**Host:** `ubuntu-vps` (`~/AI-Control-Plane`)  
**Master:** `863b611` (PR #115 catalog v1.3.3 gates_remaining)  
**Prior on host:** v1.3.2 @ `68ae48e`  
**Stack:** Docker + `acp-staging.service` (Profile A fixture, rules=8)

## Procedure

```bash
cd ~/AI-Control-Plane
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
```

## Operator output

```text
OK: governance/status runtime verify 1.3.3 13 patterns
```

## Assertions (v1.3.3)

| ID | Check | Expected | Result |
|----|-------|----------|--------|
| V133-1 | `governance_version` | `1.3.3` | ✅ |
| V133-2 | `len(known_gaps)` | `7` | ✅ (implicit via script) |
| V133-3 | OPEN gaps | `G-05` only | ✅ (implicit via script) |
| V133-4 | `len(lessons_patterns)` | `≥ 13` | ✅ **13** |
| V133-5 | `len(gates_remaining)` | `≥ 5` | ✅ (implicit via script) |
| V133-6 | `len(gates_closed)` | `≥ 3` | ✅ (implicit via script) |
| V133-7 | `practice_evidence.studies_completed` | `8` | ✅ (implicit via script) |
| V133-8 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ (implicit via script) |

## Delta from v1.3.2 pass (@ `68ae48e`)

| Field | v1.3.2 | v1.3.3 |
|-------|--------|--------|
| `governance_version` | `1.3.2` | `1.3.3` |
| `public_beta.gates_remaining` | (implicit) | **7** explicit gate IDs |
| `public_beta.gates_closed` | — | **4** (PB-11, RUNBOOK, 3-stream, Discussions) |

**Verdict:** **PASS** — catalog v1.3.3 runtime-visible on VPS staging.
