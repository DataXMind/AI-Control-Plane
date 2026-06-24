# Milestone C — Sprint Plan

**Status:** IN PROGRESS  
**Branch:** `milestone-c/mc-1-11`  
**Base:** `master` @ PR #51 (`fc296d4`)

## Issue map (GitHub)

| MC ID | GitHub | Title |
|-------|--------|-------|
| MC-9 | #52 | Durable TelemetryStore |
| MC-1 | #53 | SenseAdapter.collect |
| MC-2 | #54 | AnalyzeAdapter.analyze |
| MC-3 | #55 | PredictAdapter.predict |
| MC-4 | #56 | ActAdapter.execute |
| MC-5 | #57 | LearnAdapter propose/apply |
| MC-6 | #58 | SapalLoop + pipeline |
| MC-7 | #59 | agentctl apex status/trigger |
| MC-8 | #60 | MCP HTTP E2E |
| MC-10 | #61 | run_otel_collector.sh |
| MC-11 | #62 | apex/ tests & coverage |

## Priority matrix (execution order)

1. **Foundation:** MC-9 (telemetry persistence)
2. **SAPAL core:** MC-1 → MC-2 → MC-3 → MC-4 → MC-5 → MC-6
3. **Integration:** MC-7 (API + CLI), MC-8 (MCP E2E), MC-10 (otel script)
4. **Quality gate:** MC-11 (tests)

## Sprint breakdown

| Sprint | Items | Deliverable |
|--------|-------|-------------|
| C1 | MC-9, MC-1, MC-2, MC-11 partial | Telemetry + Sense/Analyze |
| C2 | MC-3..MC-6, MC-11 | Full SAPAL loop |
| C3 | MC-7, MC-8, MC-10, MC-11 final | CLI/API + ops |

## Acceptance

- `FileTelemetryStore` when `ACP_DATA_DIR` set; `create_telemetry_store()` factory
- SAPAL adapters implemented (no `NotImplementedError`)
- `GET /apex/status`, `POST /apex/trigger`; `agentctl apex status|trigger`
- pytest + ruff + mypy strict green
- Close #52–#62 on merge

## Beyond Milestone C

- B+ debt: #9, #3, #39, extended quota YAML
- Public Beta (`OPEN_SOURCE_READINESS.md`)
- Ops: soak tests, branch protection API (#37)
