# Create Milestone C+ issues per MILESTONE_C_PLUS_ADR.md ADR-7 (human approved)
$repo = "DataXMind/AI-Control-Plane"
$labels = "milestone-c-plus,spec-gap"

$issues = @(
    @{
        Title = "C+-1: TelemetryStore.replay() API"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-1 (APPROVED)

## Scope
Add ``replay(from_ts, to_ts, event_type, project_id)`` to TelemetryStore ABC.
Verify chain before return; fail-closed on tamper.

## Acceptance
- [ ] InMemory + FileTelemetryStore implementations
- [ ] tests/test_telemetry.py + test_telemetry_persistence.py
- [ ] mypy strict

## Do not implement until issue explicitly picked for sprint.
"@
    },
    @{
        Title = "C+-2: Sense Z-score + otel-collector.yaml.example"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-2 (APPROVED)

## Scope
Phase 2a: Z-score on replay window in SenseAdapter.
Add config/otel-collector.yaml.example; document run_otel_collector.sh.
Optional sklearn IsolationForest when [apex] extra installed.

## Acceptance
- [ ] Works without [apex] extra
- [ ] otel-collector.yaml.example in repo
- [ ] Depends on C+-1 replay API

## Do not implement until issue explicitly picked for sprint.
"@
    },
    @{
        Title = "C+-3: Analyze Argos 4-stage protocol"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-3 (APPROVED)

## Scope
Detect -> Repair -> Review -> Mutate pipeline.
New Pydantic models in core/models.py: AnalyzeFinding, RepairProposal, ReviewDecision, MutateResult.
Review integrates ApprovalGate; no auto YAML writes.

## Acceptance
- [ ] 4-stage unit tests with mocked ApprovalGate
- [ ] Fail-closed per stage

## Do not implement until issue explicitly picked for sprint.
"@
    },
    @{
        Title = "C+-4: Predict Darts token burn + fallback"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-4 (APPROVED)

## Scope
Forecast token burn rate from telemetry replay.
darts>=0.27 in [apex] optional extra; rolling mean fallback without darts.

## Acceptance
- [ ] Fallback tested without darts
- [ ] Optional darts path with synthetic series

## Do not implement until issue explicitly picked for sprint.
"@
    },
    @{
        Title = "C+-5: Act proposal-only policy path (Option C)"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-5 Option C (APPROVED)

## Scope
ActAdapter returns proposals only; no direct PolicyEngine execution.
Document TS/MCP execution path in ARCHITECTURE.

## Acceptance
- [ ] act never side-effects production state
- [ ] proposals include policy_eval_required flag
- [ ] tests for high-risk vs low-risk paths

## Do not implement until issue explicitly picked for sprint.
"@
    },
    @{
        Title = "C+-6: cyanheads MCP E2E CI (respx mock)"
        Body = @"
## ADR
MILESTONE_C_PLUS_ADR.md ADR-6a (APPROVED)

## Scope
Extend test_mcp_http_transport.py: respx mock ACP_MCP_GIT_URL cyanheads JSON-RPC.
Full path tools/call -> policy allow -> HttpGitForwarder -> result.

## Acceptance
- [ ] Runs in CI Full suite
- [ ] No live git in Python
- [ ] Invariant #3 preserved

## Do not implement until issue explicitly picked for sprint.
"@
    }
)

foreach ($item in $issues) {
    gh issue create --repo $repo --title $item.Title --body $item.Body --label $labels
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Created: $($item.Title)"
}
