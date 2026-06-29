# Security Policy

**Document ID:** ACP-SECURITY-001  
**Layer:** Legal & trust (fork surface) · complements [L2 `CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) for contributors  
**Pre-flip:** Security contact **`security@dataxmind.com`** approved @ 2026-06-27 — provision mailbox at DNS provider before PB-12; see [`PB11_LEGAL_AUDIT.md`](docs/governance/PB11_LEGAL_AUDIT.md) §Contact setup.

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

**Alternate:** Email **security@dataxmind.com** (maintainer-approved security contact).

Include:

- Description and impact
- Steps to reproduce
- Affected version / commit
- Suggested fix (optional)

---

## Known Attack Surfaces (0.x Beta)

See [`docs/governance/THREAT_MODEL.md`](docs/governance/THREAT_MODEL.md) for full threat model.

### 1. Policy Engine DoS

`POST /policy/evaluate` is the critical path for all agent decisions.
A flood of requests can cause fail-closed behavior for **all** agents.
**Mitigation status:** Rate limiting **not** yet implemented in 0.x.
**Workaround:** Deploy behind a reverse proxy (nginx/caddy) with rate limiting.
**Planned:** v0.2.x

### 2. Redis Cache Poisoning

Policy cache in Redis is not cryptographically verified in 0.x.
If Redis is compromised, stale or false policies may be served briefly before TTL expiry.
**Mitigation:** Deploy Redis with AUTH + TLS. Do not expose the Redis port externally.
`ACP_REDIS_URL` must use `rediss://` (TLS) in production.

### 3. Agent Identity Spoofing

0.x uses token-based identity. No hardware attestation or mutual TLS between agents and ACP.
An agent with a stolen token can impersonate another agent.
**Mitigation:** Rotate tokens on any suspected compromise. See [`docs/RUNBOOK.md`](docs/RUNBOOK.md) §identity.

### 4. Dependency Supply Chain

ACP is Python. Dependencies are pinned in project metadata but not SLSA-attested in 0.x.
Run `pip-audit` locally before deploying from source; confirm CI dependency checks on `master` before release.

---

## Out of Scope — 0.x Beta

- Prompt injection filtering (ACP evaluates actions, not LLM output content)
- Multi-tenant data isolation (single-tenant 0.x; multi-tenancy planned v1.x)
- Hardware security modules for key storage
- FedRAMP / IL2 compliance

---

## Verifying Security Reports

**security@dataxmind.com** — no PGP key published in 0.x beta.
For sensitive disclosures, request a Signal contact via initial email.
GitHub Security Advisories will be enabled upon public flip (PB-12).

---

## Backup Security Contact

If **security@dataxmind.com** bounces, open a GitHub Security Advisory directly
after the repo goes public (PB-12). **Do not** post vulnerabilities in public Issues.

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
