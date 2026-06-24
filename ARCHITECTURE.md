## Project: ai-control-plane



### Package structure

src/ai_control_plane/ với src layout (pyproject.toml)

CLI entrypoint: agentctl (via console_scripts)



### 8 Hard Invariants (KHÔNG BAO GIỜ vi phạm)

1. core/policies.py không bao giờ bị replace bởi OSS PolicyEngine

2. core/models.py sở hữu TẤT CẢ data contracts

3. mcp/git_server.py là facade DUY NHẤT — không Git logic trong Python

4. cli/ subcommands chỉ gọi core/ và api/ — không import OSS runtimes

5. apex/ sở hữu SAPAL loop — OSS tools được gọi TỪ apex/, không ngược

6. api/ là cross-language bridge DUY NHẤT với TypeScript

7. core/quota.py backend hoàn toàn swappable qua QuotaStore ABC

8. config/ ở root = shipped defaults, runtime path = ACP_CONFIG_DIR env var



### Module inventory (core/models.py)

ProjectConfig, AgentConfig, ModelProfile, PolicyRule, Task, TaskStatus,

TelemetryEvent, PolicyDecision, AgentIdentity, McpError,

ApprovalRequest, ApprovalDecision, RegisteredAction, RbacConfig, Guardrail



### Domain errors (core/exceptions.py)

ControlPlaneError (base), ConfigError, PolicyError, QuotaError, AgentError, ApprovalError



### Config runtime wiring (api/server.py startup)

At `create_app()` / `build_default_app_state()`, YAML from `ACP_CONFIG_DIR` or shipped `config/`:



| Source | Loader | AppState field |

|--------|--------|----------------|

| `policies.yml` | `load_policies()` | `policy_engine`, `policy_rules_count` |

| `agents.yml` | `build_agent_registry()` | `agent_registry`, `agents_loaded` |

| `projects.yml` | `load_projects()` | `projects_loaded` |

| `policies.yml` quotas | `load_project_token_limits()` | `project_limits`, `token_budget` |



### Tool naming convention

ACP uses three distinct namespaces. Do not conflate:

| Layer | Format | Example | Defined in |
|-------|--------|---------|------------|
| Shipped `config/policies.yml` | dot notation | `git.read` | Human operators |
| `PolicyEngine` / API / tests | snake_case | `git_read` | `core/tool_names.py` |
| MCP tool catalog | snake_case | `git_status` | `core/tool_names.py` |
| `allowed_tasks` (agents.yml) | hyphen | `infra-plan` | Task classifier (separate) |

**Adapter (permanent — not a workaround):**
`resolve_policy_tool_name()` in `core/tool_names.py` handles two translations:

1. Dot notation → snake_case: `git.read` → `git_read`
2. MCP tool → policy action: `git_status` → `git_read`

Called at: `POST /policy/evaluate` ingress + MCP policy gate.
Idempotent for snake_case input (pass-through).

`normalize_tool_name()` is used at YAML load time in `config/loader.py`.

**Rationale for Option A (adapter-only):** Dot notation is more readable for human operators editing YAML. Migration to snake_case (Option B) was evaluated and rejected — adapter is the permanent solution. Fork backward compat preserved.

**Identity:** `MCP_TOOL_TO_POLICY_ACTION` dict lives in `core/tool_names.py`.
Telemetry records MCP tool name; `PolicyEngine` evaluates policy action name.

### Policy YAML loading — ABAC condition keys (MB-S1-2)

`load_policies()` maps RBAC, ABAC (including `role_not_in`, `approval_status`, `read_only`), and guardrails.

| Condition key | Loaded | Enforced | Gap ID |
|---------------|--------|----------|--------|
| `environment` | ✅ | ✅ | — |
| `action` / `actions` | ✅ | ✅ | — |
| `role` | ✅ | ✅ | — |
| `data_class` / `data_category` | ✅ | ✅ deny when present | — |
| `role_not_in` | ✅ | ✅ privileged-role exemption on deny rules | — (GAP-ABAC-2 closed) |
| `approval_status` | ✅ | ✅ | — (GAP-ABAC-1 closed) |
| `read_only` | ✅ | ✅ reviewer write guard on allow rules | — (GAP-ABAC-1 closed) |

**Restrict-PII:** denies when `data_category: PII` for roles **outside** `role_not_in` privileged list (e.g. `reviewer` exempt).

**YAML sections not loaded in Milestone A:**

