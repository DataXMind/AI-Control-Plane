# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**0.x note:** API may change without deprecation warning until `1.0.0-GA`.

## [Unreleased]

### Added

- Docs: `END_USER_VALUE.md` four-door map; QUICKSTART k6 §2.5; competitive feature table; SAPAL packaging review target @ v0.3.0 ([#183](https://github.com/DataXMind/AI-Control-Plane/pull/183), drift-close follow-up)
- Design issue: `agentctl policy diff` dry-run ([#184](https://github.com/DataXMind/AI-Control-Plane/issues/184)) — implementation post-PB-12

### Changed

- Anchor drift reconcile: `ANCHOR_CURRENT`, `SESSION_ANCHOR_TEMPLATE` → pytest **221**; living SHA `44a5fef`

### Notes

- **SAPAL / apex:** experimental through 0.x; packaging decision (separate repo vs module vs archive) targeted for **v0.3.0** review — does not affect Public Beta pitch.

- Milestone C+ backlog: cyanheads MCP E2E in CI, OTel collector config, SAPAL ML depth in `apex/learn.py`

## [0.1.0-rc.1] — 2026-06-28

**Git tag:** [`v0.1.0-rc.1`](https://github.com/DataXMind/AI-Control-Plane/releases/tag/v0.1.0-rc.1) @ `c58b4cc` (pushed 2026-06-28, pre–Day-14 calendar).

Release candidate for Public Beta **`v0.1.0-beta.1`**. Completes Milestones A, B, C (code), C+ (governance depth). Public repository flip still requires PB-9 Day 14 review (~2026-07-06) and PB-12 human go/no-go.

### Added — Milestone A (PoC scaffold)

- `core/` — PolicyEngine, models, registry, quota, telemetry, identity, exceptions
- `api/server.py` — 13 HTTP endpoints (policy, tasks, health, governance, apex, quota, identity, telemetry)
- `mcp/git_server.py` — facade + server_factory + server_utils
- `cli/` — agentctl assign, status, logs, approve, quota, apex
- `apex/` — SAPAL loop (sense, analyze, predict, act, learn) — MVP heuristic
- `tests/` — 177 pytest, smoke 8/8 (SMK-01..06 incl. 06b, 06c), shipped_config parity
- `.github/workflows/ci.yml` — smoke → test + examples-minimal-smoke parallel

### Added — Milestone B (production hardening)

- `RedisQuotaStore` + `ACP_REDIS_URL` optional (#29)
- `cli/approve`, `cli/quota`, `cli/logs` live (#30–32)
- `mcp/server_factory.py` + MCP HTTP transport (#34)
- `FileTaskStore` + `ACP_DATA_DIR` persistence (#36)
- `JWTValidator` HS256 stub + JWKS RS256 via `ACP_JWKS_URL` (#35)
- ABAC full — `role_not_in`, `approval_status`, `read_only` (#45 CLOSED)
- Guardrails + kill_switch loader — KillSwitch model, `load_guardrails()` (#35)
- CLI tests — CliRunner + respx mock (Invariant #4 validated)
- Redis ActionRegistry + quotas by_agent/by_model_profile (GAP-Q-1 CLOSED)
- SMK-06, SMK-06b, SMK-06c — identity 401 contract (Study 05g-r)

### Added — Milestone C (APEX SAPAL MVP)

- `apex/` business logic — heuristic loop (sense telemetry → analyze → predict quotas → act)
- `apex/learn.py` — human-in-loop proposals (`proposals=[]` until ML engine added)
- `FileTelemetryStore` + `ACP_TELEMETRY_DIR` (MC-9)
- `cli/apex.py` + `agentctl gov status` (#59)
- `GET /governance/status` + `governance_catalog.py` v1.3.3

### Added — Governance & operations

- 6-layer Karpathy governance: `AGENTS.md`, `.cursorrules` (L0–L5), `CURSOR_RISK_POLICY.md`
- `docs/governance/LESSONS_LEARNED.md` — P-01..P-13 failure patterns
- `governance_catalog.py` — 3-stream convergence (practice evidence + Karpathy + runtime)
- `examples/minimal/` — docker-compose + Dockerfile + `.env.example` + README
- `docs/RUNBOOK.md` — deploy, rollback, config reload, incident response
- Legal: `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE`
- Static OpenAPI 3.1 — `docs/openapi/openapi.json` via `scripts/export_openapi.py`
- PB-9 staging soak — `scripts/soak_staging.sh`, `restart_soak_loop.sh`, iteration logs
- Practice studies 01–08 — operator confidence evidence (3 hosts, 4 network topologies)

### Fixed

- OpenAPI verify script: `/openapi.json` is URL, not operation in `paths{}` (`1d883ec`)
- `load_policies()` silently skipped `role_not_in` — GAP-ABAC-2 CLOSED
- `PolicyEngine(rules=[])` — policies.yml not wired at startup — P0-2 CLOSED
- Tool naming dual notation — `core/tool_names.py` Option A adapter permanent

### Changed

- `InMemoryTelemetryStore` + `FileTelemetryStore` (additive)
- `TaskStore` — in-memory default → `FileTaskStore` when `ACP_DATA_DIR` set
- `QuotaStore` — in-memory default → `RedisQuotaStore` when `ACP_REDIS_URL` set
- CI: `smoke → test + examples-minimal-smoke` (parallel after smoke gate)

### Known limitations (0.x)

- `apex/learn.py`: proposals always empty — ML rules engine = Milestone C+
- `mcp/git_server.py`: cyanheads E2E not in CI — stub forwarder only (MC-8 debt)
- `scripts/run_otel_collector.sh`: stub only — otel-collector.yaml = Milestone C+ (MC-10)
- Branch protection: GitHub Free tier on private repo — team discipline only (GAP-BP-1)
- Production soak ≥30d (PB-10) deferred to GA — staging soak (PB-9) gates 0.x beta
- 0.x API may change without deprecation; stable from `1.0.0-GA`

### Security

- JWT: HS256 dev stub default; RS256 JWKS via `ACP_JWKS_URL` for production
- Report vulnerabilities: security@dataxmind.com (GitHub Security Advisories preferred when repo is public)
- Do not open public issues for security bugs

[Unreleased]: https://github.com/DataXMind/AI-Control-Plane/compare/v0.1.0-rc.1...HEAD
[0.1.0-rc.1]: https://github.com/DataXMind/AI-Control-Plane/releases/tag/v0.1.0-rc.1
