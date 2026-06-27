# Open Source Readiness

This document defines when **AI Control Plane** may transition from a private repository to a
public, fork-friendly artifact. The repo stays **private until production stability is proven**.

## Visibility phases

| Phase | Visibility | Goal |
|-------|------------|------|
| **0 — Private** | DataXMind only | Build governance core (current) |
| **1 — Trusted preview** | Private + invited forks | Validate TS PolicyClient + MCP integration |
| **2 — Public beta** | GitHub public, `0.x` semver | Community experimentation with disclaimer |
| **3 — GA artifact** | PyPI / container registry | `pip install ai-control-plane`, stable API |

Do **not** make the repository public before Phase 2 gates pass.

## Milestone mapping

| GitHub Milestone | Scope | Close when |
|------------------|-------|------------|
| **Milestone A** | PoC scaffold: core, api, mcp, cli assign/status | **CLOSED** 2026-06-23 (master #38) |
| **Milestone B** | Production hardening: Redis, persistence, CLI live | **CLOSED** 2026-06-24 (PR #51) |
| **Milestone C (boundary)** | SAPAL MVP + file telemetry + `/apex/*` | **CLOSED** 2026-06-24 (PR #63) |
| **Milestone C+ (depth)** | OTel, Argos, Darts, replay, proposal-only act, cyanheads CI | **CLOSED** 2026-06-24 (PR #74) |
| **Public Beta** | Legal, soak, OpenAPI, `0.x` public | Go/No-Go — **in progress** ([`PUBLIC_BETA_SPRINT_PLAN.md`](governance/PUBLIC_BETA_SPRINT_PLAN.md)) |

## Technical gates (before public beta)

| Gate | Criterion | Tracking |
|------|-----------|----------|
| Config-driven runtime | No hardcoded agents/policies/quotas in `api/server.py` | #5–#7 |
| Policy truth | `config/policies.yml` matches runtime behavior (tested) | #7, #11 |
| Fail-closed proven | API down / invalid request → deny (integration tests) | #11 |
| Persistence | Tasks and quota survive API restart | #36 |
| Observability | Structured logging, `/health`, basic metrics | #19, #25 |
| CI mandatory | PR blocked on **Smoke gate** + **Full suite** (when branch protection available) | #25–#27 |
| Security hygiene | Secret scanning, dependency audit | Dependabot + pip-audit |
| Core tests | Each `core/` module has tests | #21–#24 |
| API contract snapshots | `/health`, `/policy/evaluate` schema keys stable | [`CONTRACT_TESTS.md`](CONTRACT_TESTS.md) |

## Operational gates (production)

| Gate | Criterion |
|------|-----------|
| Staging soak | Continuous run ≥ 2 weeks with simulated agent workload |
| Production soak | ≥ 30 days without SEV-1/2 caused by control plane |
| Runbook | Deploy, rollback, config reload, incident response documented |
| SLO (example) | `POST /policy/evaluate` p99 < 500 ms; availability ≥ 99.5% |

## Legal and trust artifacts (required at public beta)

- [x] `LICENSE` (MIT — declared in `pyproject.toml`)
- [x] `SECURITY.md` — vulnerability reporting (48h ack; tiered remediation; GH Security Advisories)
- [x] `CONTRIBUTING.md` — PR rules, invariant list, PACE, branch naming, contract verify
- [x] `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1 (full text)
- [x] No production secrets or internal cluster IDs in shipped `config/` (verify before PB-12)

## Fork-friendly public surface

Document these as **stable extension points** from `1.0.0`:

| Module | Contract |
|--------|----------|
| `core/models.py` | All data types — semver protected |
| `core/policies.py` | `PolicyEngine.evaluate()` — custom engine, not OSS replacement |
| `core/quota.py` | `QuotaStore` Protocol — inject Redis or other backend |
| `api/server.py` | HTTP bridge — OpenAPI published |
| `config/*.yml` | Shipped defaults; override via `ACP_CONFIG_DIR` |
| `mcp/git_server.py` | Facade only — Git logic stays in TypeScript cyanheads |

Keep **internal**: production `ACP_CONFIG_DIR`, real agent credentials, internal runbooks.

Ship **`examples/minimal/`** (fixture config, docker-compose) instead of production YAML. Index: [`examples/README.md`](../examples/README.md).

## Release and versioning

| Version | Meaning |
|---------|---------|
| `0.x.y` | Pre-GA; breaking changes allowed with changelog |
| `1.0.0` | Public GA — HTTP API and config schema frozen |
| `x.y.z-rc.N` | Release candidate for production validation |

- Use [Conventional Commits](https://www.conventionalcommits.org/) on `master`.
- Maintain `CHANGELOG.md` ([Keep a Changelog](https://keepachangelog.com/)).
- Tag releases: `v0.1.0`, `v0.1.0-rc.1`, etc.

## API stability policy (from 1.0.0)

| Surface | Stability |
|---------|-----------|
| `POST /policy/evaluate` request/response | Stable |
| `PolicyDecision` fields | Frozen; additive only |
| `config/policies.yml` | `version: N` with migration guide on bump |
| `ACP_*` environment variables | Backward compatible |

Deprecation: warn for 2 minor versions, remove on next major.

## Development workflow (apply now, while private)

```
master (protected)
  ↑ pull request only
feat|fix|chore/<issue>-<short-desc>
```

- Link every PR to a GitHub issue (`bug`, `spec-gap`, `debt`, `quality`, `milestone-b`).
- No direct pushes to `master` (branch protection when available).
- No force-push to `master`.

### Branch protection (GitHub)

| Repo state | Branch protection |
|------------|-------------------|
| **Private (free tier)** | Branch protection / Rulesets **not enforced** (API 403; UI warns Team upgrade required) — PR + CI green by team convention |
| **Private (GitHub Team/Pro)** | Run `scripts/setup_github_milestones_and_protection.sh --protection-only`; required checks: `Smoke gate`, `Full suite` |
| **Public beta** | Enable in Settings → Branches → `master`: require PR (1 approval), block force push, require conversation resolution; require status checks **Smoke gate** + **Full suite** |

**Codecov (optional):** set repository variable `CODECOV_ENABLED=true` and secret `CODECOV_TOKEN` to upload `coverage.xml` from the Full suite job.

Until protection is enabled, treat **PR-only merges to `master`** as a team rule.

## Go / No-Go — flip repository to public

Only when **all** items are checked:

- [ ] Milestone B closed
- [ ] Production stable ≥ 30 days (SLO met, no open SEV-1)
- [x] README + ARCHITECTURE + `examples/minimal/` — fork path documented; PB-7 **CLEAN** evidence pending
- [ ] LICENSE, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md present
- [ ] OpenAPI spec published; integration tests green on CI
- [ ] Default `config/` contains no production secrets
- [ ] Maintainer and security contact listed in README
- [ ] Public beta disclaimer: `0.x` API may change until `1.0.0`

## Artifact publishing (Phase 3 — GA)

| Artifact | Channel | When |
|----------|---------|------|
| Python package | PyPI `ai-control-plane` | `1.0.0` |
| CLI | `agentctl` via pip entry point | With PyPI |
| Container | `ghcr.io/dataxmind/ai-control-plane` | After Docker Compose stable |
| API docs | OpenAPI + static site | Public beta |

Before `1.0.0`: prefer `pip install git+https://...` or private registry only.

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) — invariants and module inventory
- [PUBLIC_BETA_SPRINT_PLAN.md](governance/PUBLIC_BETA_SPRINT_PLAN.md) — PB-1..12
- [PUBLIC_BETA_GO_NO_GO.md](governance/PUBLIC_BETA_GO_NO_GO.md) — flip checklist
- [CONTRIBUTING.md](../CONTRIBUTING.md) · [SECURITY.md](../SECURITY.md)
- [.cursorrules](../.cursorrules) — code generation rules
- [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues) — labeled backlog
