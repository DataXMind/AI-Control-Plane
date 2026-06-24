# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `0.x` (public beta) | Yes — security fixes on latest `0.x` |
| `< 0.1.0` pre-release | Best effort |

## Reporting a vulnerability

**Do not** open public GitHub issues for security vulnerabilities.

Email: **security@dataxmind.com** (replace with your team inbox before public flip).

Include:

- Description and impact
- Steps to reproduce
- Affected version / commit
- Suggested fix (optional)

We aim to acknowledge within **72 hours** and provide a remediation timeline within **14 days** for confirmed issues.

## Scope

In scope:

- `ai-control_plane` Python package (`src/ai_control_plane/`)
- HTTP API (`api/server.py`) — policy, identity, quota paths
- MCP Git facade (`mcp/git_server.py`)
- Shipped `config/*.yml` when used as templates (secret leakage in defaults)

Out of scope:

- Third-party MCP servers (e.g. cyanheads git-mcp-server)
- Customer `ACP_CONFIG_DIR` deployments with production secrets

## Safe defaults

- Never commit production API keys or cluster IDs to `config/`.
- Use `ACP_CONFIG_DIR` for environment-specific YAML.
- `POST /policy/evaluate` must remain fail-closed (no default-allow on errors).

See [ARCHITECTURE.md](ARCHITECTURE.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
