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
- **156 pytest**, smoke 8/8, ruff, mypy strict

## Beyond Milestone C (open debt)

| Item | Issue / gap | Target |
|------|-------------|--------|
| `load_model_profiles()` wired to AppState | #9, GAP-S4-1 | B+ debt |
| Extended `/health` proof | #39 | B+ debt |
| cyanheads MCP E2E in CI | MC-8 follow-up | **C+-6** [#72](https://github.com/DataXMind/AI-Control-Plane/issues/72) |
| OTLP collector config + doc | MC-10 follow-up | **C+-2** [#68](https://github.com/DataXMind/AI-Control-Plane/issues/68) |
| Architect SAPAL depth (replay, Argos, Darts, act proposals) | `MILESTONE_C_PLUS_ADR.md` | C+-1..C+-5 [#67–#71](https://github.com/DataXMind/AI-Control-Plane/issues/67) |
| Public beta legal + examples | `OPEN_SOURCE_READINESS.md` | Pre-public |
| Branch protection enforced | GAP-BP-1 | GitHub Team / public repo |

**Last updated:** 2026-06-24 (Milestone C code complete; issue hygiene)
