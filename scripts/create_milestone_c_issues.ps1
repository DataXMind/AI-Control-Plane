# Create Milestone C issues MC-9 .. MC-10 (execution order in titles)
$repo = "DataXMind/AI-Control-Plane"
$parent = "#37 MB9"

$issues = @(
  @{ n="MC-9"; title="MC-9: Durable TelemetryStore (file via ACP_DATA_DIR)"; sprint="C1" },
  @{ n="MC-1"; title="MC-1: SenseAdapter.collect live"; sprint="C1" },
  @{ n="MC-2"; title="MC-2: AnalyzeAdapter.analyze live"; sprint="C1" },
  @{ n="MC-3"; title="MC-3: PredictAdapter.predict live"; sprint="C2" },
  @{ n="MC-4"; title="MC-4: ActAdapter.execute policy-gated"; sprint="C2" },
  @{ n="MC-5"; title="MC-5: LearnAdapter propose/apply (no auto YAML)"; sprint="C2" },
  @{ n="MC-6"; title="MC-6: SapalLoop + run_sapal_pipeline orchestrator"; sprint="C2" },
  @{ n="MC-7"; title="MC-7: agentctl apex status/trigger via HTTP"; sprint="C3" },
  @{ n="MC-8"; title="MC-8: MCP HTTP E2E test (cyanheads path)"; sprint="C3" },
  @{ n="MC-10"; title="MC-10: run_otel_collector.sh + OTLP doc"; sprint="C3" },
  @{ n="MC-11"; title="MC-11: apex/ tests and coverage"; sprint="C1-C3" }
)

foreach ($item in $issues) {
  $body = @"
## $($item.n): $($item.title)

**Parent:** $parent
**Sprint:** $($item.sprint)
**Invariant:** #5 — SAPAL logic only in ``apex/``

### Acceptance criteria
- [ ] Implementation on master branch
- [ ] Tests updated or added
- [ ] ruff + mypy + pytest green

### References
- ``ARCHITECTURE.md`` Milestone C
- ``docs/governance/MILESTONE_C_SPRINT_PLAN.md``
"@
  gh issue create --repo $repo --title $item.title --label "milestone-c,milestone-b" --body $body
}
