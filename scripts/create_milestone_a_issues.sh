#!/usr/bin/env bash
# Create Milestone A backlog issues on DataXMind/AI-Control-Plane
set -euo pipefail

REPO="DataXMind/AI-Control-Plane"

create_label() {
  gh label create "$1" --color "$2" --description "$3" --repo "$REPO" 2>/dev/null || true
}

create_label "bug" "d73a4a" "Broken code or imminent runtime failure"
create_label "spec-gap" "fbca04" "Milestone A spec not yet implemented"
create_label "debt" "7057ff" "Scaffold inconsistency or duplicate code"
create_label "quality" "0e8a16" "Tests, CI, and quality gates"
create_label "milestone-b" "1d76db" "Explicitly deferred to Milestone B/C"

issue() {
  local title="$1"
  shift
  local labels="$1"
  shift
  gh issue create --repo "$REPO" --title "$title" --label "$labels" --body "$1"
}

echo "Creating BUG issues..."
issue "B1: Fix registry.py broken imports (Guardrail, RbacConfig, RegisteredAction)" "bug" "$(cat <<'EOF'
## Problem
`core/registry.py` imports `Guardrail`, `RbacConfig`, and `RegisteredAction` from `core/models.py`, but those types do not exist.

## Impact
```python
from ai_control_plane.core import registry  # ImportError
```

## Acceptance criteria
- [ ] All imports in `registry.py` resolve against `core/models.py` (add types or trim registry)
- [ ] `from ai_control_plane.core import registry` succeeds
- [ ] Covered by `tests/test_registry.py` (see quality backlog)

**Milestone:** A closure | **Type:** bug
EOF
)"

issue "B2: Align TelemetryEvent model with telemetry.py hash-chain fields" "bug" "$(cat <<'EOF'
## Problem
`core/telemetry.py` uses `event_id`, `event_hash`, and `previous_hash` on `TelemetryEvent`, but `core/models.py` does not define these fields.

## Impact
`InMemoryTelemetryStore.append()` will fail at runtime when sealing events.

## Acceptance criteria
- [ ] `TelemetryEvent` in `models.py` includes chain fields (or telemetry module uses only defined fields)
- [ ] `seal_event()` / `verify_event_chain()` work end-to-end
- [ ] Covered by `tests/test_telemetry.py`

**Milestone:** A closure | **Type:** bug
EOF
)"

issue "B3: Implement ControlPlaneError hierarchy in core/exceptions.py" "bug" "$(cat <<'EOF'
## Problem
`core/exceptions.py` is empty. `.cursorrules` requires domain errors inheriting from `ControlPlaneError`.

## Acceptance criteria
- [ ] `ControlPlaneError` base class exists
- [ ] At least policy/config/quota subclasses defined
- [ ] API and MCP use domain errors where appropriate (not raw exceptions for domain failures)

**Milestone:** A closure | **Type:** bug
EOF
)"

issue "B4: apex/pipeline.py must raise NotImplementedError (milestone guard)" "bug" "$(cat <<'EOF'
## Problem
`.cursorrules` milestone guard: Apex files in Milestone A should only be stubs with `NotImplementedError`. `pipeline.py` currently has only a docstring.

## Acceptance criteria
- [ ] `apex/pipeline.py` exposes stub entrypoints that raise `NotImplementedError`
- [ ] No SAPAL business logic in `apex/` until Milestone C

**Milestone:** A closure | **Type:** bug
EOF
)"

echo "Creating SPEC-GAP issues..."
issue "S1: Wire agents.yml into api/server.py (remove hardcoded agent registry)" "spec-gap" "$(cat <<'EOF'
## Problem
`api/server.py` uses `_DEFAULT_AGENT_REGISTRY` hardcoded dict instead of `config/loader.py` + `agents.yml`.

## Acceptance criteria
- [ ] Server loads agents from `ACP_CONFIG_DIR` / shipped `config/agents.yml`
- [ ] `POST /policy/evaluate` and `POST /identity/verify` use loaded registry
- [ ] Changing test `agents.yml` affects API behavior without code changes

**Milestone:** A closure | **Type:** spec-gap | Invariant #8
EOF
)"

issue "S2: Wire project token limits from config into TokenBudget" "spec-gap" "$(cat <<'EOF'
## Problem
`project_limits` in `api/server.py` is hardcoded. `config/policies.yml` defines `quotas.by_project`.

