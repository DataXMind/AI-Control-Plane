# Local runtime verify v1.3.3 — PASS

**Captured:** 2026-06-22 (UTC)  
**Host:** WSL + Docker (`minimal-acp-api-1`)  
**Master:** `863b611` (PR #115 catalog v1.3.3 gates_remaining)  
**Stack:** `examples/minimal/docker-compose.yml` (Profile A fixture, rules=8)

## Procedure

```bash
cd examples/minimal
docker compose down
docker compose up -d --build
export ACP_API_URL=http://localhost:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_governance_memory.sh
```

## Operator output

```text
OK: governance/status runtime verify 1.3.3 13 patterns
verify_governance_memory: all checks passed (ML5 pack)
```

## Assertions (v1.3.3)

| ID | Check | Expected | Result |
|----|-------|----------|--------|
| V133-1 | `governance_version` | `1.3.3` | ✅ |
| V133-2 | `len(known_gaps)` | `7` | ✅ |
| V133-3 | OPEN gaps | `G-05` only | ✅ |
| V133-4 | `len(lessons_patterns)` | `≥ 13` | ✅ **13** |
| V133-5 | `len(public_beta.gates_remaining)` | `≥ 5` | ✅ **7** |
| V133-6 | `len(public_beta.gates_closed)` | `≥ 3` | ✅ **4** |
| V133-7 | `practice_evidence.studies_completed` | `8` | ✅ |
| V133-8 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ |

## Delta from v1.3.2 pass (@ `68ae48e`)

| Field | v1.3.2 | v1.3.3 |
|-------|--------|--------|
| `governance_version` | `1.3.2` | `1.3.3` |
| `public_beta.gates_remaining` | (implicit) | **7** explicit gate IDs |
| `public_beta.gates_closed` | — | **4** (PB-11, RUNBOOK, 3-stream, Discussions) |

**Note:** Stale image without `--build` served `1.3.2` until rebuild (Study 05e-r lesson).

**Verdict:** **PASS** — catalog v1.3.3 runtime-visible on local Docker staging.
