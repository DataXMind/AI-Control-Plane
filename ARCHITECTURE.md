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

- **Canonical (engine + tests):** `snake_case` — e.g. `git_read`, `k8s_apply_prod`

- **Config YAML (shipped):** dot notation — e.g. `git.read`, `k8s.apply`

- **Adapter:** `config/loader.normalize_tool_name()` at load time (#8, #43)



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

Milestone B: registry Redis backend + ABAC full + all 5 API endpoints + cli/approve + cli/quota

Milestone C: apex/ live — sense, analyze, predict, act, learn



### Fail-closed rule

Nếu api/server.py unreachable → TypeScript PolicyClient DENY tool call.

Không có fallback, không có default-allow.

`ControlPlaneError` và unhandled exceptions → HTTP 503 + `allowed=false` on `/policy/evaluate`.



### Open source readiness

See [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) for public-beta gates and release workflow.



### Development protocol

Before any non-trivial code change, follow [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) (PACE + 9-step + P0 gate).



### Execution status (2026-06-22)

P0 gate + NEW-2 fixture unify: **complete** — Phase 2 tab 7 (telemetry) unblocked pending Claude prompt.

