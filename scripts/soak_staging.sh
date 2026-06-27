#!/usr/bin/env bash
# PB-9 staging soak — simulated agent workload against a running ACP API.
#
# Usage:
#   export ACP_API_URL=http://localhost:8000
#   bash scripts/soak_staging.sh              # one iteration
#   bash scripts/soak_staging.sh --loop 3600  # every hour (seconds between runs)
#   bash scripts/soak_staging.sh --log /var/log/acp-soak.log
#   bash scripts/soak_staging.sh --repo-log docs/governance/PB9_SOAK_ITERATION_LOG.md
#
set -euo pipefail

API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"
INTERVAL=0
LOG_FILE=""
REPO_LOG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --loop)
      INTERVAL="${2:-3600}"
      shift 2
      ;;
    --log)
      LOG_FILE="${2:-}"
      shift 2
      ;;
    --repo-log)
      REPO_LOG="${2:-}"
      shift 2
      ;;
    -h | --help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

log() {
  local line
  line="$(date -u +"%Y-%m-%dT%H:%M:%SZ") $*"
  echo "$line"
  if [ -n "$LOG_FILE" ]; then
    echo "$line" >>"$LOG_FILE"
  fi
  if [ -n "$REPO_LOG" ]; then
    echo "$line" >>"$REPO_LOG"
  fi
}

run_iteration() {
  local health policy quota apex
  health=$(curl -sf "${API_URL}/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))")
  policy=$(curl -sf -X POST "${API_URL}/policy/evaluate" \
    -H "Content-Type: application/json" \
    -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('allowed'))")
  quota=$(curl -sf "${API_URL}/quota/rust-gateway" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tokens_remaining',0))")
  apex=$(curl -sf -X POST "${API_URL}/apex/trigger" -H "Content-Type: application/json" -d '{}' >/dev/null && echo ok || echo fail)
  log "soak_iter health=${health} policy_allowed=${policy} tokens_remaining=${quota} apex=${apex}"
}

while true; do
  run_iteration || log "soak_iter ERROR curl failed"
  if [ "$INTERVAL" -le 0 ]; then
    break
  fi
  sleep "$INTERVAL"
done
