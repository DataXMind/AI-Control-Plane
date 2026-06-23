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
ApprovalRequest, ApprovalDecision

### API endpoints (api/server.py)
POST /policy/evaluate → PolicyEvalResponse
POST /policy/approve → ApprovalDecision
POST /identity/verify → AgentIdentity
GET /status/{project_id} → TaskStatus
GET /quota/{project_id} → QuotaStatus

### Milestone mapping
Milestone A: core/ + mcp/ + api/ + cli/assign + cli/status + apex/ stubs
Milestone B: registry Redis backend + ABAC + all 5 API endpoints + cli/approve + cli/quota
Milestone C: apex/ live — sense, analyze, predict, act, learn

### Fail-closed rule
Nếu api/server.py unreachable → TypeScript PolicyClient DENY tool call.
Không có fallback, không có default-allow.

### Open source readiness
See [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) for public-beta gates and release workflow.

### Development protocol
Before any non-trivial code change, follow [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) (PACE + 9-step + P0 gate).