## Acceptance criteria
- [ ] Project limits loaded from config at app startup
- [ ] `GET /quota/{project_id}` reflects configured limits
- [ ] Unknown projects fail-closed per existing behavior

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S3: Load policies.yml into PolicyEngine at API startup" "spec-gap" "$(cat <<'EOF'
## Problem
`create_app()` initializes `PolicyEngine(rules=[])`. Shipped `config/policies.yml` is never loaded.

## Acceptance criteria
- [ ] `loader.load_policies()` returns `list[PolicyRule]`
- [ ] `PolicyEngine` receives rules on startup
- [ ] `POST /policy/evaluate` reflects YAML RBAC + deny/approval rules (minimum PoC set)
- [ ] Test fixtures remain compatible

**Note:** Complex guardrails / kill_switch enforcement → Milestone B.

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S3a: Tool name adapter between config (git.read) and PolicyEngine (git_read)" "spec-gap" "$(cat <<'EOF'
## Problem
`config/policies.yml` uses dot notation (`git.read`, `k8s.apply`). `PolicyEngine` and tests use underscores (`git_read`, `k8s_apply_prod`).

## Acceptance criteria
- [ ] Single documented canonical convention
- [ ] Adapter layer at config load or policy eval boundary
- [ ] `ARCHITECTURE.md` documents mapping for TypeScript PolicyClient / MCP

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S4: Load model_profiles from agents.yml into ModelProfile objects" "spec-gap" "$(cat <<'EOF'
## Problem
`agents.yml` defines `model_profiles` but `config/loader.py` does not load them into `ModelProfile` models.

## Acceptance criteria
- [ ] `load_model_profiles()` (or equivalent) in loader
- [ ] Returns `dict[str, ModelProfile]` validated via Pydantic
- [ ] Used or ready for quota enforcement in Milestone B

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S5: Unify TaskStatus between core.models and api.schemas" "spec-gap" "$(cat <<'EOF'
## Problem
Duplicate `TaskStatus` types: `core/models.py` lacks `progress`; `api/schemas.py` adds `progress`. Violates invariant #2 (single source of truth).

## Acceptance criteria
- [ ] One canonical `TaskStatus` in `core/models.py`
- [ ] API schemas import or extend from core (no duplicate contract)
- [ ] CLI and server use same type

**Milestone:** A closure | **Type:** spec-gap | Invariant #2
EOF
)"

issue "S6: Add API integration tests for fail-closed behavior" "spec-gap,quality" "$(cat <<'EOF'
## Problem
`api/server.py` has 7 endpoints with fail-closed handlers but no integration tests.

## Acceptance criteria
- [ ] `tests/test_api_server.py` using FastAPI `TestClient`
- [ ] Invalid `/policy/evaluate` → 503 + `allowed=false`
- [ ] Timeout/unhandled paths tested where feasible
- [ ] Real `PolicyEngine` with test YAML (no mock engine)

**Milestone:** A closure | **Type:** spec-gap + quality
EOF
)"

issue "S7: Add MCP git_server facade tests" "spec-gap,quality" "$(cat <<'EOF'
## Problem
`mcp/git_server.py` has policy gate + forward logic but no tests.

## Acceptance criteria
- [ ] Policy deny → tool not forwarded, `McpError` raised
- [ ] Policy allow → `StubGitForwarder` invoked
- [ ] `requires_approval` path returns pending error

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S8: README local dev runbook (install, env vars, uvicorn, agentctl)" "spec-gap" "$(cat <<'EOF'
## Problem
`README.md` is minimal; PoC is not operable from docs alone.

## Acceptance criteria
- [ ] Install steps (`pip install -e .`)
- [ ] Document `ACP_CONFIG_DIR`, `ACP_API_URL`
- [ ] Start API + example `agentctl assign` / `status`
- [ ] Note in-memory task limitations (reload clears state)

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

issue "S9: Update ARCHITECTURE.md to match current API and conventions" "spec-gap" "$(cat <<'EOF'
## Problem
`ARCHITECTURE.md` is missing `POST /tasks`, `GET /health`, and tool naming conventions.

## Acceptance criteria
- [ ] Endpoint list matches `api/server.py`
- [ ] Tool naming convention documented (after S3a)
- [ ] Milestone A Definition of Done checklist linked or embedded

**Milestone:** A closure | **Type:** spec-gap
EOF
)"

echo "Creating DEBT issues..."
issue "D1: Remove or consolidate dead api/ stubs (app.py, routes/, deps.py)" "debt" "$(cat <<'EOF'
## Problem
`api/app.py`, `api/routes/*`, `api/deps.py` are empty stubs. All logic lives in `api/server.py`, causing confusion.

## Acceptance criteria
- [ ] Either delete unused stubs OR wire `server.py` through `create_app()` factory in `app.py`
- [ ] No duplicate undocumented API entrypoints
- [ ] Imports updated; tests pass

**Milestone:** A closure | **Type:** debt
EOF
)"

issue "D2: Implement or remove config/schemas.py stub" "debt" "$(cat <<'EOF'
## Problem
`config/schemas.py` is a one-line placeholder while `loader.py` + `models.py` handle validation.

## Acceptance criteria
- [ ] Implement YAML mirror schemas OR remove file and update imports
- [ ] No dead modules in `config/`

**Milestone:** A closure | **Type:** debt
EOF
)"

