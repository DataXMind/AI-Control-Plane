#!/usr/bin/env bash
# Create GitHub milestones, assign issues, and configure branch protection.
set -euo pipefail

REPO="DataXMind/AI-Control-Plane"

milestone_a=$(gh api "repos/${REPO}/milestones" \
  -f title="Milestone A" \
  -f description="PoC scaffold closure: core, api, mcp, cli assign/status, tests, CI (#1-#28, #38)" \
  -f state="open" \
  --jq '.number')

milestone_b=$(gh api "repos/${REPO}/milestones" \
  -f title="Milestone B" \
  -f description="Production hardening: Redis, persistence, CLI approve/quota/logs, guardrails (#29-#37)" \
  -f state="open" \
  --jq '.number')

milestone_public=$(gh api "repos/${REPO}/milestones" \
  -f title="Public Beta" \
  -f description="Open source gate: legal docs, examples, prod soak, GitHub public 0.x" \
  -f state="open" \
  --jq '.number')

echo "Created milestones: A=#${milestone_a} B=#${milestone_b} Public Beta=#${milestone_public}"

assign_milestone() {
  local issue="$1"
  local ms="$2"
  gh api -X PATCH "repos/${REPO}/issues/${issue}" -f milestone="${ms}" >/dev/null
}

for i in $(seq 1 28); do
  assign_milestone "$i" "$milestone_a"
done
assign_milestone 38 "$milestone_a"

for i in $(seq 29 37); do
  assign_milestone "$i" "$milestone_b"
done

echo "Assigned issues to milestones."

# Branch protection on master (requires GitHub Pro/Team for private repos, or public repo).
if gh api -X PUT "repos/${REPO}/branches/master/protection" \
  --input - <<'JSON' 2>/dev/null; then
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true
}
JSON
  echo "Branch protection enabled on master."
  gh api "repos/${REPO}/branches/master/protection" \
    --jq '{required_pull_request_reviews, allow_force_pushes, allow_deletions}'
else
  echo "WARN: Branch protection not applied (HTTP 403 on private free-tier repos)."
  echo "Enable manually when repo is public or org has GitHub Team:"
  echo "  Settings → Branches → Add rule for master"
  echo "  - Require pull request (1 approval)"
  echo "  - Require conversation resolution"
  echo "  - Block force pushes"
  echo "  - Add required status checks after CI (#25) merges"
fi
