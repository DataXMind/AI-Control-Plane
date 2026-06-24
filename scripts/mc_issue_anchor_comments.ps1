# DEVELOPMENT_PROTOCOL Evolve - anchor comments before PR #63 merge
$repo = "DataXMind/AI-Control-Plane"
$common = @"
**Anchor (pre-merge)** - DEVELOPMENT_PROTOCOL section 5.5 Evolve

| Field | Value |
|-------|-------|
| Status | **DONE** (pending merge) |
| PR | #63 |
| Branch | milestone-c/mc-1-11 |
| Gates | pytest 156, smoke 8/8 (SMK-01..06c), ruff, mypy --strict |
"@

$issues = @(
    @{ Num = 52; Text = "MC-9: FileTelemetryStore + create_telemetry_store() under ACP_DATA_DIR/telemetry/events.json. Tests: test_telemetry_persistence.py." },
    @{ Num = 53; Text = "MC-1: SenseAdapter.collect() aggregates telemetry by event_type/project." },
    @{ Num = 54; Text = "MC-2: AnalyzeAdapter.analyze() anomaly threshold from config." },
    @{ Num = 55; Text = "MC-3: PredictAdapter.predict() risk_level + recommended_action." },
    @{ Num = 56; Text = "MC-4: ActAdapter.execute() fail-closed skip on high risk." },
    @{ Num = 57; Text = "MC-5: LearnAdapter ingest/propose/apply (human approval required)." },
    @{ Num = 58; Text = "MC-6: SapalLoop.run() + run_sapal_pipeline() orchestrates SAPAL." },
    @{ Num = 59; Text = "MC-7: GET /apex/status, POST /apex/trigger; agentctl apex status|trigger (HTTP-only)." },
    @{ Num = 60; Text = "MC-8: MCP HTTP E2E test_mcp_http_e2e_policy_and_tool_call (tools/list + tools/call)." },
    @{ Num = 61; Text = "MC-10: scripts/run_otel_collector.sh stub launcher." },
    @{ Num = 62; Text = "MC-11: test_apex_loop.py rewritten + test_cli_apex.py + API apex tests." }
)

foreach ($item in $issues) {
    $body = "$common`n`n$($item.Text)"
    gh issue comment $item.Num --repo $repo --body $body
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Commented #$($item.Num)"
}
