# Hygiene: close stale MC issues after PR #63 merge
$repo = "DataXMind/AI-Control-Plane"
$comment = "**Closed (hygiene)** - delivered in PR #63 (6dfffdf). Manual close; auto-close from merge did not link all issues."

$issues = @(
    @{ Num = 37; Note = "MB9 umbrella - SAPAL pipeline delivered in PR #63 (MC-1..MC-6)." },
    @{ Num = 3;  Note = "ControlPlaneError hierarchy exists in core/exceptions.py; stale issue." },
    @{ Num = 13; Note = "README Quick start + env vars documented; stale issue." },
    @{ Num = 53; Note = "MC-1 SenseAdapter.collect - PR #63." },
    @{ Num = 54; Note = "MC-2 AnalyzeAdapter.analyze - PR #63." },
    @{ Num = 55; Note = "MC-3 PredictAdapter.predict - PR #63." },
    @{ Num = 56; Note = "MC-4 ActAdapter.execute - PR #63." },
    @{ Num = 57; Note = "MC-5 LearnAdapter - PR #63." },
    @{ Num = 58; Note = "MC-6 SapalLoop + pipeline - PR #63." },
    @{ Num = 59; Note = "MC-7 agentctl apex + /apex API - PR #63." },
    @{ Num = 60; Note = "MC-8 MCP HTTP E2E - PR #63." },
    @{ Num = 61; Note = "MC-10 run_otel_collector.sh stub - PR #63." },
    @{ Num = 62; Note = "MC-11 apex tests - PR #63." }
)

foreach ($item in $issues) {
    $body = "$comment $($item.Note)"
    gh issue close $item.Num --repo $repo --comment $body
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Closed #$($item.Num)"
}
