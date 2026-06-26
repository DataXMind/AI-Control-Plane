#!/usr/bin/env bash
# Verify L5 / ML5 agent memory pack — GP-01 reference implementation.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

errors=0
fail() { echo "FAIL: $1" >&2; errors=$((errors + 1)); }
ok() { echo "OK: $1"; }

# M5-1
if [[ -f AGENTS.md ]]; then ok "AGENTS.md"; else fail "missing AGENTS.md"; fi

# M5-3
ANCHOR="docs/prompts/SESSION_ANCHOR_TEMPLATE.md"
if [[ -f "$ANCHOR" ]]; then ok "$ANCHOR"; else fail "missing $ANCHOR"; fi

# M5-2
RULES_DIR=".cursor/rules"
if [[ -d "$RULES_DIR" ]]; then
  mdc_count=$(find "$RULES_DIR" -maxdepth 1 -name '*.mdc' | wc -l | tr -d ' ')
  if [[ "$mdc_count" -ge 4 ]]; then
    ok ".cursor/rules ($mdc_count .mdc files)"
  else
    fail ".cursor/rules need >= 4 .mdc files (found $mdc_count)"
  fi
  while IFS= read -r -d '' f; do
    if ! head -n 1 "$f" | grep -q '^---$'; then
      fail "$f missing YAML frontmatter"
    fi
    if ! grep -q '^description:' "$f"; then
      fail "$f missing description in frontmatter"
    fi
  done < <(find "$RULES_DIR" -maxdepth 1 -name '*.mdc' -print0)
else
  fail "missing $RULES_DIR"
fi

# M5-7
GP01="docs/governance/gold-patterns/GP-01-agent-session-memory.md"
if [[ -f "$GP01" ]]; then ok "$GP01"; else fail "missing $GP01"; fi

MATURITY="docs/governance/L5_MATURITY_MODEL.md"
if [[ -f "$MATURITY" ]]; then ok "$MATURITY"; else fail "missing $MATURITY"; fi

# M5-5 — catalog doc_links (grep SSOT)
CATALOG="src/ai_control_plane/core/governance_catalog.py"
for key in agents_md session_anchor gold_patterns l5_maturity pre_approval_audit behavioral_constitution cursor_risk_policy practice_evidence_index; do
  if grep -q "\"$key\"" "$CATALOG"; then
    ok "governance_catalog doc_links.$key"
  else
    fail "governance_catalog missing doc_links key: $key"
  fi
done

if [[ "$errors" -gt 0 ]]; then
  echo "verify_governance_memory: $errors error(s)" >&2
  exit 1
fi

echo "verify_governance_memory: all checks passed (ML5 pack)"
