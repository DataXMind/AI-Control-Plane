# Security Policy

**Document ID:** ACP-SECURITY-001  
**Layer:** Legal & trust (fork surface) · complements [L2 `CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) for contributors  
**Pre-flip:** Replace placeholder contact before PB-12 public repository flip.

---

## Supported versions

| Version | Supported |
|---------|-----------|
| `0.x` (public beta) | :white_check_mark: — security fixes on latest `0.x` |
| `< 0.1.0` pre-release | Best effort |

---

## Reporting a vulnerability

**Do not** open public GitHub issues for security vulnerabilities.

**Preferred:** [GitHub Security Advisories](https://github.com/DataXMind/AI-Control-Plane/security/advisories/new)  
(Repository → **Security** → **Advisories** → **New draft advisory**)

**Alternate:** Email **security@dataxmind.com** (replace with a live maintainer inbox before public flip).

Include:

- Description and impact
- Steps to reproduce
- Affected version / commit
- Suggested fix (optional)

---

## Response SLA (official)

**Baseline acknowledgment:** within **48 hours** for all in-scope reports (enterprise ML5-aligned).

Remediation targets by severity after triage:

| Severity | Acknowledge | Triage / assessment | Remediation target | Notes |
|----------|-------------|---------------------|--------------------|-------|
| **CRITICAL** | ≤ 48 h | ≤ 7 calendar days | ≤ 30 calendar days | Fix or documented mitigation + operator runbook |
| **HIGH** | ≤ 48 h | ≤ 14 calendar days | ≤ 60 calendar days | May ship patch release on `0.x` |
| **MEDIUM** | ≤ 48 h | ≤ 30 calendar days | ≤ 90 calendar days or next `0.x` minor | |
| **LOW** | ≤ 48 h | ≤ 30 calendar days | Best effort / scheduled release | Informational hardening |

**Disclosure:** Coordinated disclosure when a fix or mitigation is available. We credit reporters who wish to be named.

**Out of SLA:** Reports lacking reproduction steps, out-of-scope items, or duplicate reports may be closed without a remediation clock.

---

## Scope

**In scope:**

- `ai_control_plane` Python package (`src/ai_control_plane/`)
- HTTP API (`api/server.py`) — policy, identity, quota, governance paths
- Authentication (JWT / JWKS verification paths)
- Config parsing (`config/loader.py`) and shipped `config/*.yml` templates (secret leakage in defaults)
- MCP Git facade (`mcp/git_server.py`)
- Data handling in `core/` modules

**Out of scope:**

- Third-party MCP servers (e.g. cyanheads git-mcp-server) — report upstream
- Customer `ACP_CONFIG_DIR` deployments with operator-managed secrets
- Issues requiring physical access to operator infrastructure

---

## AI-specific considerations (CRITICAL severity)

This project governs AI agents. The following are **CRITICAL** by default:

| Class | Example |
|-------|---------|
| **Policy bypass** | Default-allow on error instead of fail-closed (`allowed=false`) |
| **Identity spoofing** | `AgentIdentity` forgery or JWT verification bypass |
| **Config injection** | Untrusted `ACP_CONFIG_DIR` leading to policy or agent impersonation |
| **Kill switch bypass** | Global deny disabled while `kill_switch.active=true` in config |
| **Quota / approval bypass** | Silent allow when quota exhausted or approval required |

**Operator note:** Kill switch active returns HTTP **200** + `allowed=false` (not HTTP 503). See [LESSONS P-13](docs/governance/LESSONS_LEARNED.md) and [Study 05 §5g](docs/governance/practice-evidence/study-05-advanced-surprises/RUNBOOK.md).

---

## Safe defaults

- Never commit production API keys or cluster IDs to `config/`.
- Use `ACP_CONFIG_DIR` for environment-specific YAML.
- `POST /policy/evaluate` must remain fail-closed (no default-allow on errors).
- `/identity/verify` invalid JWT → HTTP **401** (not 200+deny).

See [ARCHITECTURE.md](ARCHITECTURE.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [DATA_CLASSIFICATION.md](docs/DATA_CLASSIFICATION.md).
