# Post-merge runtime verify — MSI WSL

**Captured:** 2026-06-27 (UTC)  
**Host:** MSI WSL (`/mnt/d/Projects/ai-control-plane`)  
**Label:** **WARM** — operator re-verify after examples quick-start / PR #118 docs  
**Branch @ run:** `docs/pb12-operator-checklist-pin` @ `9b83989` (PR [#118](https://github.com/DataXMind/AI-Control-Plane/pull/118) open)  
**Stack:** Docker `minimal-acp-api-1` (assumed running; verify-only curl)

## Procedure

```bash
export ACP_API_URL=http://localhost:8000
bash scripts/verify_governance_status_runtime.sh
```

## Operator output

```text
OK: governance/status runtime verify 1.3.3 13 patterns
```

## Analysis

| Check | Result | Notes |
|-------|--------|-------|
| `governance_version` | **1.3.3** | Catalog SSOT unchanged |
| `lessons_patterns` | **13** | Incl. P-13 kill switch |
| Runtime script | **PASS** | L4/L5 governance UX wire OK |
| Examples path docs | N/A | Docs-only PR — no `src/` change; runtime confirms API still v1.3.3 |

**Context:** Operator ran verify after following post-merge examples quick-start checklist. Confirms Docker API on port 8000 still serves catalog v1.3.3 — no regression from docs wave (#116–#118).

**Prior local PASS:** [`local-runtime-v133-pass.md`](local-runtime-v133-pass.md) @ `863b611` (full rebuild). This entry is a **lighter re-verify** (script only).

**Does not close:** PB-7 CLEAN fork · PB-9 calendar · security@ · PB-12 gates.

## Verdict

**PASS** — governance runtime verify 1.3.3 · 13 patterns @ MSI WSL post-merge check.
