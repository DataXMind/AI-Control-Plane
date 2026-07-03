#!/usr/bin/env bash
# Install ACP Antigravity zsh hook (ACP repo). Idempotent.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACP_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
HOOK_LINE="source \"$SCRIPT_DIR/antigravity_shell_hook.zsh\"  # ACP Antigravity guard"
MARKER="# ACP_ANTIGRAVITY_HOOK"

install_into() {
  local profile="$1"
  [[ -f "$profile" ]] || touch "$profile"
  if grep -q "$MARKER" "$profile" 2>/dev/null; then
    echo "Already installed in $profile"
    return 0
  fi
  {
    echo ""
    echo "$MARKER"
    echo "export AI_CONTROL_PLANE_ROOT=\"$ACP_ROOT\""
    echo "$HOOK_LINE"
  } >> "$profile"
  echo "Installed into $profile"
}

case "${SHELL:-}" in
  */zsh) install_into "$HOME/.zshrc" ;;
  */bash) install_into "$HOME/.bashrc" ;;
  *) install_into "$HOME/.profile" ;;
esac

cat <<'EOF'
Set env before Antigravity terminal:
  export ACP_API_URL=http://<acp-host>:8000
  export ACP_AGENT_ID=agent1   # MSI; agent2 on Mac
  export ACP_ROLE=infra        # or backend
Open new terminal — kubectl/git/cargo auto-gated.
EOF