| Section | Status | Milestone |
|---------|--------|-----------|
| `rbac.roles` | ✅ Loaded → `PolicyRule` with `rule_type: rbac` | A |
| `abac.rules` | ✅ Full condition adapter (MB-S1-2) | A |
| `guardrails` | ✅ Loaded → `PolicyRule` with `rule_type: guardrail` | A (MB-S1-1) |
| `kill_switch` | ✅ Loaded; when active, all `/policy/evaluate` deny (HTTP 200) | A (MB-S1-1) |
| `quotas.by_model_profile` | ✅ `load_model_profile_token_limits()` + GET `/quota/profile/{id}` | B |
| `quotas.by_agent` | ✅ `load_agent_token_limits()` + GET `/quota/agent/{id}` | B |
| `quotas.by_project` | ✅ Via `load_project_token_limits()` | A |
| `ActionRegistry` | ✅ `create_action_registry()` — Redis when `ACP_REDIS_URL` | B (#33) |

**Guardrails and kill_switch:** loaded at startup via `load_guardrails()` / `load_kill_switch()` (MB-S1-1, closes GAP-GR-1/2 for load path). `GET /health` bypasses `PolicyEngine`.

Fixture `tests/fixtures/config/policies.yml` uses simplified ABAC for unit tests — CI defaults to fixtures.
Shipped parity: `tests/test_shipped_config_parity.py` (CI).

### API surface (api/server.py only — no api/routes stubs)

| Method | Path | Response |

|--------|------|----------|

| POST | `/policy/evaluate` | PolicyEvalResponse |

| POST | `/policy/approve` | ApprovalDecision |

| POST | `/identity/verify` | AgentIdentity |

| GET | `/health` | HealthResponse (config wire proof) |

| POST | `/tasks` | TaskStatus |

| GET | `/status/{project_id}` | TaskStatus |

| GET | `/quota/{project_id}` | QuotaStatus |



`GET /health` returns: `status`, `config_loaded`, `policy_rules_count`, `agents_loaded`, `projects_loaded` (#39).



### Milestone mapping

Milestone A: core/ + mcp/ + api/ + cli/assign + cli/status + apex/ stubs

**CLI tests (MB-S1-4):** `tests/test_cli_assign.py`, `tests/test_cli_status.py` — `CliRunner` + `respx` mock `ACP_API_URL`; no direct `core/policies.py` import (Invariant #4).

Milestone B: registry Redis backend + ABAC full + all 5 API endpoints + cli/approve + cli/quota

Milestone C: apex/ live — sense, analyze, predict, act, learn



### Fail-closed rule

Nếu api/server.py unreachable → TypeScript PolicyClient DENY tool call.

Không có fallback, không có default-allow.

`ControlPlaneError` và unhandled exceptions → HTTP 503 + `allowed=false` on `/policy/evaluate`.

**HTTP contracts (MB-S1-5):**

- **Identity path** (`POST /identity/verify`): auth failure → **401** (invalid JWT, unknown agent).
- **Policy path** (`POST /policy/evaluate`): authorization failure → **200** + `allowed=false`.
- **Service unavailable:** both paths → **503** on internal errors only.



### Telemetry hash-chain contract

Every `TelemetryEvent` appended via `InMemoryTelemetryStore.append()` is sealed:

- `event_hash` = SHA-256(`previous_hash` + canonical JSON of event, excluding `event_hash`, `previous_hash`, `id`)
- `previous_hash` = previous event's `event_hash` (empty string / `None` chain start for first event)
- Chain integrity: `verify_event_chain(store.list_events())` or `store.verify_chain()`

**Invariant:** `TelemetryWriter.emit()` is the only supported way to append events in production code.
MCP `GitMcpServer._emit_tool_call()` delegates to `TelemetryWriter` — no direct hash computation in `mcp/`.

**Failure mode:** Telemetry emit failures are fail-silent (`structlog.warning`) — they must not alter `PolicyDecision`.

**Thread safety:** `InMemoryTelemetryStore.append()` uses `threading.Lock` (Milestone A in-process store).

`AppState.telemetry_store` holds the shared in-process store for API/MCP wiring (no HTTP ingest endpoint in Milestone A).

### In-memory runtime stores (Milestone A)

| Store | Location | Persistence |
|-------|----------|-------------|
| `TaskStore` | `AppState.task_store` | **File-backed** when `ACP_DATA_DIR` set (`FileTaskStore`); else in-memory (#36) |
| `QuotaStore` | `AppState.quota_store` | Redis when `ACP_REDIS_URL` set; else in-memory |
| `InMemoryTelemetryStore` | `AppState.telemetry_store` | Lost on restart |

Set `ACP_DATA_DIR` in production so `/tasks` and `/status/{project_id}` survive API restarts.



### Open source readiness

See [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) for public-beta gates and release workflow.



### Development protocol

Before any non-trivial code change, follow [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) (PACE + 9-step + P0 gate).



### Execution status (2026-06-23)

Milestone A (#38): **CLOSED** — PoC scaffold. Phase 1 v2 record: [`docs/governance/PHASE1_REPORT_V2.md`](docs/governance/PHASE1_REPORT_V2.md).

P0-2b shipped YAML notation: **CLOSED — Option A** (adapter permanent; `core/tool_names.py`). See ARCHITECTURE § Tool naming.

