# ACP shell guard for Antigravity / zsh IDE terminals (fail-closed).
# Source from ai-control-plane repo:
#   source examples/integrate/shell/antigravity_shell_hook.zsh
#
# Disable: export ACP_SHELL_GUARD=0

[[ -n "$ACP_SHELL_GUARD_LOADED" ]] && return 0
[[ -z "$ACP_API_URL" ]] && return 0
[[ "${ACP_SHELL_GUARD:-1}" == "0" ]] && return 0

export ACP_SHELL_GUARD_LOADED=1
_ACP_HOOK_DIR="${0:A:h}"

_acp_guard_repo() {
  if [[ -n "$AI_CONTROL_PLANE_ROOT" && -f "$AI_CONTROL_PLANE_ROOT/examples/integrate/python/run_tool_guarded.py" ]]; then
    echo "$AI_CONTROL_PLANE_ROOT"
    return 0
  fi
  if [[ -f "./examples/integrate/python/run_tool_guarded.py" ]]; then
    pwd
    return 0
  fi
  if [[ -f "$HOME/AI-Control-Plane/examples/integrate/python/run_tool_guarded.py" ]]; then
    echo "$HOME/AI-Control-Plane"
    return 0
  fi
  if [[ -n "$HYBRID_AI_GATEWAY_ROOT" && -f "$HYBRID_AI_GATEWAY_ROOT/scripts/acp/run_tool_guarded.py" ]]; then
    echo "$HYBRID_AI_GATEWAY_ROOT"
    return 0
  fi
  return 1
}

_acp_run_guarded() {
  local tool="$1"
  shift
  local repo
  if repo="$(_acp_guard_repo)"; then
    if [[ -f "$repo/examples/integrate/python/run_tool_guarded.py" ]]; then
      python3 "$repo/examples/integrate/python/run_tool_guarded.py" --tool "$tool" -- "$@"
      return $?
    fi
    if [[ -f "$repo/scripts/acp/run_tool_guarded.py" ]]; then
      python3 "$repo/scripts/acp/run_tool_guarded.py" --tool "$tool" -- "$@"
      return $?
    fi
  fi
  if [[ -f "$_ACP_HOOK_DIR/acp_evaluate.sh" ]]; then
    "$_ACP_HOOK_DIR/acp_evaluate.sh" "$tool" || return 1
    "$@"
    return $?
  fi
  echo "ACP deny (fail-closed): run_tool_guarded.py not found" >&2
  return 1
}

kubectl() {
  case "$1" in
    apply|delete|patch|replace)
      _acp_run_guarded k8s_apply command kubectl "$@"
      ;;
    *)
      command kubectl "$@"
      ;;
  esac
}

git() {
  case "$1" in
    status|diff|log|show|branch)
      _acp_run_guarded git_read command git "$@"
      ;;
    commit)
      _acp_run_guarded git_commit command git "$@"
      ;;
    push)
      _acp_run_guarded git_push command git "$@"
      ;;
    *)
      command git "$@"
      ;;
  esac
}

cargo() {
  case "$1" in
    build|run|test)
      _acp_run_guarded build.rust command cargo "$@"
      ;;
    *)
      command cargo "$@"
      ;;
  esac
}

echo "ACP shell guard active (agent=${ACP_AGENT_ID:-?} role=${ACP_ROLE:-?})" >&2