issue "D3: Document and standardize tool naming across config, engine, MCP" "debt" "$(cat <<'EOF'
## Problem
Three naming styles coexist: `git.read`, `git_read`, MCP `git_commit`.

## Acceptance criteria
- [ ] Canonical naming table in `ARCHITECTURE.md`
- [ ] Aligns with S3a adapter implementation
- [ ] No silent mismatches in policy evaluation

**Milestone:** A closure | **Type:** debt
EOF
)"

issue "D4: Align cli/_http.py with async I/O convention" "debt" "$(cat <<'EOF'
## Problem
`.cursorrules` requires async/await for I/O. `cli/_http.py` uses sync `httpx.Client`.

## Options
- Migrate to `httpx.AsyncClient` + `asyncio.run` in Typer commands
- OR document explicit CLI sync exception in `ARCHITECTURE.md`

## Acceptance criteria
- [ ] Decision documented
- [ ] Implementation matches decision

**Milestone:** A closure | **Type:** debt
EOF
)"

issue "D5: Replace stdlib logging with structlog in api/server.py" "debt" "$(cat <<'EOF'
## Problem
`.cursorrules` requires structlog. `api/server.py` uses `logging.getLogger`.

## Acceptance criteria
- [ ] structlog configured for HTTP middleware and error paths
- [ ] Uvicorn log output remains readable (no garbled stdout)

**Milestone:** A closure | **Type:** debt
EOF
)"

issue "D6: Document in-memory task store limitations" "debt" "$(cat <<'EOF'
## Problem
Tasks stored in `task_status_by_project` dict are lost on API reload/restart. Not obvious to operators.

## Acceptance criteria
- [ ] Documented in README and/or ARCHITECTURE.md
- [ ] Persistence explicitly scoped to Milestone B

**Milestone:** A closure | **Type:** debt
EOF
)"

echo "Creating QUALITY issues..."
issue "Q1: Add tests/test_models.py" "quality" "$(cat <<'EOF'
## Requirement
`.cursorrules`: each `core/` file must have a corresponding test file.

