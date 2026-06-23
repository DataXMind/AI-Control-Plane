# Phase 1 Consolidated Record — For Claude Architect Review (Pre–Phase 2)

**Document ID:** ACP-GOV-PHASE1-CONSOLIDATE-001  
**Version:** 1.0  
**Date:** 2026-06-23  
**Audience:** Claude (architecture / audit / Phase 2 planning)  
**Repo:** [DataXMind/AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane) (private)  
**Branch:** `master` @ `83e3ab5`  
**Human workflow:** Claude plan → Human approve → Cursor execute → CI + SMK verify

**Purpose:** Single source packet to **re-evaluate Phase 1**, validate honest gaps, decide **P0-2b**, and **adjust Phase 2 / Milestone B entry** before new execution prompts.

**Supersedes for external review:** Chat-only Phase 1 v1 narrative (optimistic). Authoritative in-repo: this file + [`PHASE1_REPORT_V2.md`](PHASE1_REPORT_V2.md).

---

## 0. Executive verdict (honest)

| Question | Answer |
|----------|--------|
| Was Milestone A (#38) close valid? | **Yes** — scope = **PoC scaffold**, not production |
| Did Phase 1 achieve Architecture V3 scaffold? | **Mostly yes** — core wiring, API, MCP facade, Tab 7, SMK, CI |
| Did initial synthesis report (v1) overclaim? | **Yes** — integration, coverage, structlog, config parity |
| Is project ready for Phase 2 without architect pass? | **No** — need Claude verdict on **P0-2b**, guardrails/ABAC scope, Milestone B ordering |
| Current test gate | **91 pytest**, SMK **5/5**, ruff + mypy strict, shipped parity **4 tests** |
| Current coverage baseline (Codecov) | **~64.5%** lines (`83e3ab5`) — see §8 |

---

## 1. North star & boundaries

### 1.1 Target (unchanged)

- **Governance:** Config-driven policy, fail-closed, custom `PolicyEngine` (no OSS replace)
- **Architecture:** 8 hard invariants — [`ARCHITECTURE.md`](../../ARCHITECTURE.md)
- **Milestone A:** PoC E2E scaffold — core + api + cli (partial) + mcp + apex stubs
- **Milestone B:** Redis, persistence, full YAML sections, CLI live, identity JWT
- **Milestone C:** apex SAPAL live
- **Process:** [`docs/DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) v1.3 — PACE + 9-step + SMK-01..05

### 1.2 What Milestone A is NOT

- Production-ready control plane
- Full `config/policies.yml` enforcement (guardrails, kill_switch, full ABAC)
- MCP ↔ cyanheads TS E2E in CI
- Branch protection enforced (org GitHub **free** private — discipline only)
- 100% coverage or structlog everywhere

---

## 2. Workflow & artifact map

### 2.1 Roles

| Role | Responsibility |
|------|----------------|
| **Claude** | Architecture, audit, adjusted prompts, verdict packets |
| **Cursor** | Code execution, pytest/ruff/mypy, docs sync |
| **Human** | Approve scope, merge, close issues, secrets (Codecov) |

### 2.2 Claude HTML archive (`docs/governance/`)

| File | Role in Phase 1 |
|------|-----------------|
| `ai_control_plane_consolidated_architecture.html` | V3 = union V1+V2; invariants; milestones |
| `cursor_workflow_prompt_system.html` | 3-tier prompts; Milestone A build order |
| `cursor_workflow_continued.html` | Apex stubs, test_apex_loop, launch checklist |
| `phase2_adjusted_prompts.html` | Post-scaffold audit: **4 P0 broken**, P0 fix pack |
| `cursor_claude_reconcile_analysis.html` | Reconcile Claude↔Cursor; NEW-GAP-1..5; ~88% match claim |
| `tab7_telemetry_spec_and_smoke_audit.html` | Tab 7 **APPROVED**; SMK **APPROVE WITH CHANGES**; CI 2-job |

### 2.3 Cursor prompt packets executed (`docs/prompts/`)

| Prompt | Issue / theme | Outcome |
|--------|---------------|---------|
| `CLAUDE_PROMPT_TAB7_TELEMETRY.md` | #23 Tab 7 | ✅ Telemetry seal |
| `CLAUDE_PROMPT_SMOKE_AUDIT.md` | #25 SMK | ✅ SMK v2 + CI smoke job |
| `CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md` | #8, D3 P0-2b | ⏸ **Pending Claude verdict** (§7) |

### 2.4 In-repo governance (markdown)

| File | Role |
|------|------|
| [`PHASE1_REPORT_V2.md`](PHASE1_REPORT_V2.md) | Re-audit + gap IDs + v2 fixes |
| [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md) | MB7 guardrails + kill_switch |
| **This file** | Consolidated packet for Claude pre–Phase 2 |

---

## 3. Chronology — Phase 1 execution

### 3.1 Commit chain

```
629c39f  Milestone A scaffold
4d7408d  P0-1 models/registry/telemetry/TaskStatus
1bd9254  NEW-5 load_policies adapter
8b59189  P0-2 PolicyEngine from YAML
e0461fc  NEW-3/4 apex stubs + test_apex_loop
bc5ea40  NEW-2 fixture unify + smoke gate
5585fc5  Tab 7 telemetry + SMK v2 + CI (#23, #25)
77054ec  Docs sync
b265f9c  Branch protection script (org free-tier limits)
6b3db41  Core tests, structlog (api+mcp), pre-commit file, README
9196ee5  MCP tests, S4 A1 model profiles, debt → #38 close prep
1796c33  Governance HTML archive; DEVELOPMENT_PROTOCOL v1.2
83e3ab5  Phase 1 v2: ingress normalize, parity CI, MCP integration, governance v2
```

### 3.2 Pipeline order actually followed

```
P0-1 → NEW-5 → P0-2 → NEW-3/4 → NEW-2 → SMK gate → Tab 7 (#23)
→ CI 2-job → Track A debt (S7, S4 A1, S5, D2, D4, D6, Q9)
→ Close #38 → Re-audit → Phase 1 v2 (83e3ab5)
→ Codecov setup + first upload (human)
```

### 3.3 Claude audit → Cursor adjustments (high signal)

| Claude audit finding | Cursor adjustment |
|---------------------|-------------------|
| 4 P0 broken (models, telemetry, empty policy, naming) | P0-1, P0-2, NEW-5; naming partial until v2 |
| Fixture ≠ production `policies.yml` schema | **NEW-2** — fixture uses `rbac`/`abac` schema |
| Adapter more complex than Claude spec | Production `rbac`/`abac` loader; pass-through for tests |
| Tab 7 traps (EventStore, POST /telemetry) | Not violated; `InMemoryTelemetryStore` + MCP emit |
| SMK weak assertions | SMK v2: import, reason non-empty, quota floor 100k |
| Reconcile NEW-GAP-1..5 | Issues scripts, learn.py, CI, fixture naming |

---

## 4. Milestone A (#38) — Definition of Done (actual)

### 4.1 Closed items

| Track | Items |
|-------|-------|
| **P0** | #1–7, #15, #39–43, NEW-2/3/4/5 |
| **Governance** | YAML → PolicyEngine; fail-closed on `/policy/evaluate` |
| **Telemetry** | Hash-chain, MCP `_emit_tool_call` → `TelemetryWriter` (#23) |
| **Quality** | 91 tests; SMK 5/5; CI `Smoke gate` → `Full suite` |
| **Debt** | S7 MCP tests, S4 A1 loader, S5, D2, D4, D6, Q9 |
| **Docs** | README, ARCHITECTURE, DEVELOPMENT_PROTOCOL, governance archive |

### 4.2 Explicitly deferred

| Item | Reason |
|------|--------|
| P0-2b YAML **notation** A/B/C | Architect decision — [`CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`](../prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md) |
| Branch protection | Org DataXMind free tier |
| Guardrails + kill_switch loader | Milestone B MB7 |
| Full ABAC conditions | Milestone B |
| Redis / persistence | Milestone B #29–37 |
| apex SAPAL live | Milestone C |
| `mcp/server_factory`, `server_utils` | V3 plan — not PoC blocker |

---

## 5. Re-audit: Phase 1 v1 report vs reality

### 5.1 Overclaims corrected in v2

| Claim (v1) | Reality |
|------------|---------|
| "Runtime OK" for tool naming | Loader OK only until v2; API ingress + MCP namespace were gaps |
| "Full core/ coverage" | No `fail_under`; ~64.5% on Codecov; `cli/` 0% |
| structlog in DoD | Only `api/server.py` + `mcp/git_server.py` |
| pre-commit in DoD | File exists; **CI runs ruff/mypy directly** |
| MCP E2E policy | v1 tests **mocked** HTTP; v2 added real-policy ASGI test |
| CI tests shipped `config/` | v1 used fixtures only; v2 added `test_shipped_config_parity.py` |
| "88% reconcile" | Not measurable — use GAP-* list below |

### 5.2 Eight invariants — compliance @ `83e3ab5`

| # | Invariant | Status |
|---|-----------|--------|
| 1 | Custom PolicyEngine | ✅ |
| 2 | models.py owns contracts | ✅ |
| 3 | MCP facade only | ✅ |
| 4 | CLI HTTP only (no core.policies import) | ✅ |
| 5 | apex owns SAPAL | ✅ stubs |
| 6 | api/ sole TS bridge | ✅ 7 endpoints |
| 7 | QuotaStore swappable | ✅ in-memory |
| 8 | config/ + ACP_CONFIG_DIR | ✅ + shipped parity CI |

---

## 6. Phase 1 v2 remediation (`83e3ab5`)

### 6.1 Code changes

| Change | Files | Why |
|--------|-------|-----|
| `resolve_policy_tool_name()` | `config/loader.py` | Normalize dot notation + MCP→policy aliases at ingress |
| API ingress normalize | `api/server.py` | `POST /policy/evaluate` accepts `git.read` |
| MCP policy payload normalize | `mcp/git_server.py` | `git_status` → `git_read` for RBAC |
| Shipped config parity tests | `tests/test_shipped_config_parity.py` | CI validates `config/` not only fixtures |
| MCP real policy integration | `tests/test_mcp_policy_integration.py` | ASGITransport, no mocked policy HTTP |
| CI shipped parity step | `.github/workflows/ci.yml` | `-m shipped_config` |
| Docs honest | ARCHITECTURE, DEVELOPMENT_PROTOCOL v1.3, PHASE1_REPORT_V2 | ABAC/guardrails limits documented |

### 6.2 MCP → policy action map (runtime)

| MCP tool | Policy action |
|----------|---------------|
| `git_clone`, `git_branch`, `git_status` | `git_read` |
| `git_commit` | `git_commit` |
| `git_push` | `git_push` |
| `git_pr_create` | `create_pr` |

Telemetry and forwarder keep **MCP name**; policy evaluation uses **mapped action**.

### 6.3 `policies.yml` — what loads today

| YAML section | Milestone A |
|--------------|-------------|
| `rbac.roles` | ✅ Loaded |
| `abac.rules` | ⚠️ Subset — see §6.4 |
| `guardrails` | ❌ Not loaded (engine supports `rule_type: guardrail`) |
| `kill_switch` | ❌ Not enforced |
| `quotas.by_project` | ✅ `load_project_token_limits()` |
| `quotas.by_model_profile` / `by_agent` | ❌ Not wired to runtime |

### 6.4 ABAC adapter limitations (shipped config)

- Rules with `approval_status`, `role_not_in`, or `read_only` → **skipped entirely**
- `Restrict-PII`: maps when `data_class: pii` but **`role_not_in` not enforced** (partial semantics)
- Fixture `tests/fixtures/config/policies.yml` is **simplified ABAC** for unit tests — CI default env uses fixtures

---

## 7. Pending architect decision — P0-2b / #8 / D3

**Packet:** [`docs/prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`](../prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md)

### 7.1 Already done (do not re-litigate)

- `normalize_tool_name()` at YAML load
- `resolve_policy_tool_name()` at API + MCP ingress
- MCP tool catalog remains separate namespace (`git_status`, etc.)

### 7.2 Still open — choose A, B, or C

| Option | Description |
|--------|-------------|
| **A** | Keep shipped YAML dot notation; document as human-facing; engine snake_case |
| **B** | Migrate `config/` + fixtures to snake_case |
| **C** | Hybrid — snake_case in `allowed_actions`; dot in docs only |

### 7.3 Claude output requested

1. Verdict A/B/C + rationale (public beta + fork ergonomics)
2. Cursor execution packet if B/C
3. GitHub comment text for #8 / D3 close or re-scope

---

## 8. Codecov — journey & current state

### 8.1 CI wiring (pre-existing)

```yaml
# .github/workflows/ci.yml — Full suite job
pytest tests/ --cov=ai_control_plane --cov-report=xml
# Upload when vars.CODECOV_ENABLED == 'true'
codecov/codecov-action@v4  # secrets.CODECOV_TOKEN
```

### 8.2 Human setup completed (2026-06-23)

| Step | Status |
|------|--------|
| Codecov GitHub App on org **DataXMind** | ✅ Repo `AI-Control-Plane` selected |
| Configure repo on Codecov dashboard | ✅ |
| `gh secret set CODECOV_TOKEN` | ✅ |
| `gh variable set CODECOV_ENABLED=true` | ✅ |
| First upload (local CLI) commit `83e3ab5` | ✅ S3 upload OK |
| Dashboard | ✅ https://app.codecov.io/github/dataxmind/ai-control-plane |

### 8.3 Token policy banner

*"You must now upload using a token"* — **organizational policy**, not an error. Uploads must use **repository** or **global** upload token. Both local CLI (`CODECOV_TOKEN` env) and GitHub Actions (`secrets.CODECOV_TOKEN`) satisfy this.

**Security note:** Token was exposed in terminal during setup — **should be regenerated** and GitHub secret updated.

### 8.4 Coverage baseline @ `83e3ab5` (Codecov)

| Area | Coverage | Notes |
|------|----------|-------|
| **Total (approx.)** | **~64.5%** | 961 / 1491 tracked lines |
| `apex/` | 100% | Stubs + import tests |
| `core/` | 81.73% | Strong |
| `config/` | 72.31% | Loader tested |
| `api/` | 71.53% | Gaps: identity, tasks, approve paths |
| `mcp/` | 53.33% | stdio loop, forwarder |
| `cli/` | 0% | No CLI tests yet |
| `core/policies.py` | **54.64%** | **High-risk** — prioritize Milestone B |
| `api/server.py` | 62.56% | |
| `mcp/git_server.py` | 53.33% | |

### 8.5 Codecov role vs project gates

| Gate | Role |
|------|------|
| SMK-01..05 | **Mandatory** build verification |
| Shipped parity tests | **Mandatory** in CI |
| Codecov | **Observability** — not blocking (`fail_under` absent, `fail_ci_if_error: false`) |

First upload shows **"Missing Base Commit"** on commit page — normal until second CI/local upload establishes diff baseline.

### 8.6 Not enabled (optional later)

- `codecov.yml` PR comments / targets
- `fail_under` in `pyproject.toml`
- Tab **Tests (New)** on Codecov — separate product; skip for now

---

## 9. Gap registry (master list)

### 9.1 Closed in v2

| ID | Gap | Fix |
|----|-----|-----|
| GAP-TN-1 | API ingress no normalize | `resolve_policy_tool_name()` in server |
| GAP-TN-2 | MCP tools ≠ policy actions | `MCP_TOOL_TO_POLICY_ACTION` |
| GAP-CFG-1 | CI no shipped config test | `test_shipped_config_parity.py` |
| GAP-INT-1 | MCP policy mocked | `test_mcp_policy_integration.py` |
| GAP-DOC-1 | guardrails/ABAC undocumented | ARCHITECTURE § |
| GAP-DOC-2 | coverage/structlog overclaim | Protocol v1.3 |

### 9.2 Open — need Claude / Milestone B

| ID | Gap | Target |
|----|-----|--------|
| GAP-TN-3 | Shipped YAML dot notation | Claude A/B/C (#8) |
| GAP-GR-1 | guardrails not loaded | MB7 Milestone B |
| GAP-GR-2 | kill_switch not enforced | MB7 |
| GAP-ABAC-1 | approval_status, role_not_in, read_only skipped | Milestone B |
| GAP-ABAC-2 | Restrict-PII partial map | Milestone B |
| GAP-Q-1 | quotas by_model_profile / by_agent | Milestone B |
| GAP-S4-1 | model_profiles not in AppState | Milestone B |
| GAP-ID-1 | identity registry-only; 503 on fail | SMK-06 Milestone B |
| GAP-BP-1 | branch protection | Team discipline / Team plan |
| GAP-CC-2 | Codecov CI upload not yet verified post-secret | Next CI push |
| GAP-CLI-1 | cli/ 0% coverage | Milestone B tests |

---

## 10. Verify gates (current)

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v                           # 91 tests
pytest tests/test_smoke.py -v -m smoke     # SMK 5/5
pytest tests/test_shipped_config_parity.py -v -m shipped_config
```

**Env:** Default `ACP_CONFIG_DIR=tests/fixtures/config` (conftest autouse). Shipped parity overrides to `config/`.

**CI:** `Smoke gate` (2 min cap) → `Full suite` (pytest + parity + ruff + mypy + optional Codecov upload).

---

## 11. API surface @ Milestone A close

| Method | Path | Milestone A |
|--------|------|-------------|
| POST | `/policy/evaluate` | ✅ + ingress normalize v2 |
| POST | `/policy/approve` | ✅ in-memory |
| POST | `/identity/verify` | ✅ registry lookup (no JWT) |
| GET | `/health` | ✅ config wire proof |
| POST | `/tasks` | ✅ in-memory |
| GET | `/status/{project_id}` | ✅ |
| GET | `/quota/{project_id}` | ✅ by_project limits |

**Fail-closed:** `/policy/evaluate` → HTTP 200 + `allowed=false` for unknown agent. `/identity/verify` unknown → **503** (differs from policy path).

---

## 12. Questions for Claude (required before Phase 2)

### 12.1 Architecture decisions

1. **P0-2b:** Verdict **A, B, or C** for shipped YAML tool notation? (§7)
2. Should `MCP_TOOL_TO_POLICY_ACTION` live in `loader.py` long-term or move to `mcp/` / config YAML?
3. **Restrict-PII partial map:** fix loader to honor `role_not_in`, or defer full ABAC to Milestone B?
4. **Guardrails:** confirm MB7 as first Milestone B governance task?

### 12.2 Phase 2 ordering

Proposed entry (validate or reorder):

```
1. Claude P0-2b verdict + Cursor packet (if B/C)
2. MB7 guardrails + kill_switch loader
3. ABAC full adapter (approval_status, role_not_in, read_only)
4. Redis / persistence (#29–31)
5. CLI live + tests (approve, quota, logs)
6. Identity JWT + SMK-06
```

### 12.3 Quality / coverage

1. Set Codecov project target (e.g. 70%) now or after Milestone B?
2. Prioritize tests: `policies.py` vs `server.py` vs `cli/` — order?
3. Is ~64.5% acceptable gate for **starting** Milestone B?

### 12.4 Process

1. Does Phase 1 v2 adequately close re-audit concerns, or flag remaining blockers?
2. Any invariant violations or trap regressions missed?
3. Adjusted **Phase 2 prompt pack** — what to add/remove vs `phase2_adjusted_prompts.html`?

---

## 13. Suggested Claude deliverables (Phase 2 entry)

| # | Deliverable |
|---|-------------|
| 1 | **Phase 2 adjusted prompt pack** (markdown or HTML) — ordered tasks with dependencies |
| 2 | **P0-2b verdict** + Cursor packet per [`CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`](../prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md) |
| 3 | **Milestone B sprint 1** scope — max 5 issues with acceptance criteria |
| 4 | **Risk register** update — GAP-* items promoted or closed |
| 5 | **SMK-06** spec draft (identity) if Milestone B includes it |

---

## 14. Reference index

| Resource | Path |
|----------|------|
| Architecture | [`ARCHITECTURE.md`](../../ARCHITECTURE.md) |
| Development Protocol v1.3 | [`docs/DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) |
| Phase 1 v2 report | [`PHASE1_REPORT_V2.md`](PHASE1_REPORT_V2.md) |
| Milestone B backlog | [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md) |
| Tool naming packet | [`docs/prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`](../prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md) |
| Tab 7 packet | [`docs/prompts/CLAUDE_PROMPT_TAB7_TELEMETRY.md`](../prompts/CLAUDE_PROMPT_TAB7_TELEMETRY.md) |
| Smoke packet | [`docs/prompts/CLAUDE_PROMPT_SMOKE_AUDIT.md`](../prompts/CLAUDE_PROMPT_SMOKE_AUDIT.md) |
| Open source gates | [`docs/OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) |
| Issue #38 (closed) | Milestone A DoD |
| Issues #29–37 | Milestone B theme |

---

**Prepared by:** Cursor (consolidation from execution + re-audit + Codecov setup)  
**For:** Claude architect review — **do not execute code** until human approves Phase 2 scope  
**Next human action:** Send this file to Claude → receive verdict + Phase 2 pack → approve → Cursor execute
