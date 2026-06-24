# Public Beta — Sprint Plan

**Document ID:** ACP-GOV-PUBLIC-BETA-001  
**Status:** **IN PROGRESS** — prep started 2026-06-24  
**Baseline:** `master` @ `de931b5` (post audit prompts 1–3 + C+)  
**Parent:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md)  
**Go/No-Go tracker:** [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)

---

## Scope boundary

Public Beta = **Phase 2 visibility** (public GitHub, `0.x` semver). **Not** PyPI GA (Phase 3).

**Out of scope for this sprint:** Re-open Milestone A/B/C/C+ hygiene; change SAPAL architecture.

**Parallel track:** 6-layer Cursor governance — [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) (docs-only; does not block soak).

---

## Sprint tracks (parallel)

| Track | Owner | Goal |
|-------|-------|------|
| **PB-L** Legal & trust | Maintainer | LICENSE, SECURITY, CONTRIBUTING, CoC |
| **PB-T** Technical | Cursor + CI | OpenAPI export, `examples/`, README ≤15 min fork |
| **PB-O** Operational | Ops | Staging soak 2w → production soak 30d |
| **PB-P** Platform | Org admin | Branch protection API or public-repo flip |

---

## Work items

| ID | Item | Source gate | Status | Evidence / target |
|----|------|-------------|--------|-------------------|
| PB-1 | `LICENSE` (MIT per `pyproject.toml`) | Legal | ✅ | repo root `LICENSE` |
| PB-2 | `SECURITY.md` vulnerability reporting | Legal | ✅ | repo root |
| PB-3 | `CONTRIBUTING.md` (invariants + PR rules) | Legal | ✅ | repo root |
| PB-4 | `CODE_OF_CONDUCT.md` | Legal | ✅ | repo root |
| PB-5 | `examples/minimal` docker-compose + README | Technical | ✅ | `examples/minimal/` |
| PB-6 | OpenAPI spec export + doc | Technical | ✅ | `scripts/export_openapi.py`, `docs/openapi/` |
| PB-7 | README fork path ≤15 min verified | Go/No-Go | 🔄 | Docker path documented; operator verify |
| PB-8 | `CHANGELOG.md` + `v0.1.0-rc.1` tag plan | Release | 🔄 | `CHANGELOG.md` added; tag at PB-12 |
| PB-9 | Staging soak ≥2 weeks | Operational | 🔄 **IN PROGRESS** | Started 2026-06-22 — [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) |
| PB-10 | Production soak ≥30 days SLO | Operational | ❌ | [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) |
| PB-11 | Branch protection API enforced | Platform | ❌ | [#79](https://github.com/DataXMind/AI-Control-Plane/issues/79) — 403 free tier |
| PB-12 | Flip repo public + disclaimer | Go/No-Go | ❌ | [#80](https://github.com/DataXMind/AI-Control-Plane/issues/80) |

---

## Technical gates (from OPEN_SOURCE_READINESS) — current

| Gate | Status @ `de931b5` |
|------|-------------------|
| Config-driven runtime | ✅ |
| Policy truth (shipped parity CI) | ✅ |
| Fail-closed proven | ✅ integration + smoke |
| Persistence (`ACP_DATA_DIR`, Redis) | ✅ |
| Observability (`/health`, structlog) | ✅ |
| CI Smoke + Full suite | ✅ |
| Security hygiene (Dependabot, pip-audit in CI) | ✅ |
| Core module tests | ✅ 165 pytest |

---

## Execution order (recommended)

```text
PB-1..4 (legal) ──┬──> PB-5..6 (fork surface) ──> PB-7..8 ──> PB-9 ──> PB-10
PB-11 (platform) ─┘                                      └──> PB-12 (human go/no-go)
```

**Human approve required before:** PB-12 (public flip), ~~PB-9 soak start~~ ✅ 2026-06-22, upgrading org plan for PB-11 (deferred to PB-12).

---

## Verification gate (each PR)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -q
pytest -m smoke -q
```

---

**Last updated:** 2026-06-22 (PB-9 soak started)