## Acceptance criteria
- [ ] Tests for frozen models, validation, key serializers
- [ ] Uses fixtures from `conftest.py` where applicable

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q2: Add tests/test_quota.py" "quality" "$(cat <<'EOF'
## Acceptance criteria
- [ ] `InMemoryQuotaStore` thread safety basics
- [ ] `QuotaTracker.consume` / `TokenBudget.deduct` limit enforcement
- [ ] `RateLimiter.check` behavior
- [ ] Inject mock `QuotaStore` per `.cursorrules`

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q3: Add tests/test_telemetry.py" "quality" "$(cat <<'EOF'
## Acceptance criteria
- [ ] `compute_event_hash` / `verify_event_chain`
- [ ] `InMemoryTelemetryStore.append` and `verify_chain`
- [ ] Depends on B2 (model alignment)

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q4: Add tests/test_registry.py" "quality" "$(cat <<'EOF'
## Acceptance criteria
- [ ] `ActionRegistry` register/validate/list
- [ ] Depends on B1 (import fix)

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q6: Add GitHub Actions CI (ruff, pytest, mypy)" "quality" "$(cat <<'EOF'
## Problem
No `.github/workflows/` — regressions not caught automatically.

## Acceptance criteria
- [ ] Workflow on push/PR to `master`/`main`
- [ ] `ruff check`, `pytest`, `mypy` (mypy allowed to fail initially with follow-up Q8)
- [ ] Uses `pip install -e .[dev]`

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q7: Add .pre-commit-config.yaml" "quality" "$(cat <<'EOF'
## Problem
`pre-commit` listed in dev dependencies but no config file.

## Acceptance criteria
- [ ] Hooks for ruff (and optionally mypy)
- [ ] Document `pre-commit install` in README

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q8: Ensure ruff and mypy pass on src/" "quality" "$(cat <<'EOF'
## Acceptance criteria
- [ ] `ruff check src/` clean
- [ ] `mypy` clean on `ai_control_plane` package (strict mode)
- [ ] CI enforces both (Q6)

**Milestone:** A closure | **Type:** quality
EOF
)"

issue "Q9: Extend conftest.py with FastAPI app fixture" "quality" "$(cat <<'EOF'
## Acceptance criteria
- [ ] `app` / `client` pytest fixtures using test config dir
- [ ] Shared by `test_api_server.py` and integration tests
- [ ] `ACP_CONFIG_DIR` set via existing autouse fixture

**Milestone:** A closure | **Type:** quality
EOF
)"

echo "Creating MILESTONE-B issues (deferred)..."
issue "MB1: Implement RedisQuotaStore backend" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone B — not Milestone A.

## Acceptance criteria
- [ ] `RedisQuotaStore` implements `QuotaStore` protocol
- [ ] Connection via env var / constructor injection (no hardcoded URL)
- [ ] Swappable in `api/server.py` AppState

**Deferred:** Milestone B
EOF
)"

issue "MB2: Implement cli/approve wired to POST /policy/approve" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone B — `cli/approve.py` is currently a stub.

## Acceptance criteria
- [ ] Resolve approval requests via HTTP API
- [ ] Rich/JSON output for operators

**Deferred:** Milestone B
EOF
)"

issue "MB3: Implement cli/quota wired to GET /quota/{project_id}" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone B — `cli/quota.py` is currently a stub.

**Deferred:** Milestone B
EOF
)"

issue "MB4: Implement cli/logs for telemetry audit stream" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone B — `cli/logs.py` is currently a stub.

**Deferred:** Milestone B
EOF
)"

issue "MB5: Redis-backed ActionRegistry" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone B per ARCHITECTURE.md: registry Redis backend.

**Deferred:** Milestone B
EOF
)"

issue "MB6: MCP HTTP transport for git_server" "milestone-b" "$(cat <<'EOF'
## Scope
`GitMcpServer.start(transport="http")` raises NotImplementedError — Milestone B.

**Deferred:** Milestone B
EOF
)"

issue "MB7: Full guardrails and kill_switch enforcement from policies.yml" "milestone-b" "$(cat <<'EOF'
## Scope
`config/policies.yml` guardrails section + kill_switch — enforce at policy eval time.

**Deferred:** Milestone B (minimum deny rules in S3 for Milestone A)
EOF
)"

issue "MB8: Task persistence across API restarts" "milestone-b" "$(cat <<'EOF'
## Scope
Replace in-memory `task_status_by_project` with durable store.

**Deferred:** Milestone B
EOF
)"

issue "MB9: apex/ SAPAL pipeline (Sense, Analyze, Predict, Act, Learn)" "milestone-b" "$(cat <<'EOF'
## Scope
Milestone C per ARCHITECTURE.md — OSS tools called FROM apex/, not before.

**Deferred:** Milestone C
EOF
)"

issue "Milestone A — Definition of Done (tracking issue)" "spec-gap,quality" "$(cat <<'EOF'
## Goal
Close Milestone A PoC scaffold with config-driven governance and test/CI gates.

## Checklist
- [ ] B1–B4: All bugs fixed
- [ ] S1–S9: Config wired, types unified, tests/docs updated
- [ ] D1–D6: Scaffold debt addressed
- [ ] Q1–Q4, Q6–Q9, S6–S7: Quality gates green on CI
- [ ] MB1–MB9: Explicitly **not** in scope (Milestone B/C)

## Reference
See audit backlog: bug / spec-gap / debt / quality / milestone-b labels.

**Close this issue when all child issues for Milestone A are resolved.**
EOF
)"

echo "Done. Issue list:"
gh issue list --repo "$REPO" --limit 50
