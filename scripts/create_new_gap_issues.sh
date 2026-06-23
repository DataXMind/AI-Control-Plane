#!/usr/bin/env bash
# Create NEW-1..NEW-5 GitHub issues (post-audit gap items).
set -euo pipefail

REPO="DataXMind/AI-Control-Plane"
MILESTONE_A=1

issue() {
  local title="$1"
  shift
  local labels="$1"
  shift
  local url
  url=$(gh issue create --repo "$REPO" --title "$title" --label "$labels" --body "$1")
  echo "${url##*/}"
}

assign_milestone() {
  gh api -X PATCH "repos/${REPO}/issues/${1}" -f milestone="${MILESTONE_A}" >/dev/null
}

echo "Creating NEW-1..NEW-5..."

n1=$(issue "NEW-1: P0-4b — Extend GET /health with config wire proof" "spec-gap" "## Problem
\`GET /health\` currently returns only \`{\"status\": \"ok\"}\`. After P0-4 wires \`agents.yml\` and \`policies.yml\`, operators and CI have no quick way to verify config was loaded at startup.

## Acceptance criteria
- [ ] \`GET /health\` returns JSON including:
  - \`config_loaded: true|false\`
  - \`policy_rules_count: int\`
  - \`agents_loaded: list[str]\`
  - \`projects_loaded: list[str]\`
- [ ] When \`ACP_CONFIG_DIR\` is missing or invalid → \`config_loaded: false\` (fail-closed signal)
- [ ] Documented in README runbook (#13)

## Dependencies
- Blocks on: P0-2 (policies wire), P0-4 (agents/projects wire)
- Related: #5, #6, #7

## Milestone A | Type: spec-gap | Priority: P0-4b")

n2=$(issue "NEW-2: Unify test fixtures policies.yml with production schema after P0-2" "spec-gap,quality" "## Problem
Two incompatible policy schemas exist today:
- \`config/policies.yml\` — \`rbac:\` / \`abac:\` sections (dot notation e.g. \`git.read\`)
- \`tests/fixtures/config/policies.yml\` — \`rules:\` list with \`PolicyRule\` format (\`rule_type\`, \`allowed_actions\`)

After P0-2 wires production YAML into \`PolicyEngine\`, unit tests may pass on fixtures but diverge from shipped config.

## Acceptance criteria
- [ ] Single adapter: \`config/policies.yml\` → \`list[PolicyRule]\` (see NEW-5)
- [ ] Test fixtures either use production-format YAML or assert adapter output matches fixture rules
- [ ] \`tests/test_policies.py\` runs against adapter-loaded rules from production schema (or shared canonical fixture)
- [ ] No silent drift between \`ACP_CONFIG_DIR\` test path and \`config/\` defaults

## Dependencies
- Blocks on: NEW-5, P0-2
- Related: #7, #8, #11

## Milestone A | Type: spec-gap + quality")

n3=$(issue "NEW-3: apex/ — 6 import-clean SAPAL stub files" "spec-gap" "## Problem
\`.cursorrules\` milestone guard requires apex/ to be stubs only until Milestone C. Issue #4 only covers \`pipeline.py\`. Audit checklist expects 6 import-clean stub modules for the SAPAL loop.

## Acceptance criteria
- [ ] Stub modules exist and import without side effects:
  - \`sense.py\`, \`analyze.py\`, \`predict.py\`, \`act.py\`, \`learn.py\`, \`loop.py\` (or equivalent names documented in ARCHITECTURE.md)
- [ ] Each public entrypoint raises \`NotImplementedError\` with clear message
- [ ] \`apex/__init__.py\` exports stable names for import tests
- [ ] No OSS agent framework imports
- [ ] \`pipeline.py\` aligned with same stub pattern (#4)

## Dependencies
- Related: #4, MB9 (#37)

## Milestone A | Type: spec-gap | Not Milestone C logic")

n4=$(issue "NEW-4: tests/test_apex_loop.py — import-clean regression for apex stubs" "quality" "## Problem
No test guards apex/ stub contract. Regressions could add real SAPAL logic before Milestone C.

## Acceptance criteria
- [ ] \`tests/test_apex_loop.py\` imports all apex stub modules
- [ ] Asserts calling stub entrypoints raises \`NotImplementedError\`
- [ ] Uses fixtures from \`conftest.py\` where applicable
- [ ] CI runs this test (after #25)

## Dependencies
- Blocks on: NEW-3
- Related: #4

## Milestone A | Type: quality")

n5=$(issue "NEW-5: P0-2c — policies.yml to PolicyRule adapter (not naive rbac loop)" "spec-gap" "## Problem
\`config/policies.yml\` uses \`rbac.roles.*.allowed_actions\` / \`abac.rules[]\` with dot notation. \`PolicyEngine\` expects \`PolicyRule\` objects with \`conditions.rule_type\`, \`allowed_actions\`, \`denied_patterns\`, etc. (see \`tests/fixtures/config/policies.yml\` and \`core/policies.py\`).

A naive loader that only maps role names will not drive \`_evaluate_rbac\` / \`_evaluate_abac\` correctly.

## Acceptance criteria
- [ ] \`config/loader.py\`: \`load_policies() -> list[PolicyRule]\` with documented mapping
- [ ] RBAC: per-role rules with \`conditions.rule_type=rbac\`, \`role\`, \`allowed_actions\`, \`denied_patterns\`
- [ ] ABAC: deny/allow rules with \`conditions.rule_type=abac\` and engine-supported keys (\`environment\`, \`action\`, \`data_category\`, \`requires_approval\`)
- [ ] Tool names normalized to \`snake_case\` at load time (#8)
- [ ] Unit tests for adapter (can live in \`tests/test_loader.py\` or \`tests/test_policies.py\`)
- [ ] Document mapping in \`ARCHITECTURE.md\` (#14)

## Dependencies
- Blocks: P0-2, NEW-2
- Related: #7, #8, #17

## Milestone A | Type: spec-gap | Priority: P0-2c (critical path)")

for num in "$n1" "$n2" "$n3" "$n4" "$n5"; do
  assign_milestone "$num"
done

echo "Created and assigned to Milestone A:"
gh issue list --repo "$REPO" --search "NEW-" --limit 10 --json number,title,milestone \
  --jq '.[] | "#\(.number) [\(.milestone.title // "none")] \(.title)"'
