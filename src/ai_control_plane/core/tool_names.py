"""Tool naming constants and normalization — single source of truth."""

from __future__ import annotations

# MCP tool name → PolicyEngine action name
# MCP catalog uses snake_case (git_status); policy actions use snake_case (git_read)
# These are SEPARATE namespaces — do not conflate
MCP_TOOL_TO_POLICY_ACTION: dict[str, str] = {
    "git_clone": "git_read",
    "git_branch": "git_read",
    "git_status": "git_read",
    "git_commit": "git_commit",
    "git_push": "git_push",
    "git_pr_create": "create_pr",
}


def normalize_tool_name(name: str) -> str:
    """Normalize dot notation to snake_case. Idempotent for snake_case input."""
    return name.replace(".", "_")


def resolve_policy_tool_name(name: str) -> str:
    """Resolve MCP tool name OR dot-notation tool name to canonical policy action."""
    if name in MCP_TOOL_TO_POLICY_ACTION:
        return MCP_TOOL_TO_POLICY_ACTION[name]
    return normalize_tool_name(name)


__all__ = ["MCP_TOOL_TO_POLICY_ACTION", "normalize_tool_name", "resolve_policy_tool_name"]
