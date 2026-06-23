#!/usr/bin/env bash
# Idempotent GitHub milestones + optional branch protection for AI-Control-Plane.
#
# Usage:
#   bash scripts/setup_github_milestones_and_protection.sh              # milestones + assign + protection probe
#   bash scripts/setup_github_milestones_and_protection.sh --milestones-only
#   bash scripts/setup_github_milestones_and_protection.sh --protection-only
#   ASSIGN_ISSUES=false bash scripts/setup_github_milestones_and_protection.sh
#
# Branch protection requires GitHub Pro/Team (private) or a public repository.
# Private org free tier: Rulesets UI is visible but NOT enforced until GitHub Team.
set -euo pipefail

REPO="${REPO:-DataXMind/AI-Control-Plane}"
ASSIGN_ISSUES="${ASSIGN_ISSUES:-true}"
RUN_MILESTONES=true
RUN_PROTECTION=true

log() { printf '%s\n' "$*" >&2; }
warn() { printf 'WARN: %s\n' "$*" >&2; }

usage() {
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --milestones-only)
      RUN_PROTECTION=false
      ;;
    --protection-only)
      RUN_MILESTONES=false
      ASSIGN_ISSUES=false
      ;;
    -h | --help)
      usage 0
      ;;
    *)
      warn "Unknown option: $1"
      usage 1
      ;;
  esac
  shift
done

get_or_create_milestone() {
  local title="$1"
  local description="$2"
  local number

  number=$(
    gh api "repos/${REPO}/milestones" --paginate \
      --jq ".[] | select(.title == \"${title}\") | .number" | head -1
  )

  if [ -n "$number" ]; then
    log "Milestone exists: ${title} (#${number})"
    printf '%s' "$number"
    return 0
  fi

  number=$(
    gh api "repos/${REPO}/milestones" \
      -f title="$title" \
      -f description="$description" \
      -f state="open" \
      --jq '.number'
  )
  log "Created milestone: ${title} (#${number})"
  printf '%s' "$number"
}

setup_milestones() {
  log "=== Milestones (${REPO}) ==="

  milestone_a=$(
    get_or_create_milestone \
      "Milestone A" \
      "PoC scaffold closure: core, api, mcp, cli assign/status, tests, CI (#1-#28, #38)"
  )
  milestone_b=$(
    get_or_create_milestone \
      "Milestone B" \
      "Production hardening: Redis, persistence, CLI approve/quota/logs, guardrails (#29-#37)"
  )
  milestone_public=$(
    get_or_create_milestone \
      "Public Beta" \
      "Open source gate: legal docs, examples, prod soak, GitHub public 0.x"
  )

  log "Milestones ready: A=#${milestone_a} B=#${milestone_b} Public Beta=#${milestone_public}"

  if [ "$ASSIGN_ISSUES" != "true" ]; then
    log "Skipping issue assignment (ASSIGN_ISSUES=false)."
    return 0
  fi

  assign_milestone() {
    local issue="$1"
    local ms="$2"
    if ! gh api "repos/${REPO}/issues/${issue}" >/dev/null 2>&1; then
      warn "Issue #${issue} not found — skip"
      return 0
    fi
    if gh api -X PATCH "repos/${REPO}/issues/${issue}" -f milestone="${ms}" >/dev/null 2>&1; then
      return 0
    fi
    warn "Could not assign milestone to issue #${issue}"
  }

  log "Assigning issues to milestones..."
  for i in $(seq 1 28); do
    assign_milestone "$i" "$milestone_a"
  done
  assign_milestone 38 "$milestone_a"
  for i in $(seq 29 37); do
    assign_milestone "$i" "$milestone_b"
  done
  log "Issue assignment complete."
}

branch_protection_available() {
  local err_file err_body

  err_file=$(mktemp)

  if gh api "repos/${REPO}/branches/master/protection" >/dev/null 2>"$err_file"; then
    rm -f "$err_file"
    return 0
  fi

  err_body=$(cat "$err_file")
  rm -f "$err_file"

  if echo "$err_body" | grep -qE '403|Upgrade to GitHub Pro'; then
    return 1
  fi
  if echo "$err_body" | grep -q '404'; then
    return 0
  fi

  warn "Unexpected branch protection probe: ${err_body}"
  return 1
}

apply_branch_protection() {
  log "=== Branch protection (${REPO}:master) ==="

  if ! branch_protection_available; then
    warn "Branch protection API unavailable on this repository plan."
    warn "Private DataXMind org (free): Rulesets UI shows enforcement requires GitHub Team upgrade."
    warn "Options:"
    warn "  1) Upgrade org to GitHub Team / use GitHub Pro"
    warn "  2) Make repository public (public beta gate)"
    warn "  3) Until then: team discipline — PR-only merges + require CI green manually"
    warn "Required checks when enabled: Smoke gate, Full suite"
    return 0
  fi

  # Use legacy contexts[] — checks[] with app_id:null causes HTTP 422.
  local err_file
  err_file=$(mktemp)
  if gh api -X PUT "repos/${REPO}/branches/master/protection" \
    --input - 2>"$err_file" <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Smoke gate", "Full suite"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON
  then
    log "Branch protection enabled on master."
    gh api "repos/${REPO}/branches/master/protection" \
      --jq '{required_status_checks, required_pull_request_reviews, allow_force_pushes}'
  else
    warn "Branch protection PUT failed:"
    cat "$err_file" >&2
    return 1
  fi
  rm -f "$err_file"
}

if [ "$RUN_MILESTONES" = true ]; then
  setup_milestones
fi

if [ "$RUN_PROTECTION" = true ]; then
  apply_branch_protection
fi

log "Done."
