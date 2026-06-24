# Milestone C — Sprint Plan

**Status:** **CLOSED** (code) — 2026-06-24  
**Master:** post PR #63 (`6dfffdf`) — branch `milestone-c/mc-1-11`

## Issue map (GitHub)

| MC ID | GitHub | Title | Close |
|-------|--------|-------|-------|
| MC-9 | #52 | Durable TelemetryStore | PR #63 |
| MC-1 | #53 | SenseAdapter.collect | hygiene close |
| MC-2 | #54 | AnalyzeAdapter.analyze | hygiene close |
| MC-3 | #55 | PredictAdapter.predict | hygiene close |
| MC-4 | #56 | ActAdapter.execute | hygiene close |
| MC-5 | #57 | LearnAdapter propose/apply | hygiene close |
| MC-6 | #58 | SapalLoop + pipeline | hygiene close |
| MC-7 | #59 | agentctl apex status/trigger | hygiene close |
| MC-8 | #60 | MCP HTTP E2E | hygiene close |
| MC-10 | #61 | run_otel_collector.sh | hygiene close |
| MC-11 | #62 | apex/ tests & coverage | hygiene close |
| MB9 umbrella | #37 | apex/ SAPAL pipeline | hygiene close |

## Delivered (PR #63)

- `FileTelemetryStore` + `create_telemetry_store()` when `ACP_DATA_DIR` set
- SAPAL adapters + `SapalLoop` + `run_sapal_pipeline()` (MVP heuristic loop)
- `GET /apex/status`, `POST /apex/trigger`; `agentctl apex status|trigger`
- `scripts/run_otel_collector.sh` stub; MCP HTTP E2E test (stub forwarder)
- **165 pytest**, smoke 8/8, ruff, mypy strict

## C+ depth (PR #74)

Architect ADR items delivered: `replay()`, Z-score sense, Argos analyze, Darts/rolling predict, proposal-only act, cyanheads MCP E2E CI — issues #67–#72 closed.

## Beyond Milestone C+ (open)

| Item | Target |
|------|--------|
| Public beta legal + examples | `OPEN_SOURCE_READINESS.md` |
| Branch protection API enforced | GitHub Team / public repo |

**Last updated:** 2026-06-24 (Milestone C + C+ complete; #9/#39 closed PR #75)
