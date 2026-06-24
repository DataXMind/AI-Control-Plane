# AI Control Plane — Development Protocol

> **Purpose:** Chuẩn hóa mọi thay đổi code/docs trên **ai-control-plane** — chất lượng, 8 hard invariants, fail-closed governance, tránh schema/wiring drift.

**Document ID:** ACP-DEV-PROTOCOL-001  
**Version:** 1.4  
**Created:** 2026-06-22 (rebased từ ACOP/AEOS Development Protocol template)  
**Last updated:** 2026-06-24 — Milestone C merged (PR #63 `6dfffdf`); hygiene closes #37, #3, #13, #53–#62  
**Status:** ACTIVE  
**Applies to:** Mọi task code/config có rủi ro; docs-only có thể rút gọn (xem §2)

**Owner:** DataXMind maintainers + AI pair (Claude plan / Cursor execute)  
**Review cadence:** Sau mỗi GitHub Milestone (A → B → Public Beta) hoặc khi P0/PACE đổi

---

## 1. Vị trí trong hệ thống quy trình

File này là **cổng bắt buộc trước khi sửa code** cho agent và dev. Nó **không thay** các tài liệu chi tiết — **bổ sung và trỏ tới**:

| Khái niệm | Tài liệu | Phạm vi |
| ---------- | -------- | ------- |
| **Development Protocol (file này)** | `docs/DEVELOPMENT_PROTOCOL.md` | _Khi nào_ áp dụng, PACE, 9 bước, task mới/cập nhật |
| **Architecture & invariants** | [`ARCHITECTURE.md`](../ARCHITECTURE.md) | 8 hard invariants, module inventory, milestones |
| **Code generation rules** | [`.cursorrules`](../.cursorrules) | Pydantic v2, structlog, async I/O, test rules |
| **Open source gates** | [`docs/OPEN_SOURCE_READINESS.md`](OPEN_SOURCE_READINESS.md) | Khi nào public repo / PyPI |
| **Milestone A archive** | [`docs/governance/`](governance/) | Claude audit HTML + **Phase 1 v2 report** (closed #38) |
| **Cursor task prompts** | [`docs/prompts/`](prompts/) | Tab 7, smoke, tool-naming defer packets |
| **Execution backlog** | [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues) | Labels: `bug`, `spec-gap`, `debt`, `quality`, `milestone-b` |
| **Milestone A tracking** | Issue [#38](https://github.com/DataXMind/AI-Control-Plane/issues/38) | **CLOSED** — Definition of Done PoC scaffold |

### Vai trò AI pair (bắt buộc ghi nhớ)

| Vai trò | Trách nhiệm | Không làm |
| ------- | ----------- | --------- |
| **Claude** | Architecture, review, plan, task packet, reject naive wiring | Patch code trực tiếp (trừ khi human chỉ định) |
| **Cursor** | Thực thi code, pytest/ruff/mypy, PR diff cụ thể | Đổi kiến trúc / invariant không qua review |
| **Human** | Approve scope, merge PR, commit/push khi yêu cầu | — |

### PACE — hai tầng

```text
SESSION (mỗi phiên làm việc)
  P  Plan     — đọc ARCHITECTURE + issue liên quan; xác nhận scope
  A  Act      — thực thi theo Development Protocol + micro-PACE
  C  Check    — ruff, mypy, pytest; verify fail-closed nếu chạm api/
  E  Evolve   — cập nhật issue/PR; CHANGELOG khi release

TASK (một issue / một PR) — Standard+ và High-risk
  P  Pause    — phân tích impact; chưa patch
  A  Anchor   — done / pending / not started (trong issue comment)
  C  Confirm  — human hoặc architect approve (đặc biệt P0, schema, policy)
  E  Execute  — sửa file + gates + commit (chỉ khi human yêu cầu)
```

**Gốc template:** ACOP `DEVELOPMENT_PROTOCOL.md` v2.0 + AEOS 9-step process — đã loại bỏ domain R1–R32, pnpm, hexagonal NestJS; thay bằng ACP invariants và Python toolchain.

---

## 2. Khi nào áp dụng (ba mức)

| Mức | Ví dụ | Bắt buộc |
| --- | ----- | -------- |
| **Trivial** | Typo doc, comment, format không đổi hành vi | `ruff` nếu chạm `.py`; không cần 9 bước đầy đủ |
| **Standard** | Feature `core/`, endpoint mới, loader, test file | Steps 1–7 + session **Check**; micro-PACE nếu ≥2 file hoặc chạm `core/` |
| **High-risk** | `models.py`, `policies.py`, policy YAML adapter, schema config, deploy | Full 9 steps + human confirm; không merge khi P0 gate chưa pass |

**Luôn áp dụng** (mọi mức có code):

- 8 hard invariants ([`ARCHITECTURE.md`](../ARCHITECTURE.md))
- Fail-closed cho policy (`allowed=false` khi lỗi/timeout — không default-allow)
- Không secrets trong git; `ACP_*` env cho runtime path
- `core/models.py` = single source of truth cho types (Invariant #2)

---

## 3. Thứ bậc sự thật (tránh drift)

Khi mâu thuẫn, xử lý theo thứ tự:

1. **`ARCHITECTURE.md`** — 8 invariants, milestone scope  
2. **`.cursorrules`** — code style và NEVER rules  
3. **`core/models.py`** — data contracts (code là truth cho types)  
4. **`config/*.yml`** — shipped defaults (runtime qua `ACP_CONFIG_DIR`)  
5. **GitHub issue đang implement** — acceptance criteria  
6. **README / docs phụ** — mô tả, không override code  

**Code** quyết định hành vi thực tế. Nếu code vi phạm invariant → **dừng**, không “sửa lặng”. Nếu docs lệch code → sửa docs hoặc mở issue `debt`.

### Cảnh báo đã audit (không tái phạm)

| Trap | Triệu chứng | Status |
| ---- | ----------- | ------ |
| **Silent default policy** | `PolicyEngine(rules=[])` — YAML không govern | ✅ Fixed P0-2 (#7, #43) |
| **Model drift** | `registry.py` / `telemetry.py` import field không có trong `models.py` | ✅ Fixed P0-1 (#1, #2) |
| **Fixture drift** | `tests/fixtures` khác schema `config/policies.yml` | ✅ Fixed NEW-2 (#40) — fixture uses production schema |
| **Duplicate API** | Logic ở `server.py` nhưng còn `api/routes/*` stub | ✅ Fixed P0-3 (#15) |
| **CLI bypass** | `cli/` import `core.policies` trực tiếp | ✅ OK — CLI dùng HTTP |
| **Shipped config snake_case** | Edit `config/*.yml` actions to snake_case | ✅ DON'T — dot notation intentional (P0-2b Option A) |
| **Tool map outside core** | Define `MCP_TOOL_TO_POLICY_ACTION` outside `core/tool_names.py` | ✅ DON'T — single source of truth |

---

## 4. P0 gate — trước Phase 2 prompts

**P0 gate: PASSED (2026-06-22)** · **Milestone A: CLOSED (2026-06-23, #38)** — pytest full suite + smoke SMK-01..06 + shipped parity CI.

**Phase 1 v2 record:** [`docs/governance/PHASE1_REPORT_V2.md`](governance/PHASE1_REPORT_V2.md) — honest gap list, ingress normalize, MCP→policy map, Codecov notes.

### 4.1 Milestone A closed — governance archive

Artifact Claude (HTML) và prompt Cursor lưu tại repo để audit trail Phase 1. Mở file trong browser (local hoặc GitHub raw).

| Artifact | File | Nội dung |
| -------- | ---- | -------- |
| Architecture V3 consolidate | [ai_control_plane_consolidated_architecture.html](governance/ai_control_plane_consolidated_architecture.html) | V1∪V2 decision matrix, invariants, milestones |
| Cursor workflow (setup → CLI) | [cursor_workflow_prompt_system.html](governance/cursor_workflow_prompt_system.html) | 3-tier prompts, build order Milestone A |
| Cursor workflow (apex, tests) | [cursor_workflow_continued.html](governance/cursor_workflow_continued.html) | Apex stubs, test_apex_loop, launch checklist |
| Phase 2 adjusted (audit) | [phase2_adjusted_prompts.html](governance/phase2_adjusted_prompts.html) | P0 broken items, P0 fix pack, adjusted prompts |
| Claude ↔ Cursor reconcile | [cursor_claude_reconcile_analysis.html](governance/cursor_claude_reconcile_analysis.html) | 88% match, NEW-GAP-1..5, action items |
| Tab 7 + SMK audit | [tab7_telemetry_spec_and_smoke_audit.html](governance/tab7_telemetry_spec_and_smoke_audit.html) | Telemetry APPROVED, SMK APPROVE WITH CHANGES, CI yaml |
| **Phase 1 consolidated (Claude)** | [PHASE1_CONSOLIDATED_FOR_CLAUDE.md](governance/PHASE1_CONSOLIDATED_FOR_CLAUDE.md) | Pre–Phase 2 architect review packet |
| **Phase 1 v2 report** | [PHASE1_REPORT_V2.md](governance/PHASE1_REPORT_V2.md) | Re-audit, gap IDs, v2 remediation, Codecov |
| **Milestone B backlog** | [MILESTONE_B_BACKLOG.md](governance/MILESTONE_B_BACKLOG.md) | **CLOSED** (PR #48–#51) |
| **Milestone C sprint plan** | [MILESTONE_C_SPRINT_PLAN.md](governance/MILESTONE_C_SPRINT_PLAN.md) | **CLOSED** — PR #63 (`6dfffdf`) |
| **Phase 2 Sprint 1 report** | [PHASE2_SPRINT1_REPORT.md](governance/PHASE2_SPRINT1_REPORT.md) | MB-S1-1..5 close, gates, coverage |
| **Phase 2 Sprint 1 audit (final)** | [PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md](governance/PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md) | Checklist 38-item verify + Path B |
| **Full audit snapshot (Claude)** | [acp_full_audit_report.html](governance/acp_full_audit_report.html) | Baseline `fc296d4` — **historical**; see SNAPSHOT_README |
| **Full audit reconciliation (live)** | [ACP_FULL_AUDIT_RECONCILIATION.md](governance/ACP_FULL_AUDIT_RECONCILIATION.md) | master @ `a285539` strict audit |
| **Artifact puzzle map** | [ACP_ARTIFACT_PUZZLE_MAP.md](governance/ACP_ARTIFACT_PUZZLE_MAP.md) | Claude HTML → prompts → execution |
| **Post-MC Cursor prompts** | [ACP_CURSOR_PROMPT_PACKET_POST_MC.md](governance/ACP_CURSOR_PROMPT_PACKET_POST_MC.md) | Remaining doc drift + C+ seeds |

**Cursor prompts (markdown):**

| Prompt | File |
| ------ | ---- |
| Tab 7 telemetry (#23) | [`docs/prompts/CLAUDE_PROMPT_TAB7_TELEMETRY.md`](prompts/CLAUDE_PROMPT_TAB7_TELEMETRY.md) |
| Smoke audit (#25) | [`docs/prompts/CLAUDE_PROMPT_SMOKE_AUDIT.md`](prompts/CLAUDE_PROMPT_SMOKE_AUDIT.md) |
| Tool naming defer (#8, D3) | [`docs/prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`](prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md) |
| Milestone C+ architect depth | [`docs/prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md`](prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md) |

**Verify gate at close:** `pytest tests/` pass · `pytest -m smoke` 8 pass (SMK-01..06 incl. 06b/06c) · `pytest -m shipped_config` pass · CI jobs `Smoke gate` + `Full suite` green.

**Milestone C pre-merge gate (PR #63):** `pytest tests/` **156 passed** · `pytest -m smoke` **8/8** · `ruff` clean · `mypy src --strict` clean.

**Phase 1 v2 (post-close hardening):** `core/tool_names.py`; `test_shipped_config_parity.py`; `test_mcp_policy_integration.py`.

**Milestone B Sprint 1 (closed):** Guardrails/kill_switch (MB-S1-1), ABAC full (MB-S1-2), coverage floor (MB-S1-3), CLI tests (MB-S1-4), identity JWT (MB-S1-5) — see [`PHASE2_SPRINT1_REPORT.md`](governance/PHASE2_SPRINT1_REPORT.md).

**Deferred to Sprint 2:** ~~Redis quota, MCP factory, live CLI approve/quota~~ — **CLOSED** in Milestone B (PR #49–#51). See [`MILESTONE_B_BACKLOG.md`](governance/MILESTONE_B_BACKLOG.md).

**P0-2b closed (Phase 2 P2-0):** Option A — dot notation in shipped `config/`; `core/tool_names.py` is single source of truth.

| Thứ tự | Nội dung | Issues | Status |
| ------ | -------- | ------ | ------ |
| **P0-1** | `models.py` — TelemetryEvent hash fields, TaskStatus.progress, registry types | #1, #2, #10 | ✅ |
| **NEW-5** | `load_policies()` adapter YAML → PolicyRule | #43 | ✅ |
| **NEW-3/4** | apex/ 6 stubs + `test_apex_loop.py` | #41, #42 | ✅ |
| **P0-2** | Wire `PolicyEngine` at API startup | #7 | ✅ |
| **P0-3** | `ControlPlaneError` + xóa api stubs | #3, #15 | ✅ |
| **P0-4** | Wire agents/projects/quotas + `/health` proof | #5, #6, #39 | ✅ |
| **P0-2b** | Tool naming convention | #8 | ✅ CLOSED — Option A: adapter permanent; `core/tool_names.py` |
| **NEW-2** | Unify fixture policies schema | #40 | ✅ Production `rbac`/`abac` schema; adapter path only |

**Verify gate (passed):**

```bash
python -c "from ai_control_plane.core import registry, telemetry; print('P0 OK')"
pytest tests/ -v                    # 91+ tests (incl. v2 parity + MCP integration)
curl -s http://localhost:8000/health | jq .
# Expect: config_loaded=true, policy_rules_count>0, agents_loaded, projects_loaded, model_profiles_loaded
```

**Phase 2 execution order (sau P0 + NEW-2):**

1. ~~**Claude prompt tab 7** — telemetry hash-chain patch (#23)~~ ✅
2. ~~SMK v2 + CI smoke gate (#25)~~ ✅
3. Core module tests (#21–24): `test_models`, `test_registry`, `test_quota`, `test_telemetry` ✅
4. MCP facade tests (#12 S7), schema unify (S5), loader profiles (S4 A1) ✅
5. Debt: D2, D4, D6, Q9 ✅ — P0-2b deferred → `docs/prompts/CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md`
6. CI + ruff/mypy in CI (#25–27); structlog in **api/ + mcp/** (#19 partial); pre-commit file present, CI does not run `pre-commit`
7. README runbook (#13), ARCHITECTURE sync (#14) ✅
8. ~~Close tracking issue #38~~ ✅ **closed** (human, post CI green)

---

## 5. Quy trình task mới (New task)

### 5.1 Human / Architect (Claude) — task ≥ Standard

1. Mở hoặc trỏ GitHub issue (`bug` / `spec-gap` / `debt` / `quality`).
2. Ghi **Goal**, **Non-goals**, **Acceptance criteria**, **Dependencies** (issue #).
3. Ghi **out of scope** (vd. “không Redis”, “không apex logic”).
4. Với High-risk: chờ human approve trước khi Cursor Execute.

### 5.2 Executor (Cursor) — Session **Plan**

1. Đọc [`ARCHITECTURE.md`](../ARCHITECTURE.md) + issue + file sẽ chạm.
2. Kiểm tra P0 gate (§4) nếu task chạm `core/`, `api/server.py`, `config/loader.py`.
3. Trình bày: file dự kiến, rủi ro invariant, thứ tự patch.
4. **Pause** — chờ confirm nếu High-risk hoặc đổi `models.py` / policy adapter.

### 5.3 Executor — **Act** (9 bước §7)

Micro-PACE: Pause → Anchor → Confirm (nếu cần) → Execute.

### 5.4 Session **Check**

```bash
# Từ repo root, venv active
ruff check src/ tests/
mypy src/ai_control_plane          # khi Q8 clean
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke   # ACP smoke gate (§5.5)
# Integration (khi có):
# pytest tests/test_api_server.py -v
```

Env test:

```bash
export ACP_CONFIG_DIR=tests/fixtures/config   # Linux/WSL
# pytest tự set qua conftest autouse fixture khi chạy tests/
```

Manual smoke (khi chạm api/ + cli) — hoặc chạy `scripts/smoke_acp.sh`:

```bash
uvicorn ai_control_plane.api.server:app --reload
agentctl assign rust-gateway agent2 git_read --json
curl -s http://localhost:8000/health | jq .
```

### 5.5 ACP Smoke Gate — 8 tests (gold pattern)

> **Nguồn:** Harness CI/CD smoke pattern + qa-checklist.dev + ISTQB build verification — rút gọn cho control-plane PoC.

**Mục tiêu:** Xác nhận build/deploy **ổn định đủ** để tiếp tục regression/Phase 2 — chạy **&lt; 2 phút**, fail-closed.

| ID | Tên | Lệnh / test | Pass criteria |
| -- | --- | ----------- | ------------- |
| **SMK-01** | Core import | `test_smk01_core_import_python` | No ImportError |
| **SMK-02** | Readiness | `test_smk02_health_readiness` | HTTP 200, `config_loaded=true`, `policy_rules_count>0`, `agents_loaded`, `projects_loaded`, `model_profiles_loaded` |
| **SMK-03** | Policy allow | `test_smk03_policy_allow_critical_path` | `allowed=true` |
| **SMK-04** | Fail-closed deny | `test_smk04_policy_deny_fail_closed` | `allowed=false`, non-empty `reason` |
| **SMK-05** | Quota/config read | `test_smk05_quota_dependency_read` | HTTP 200, `tokens_remaining >= 100000` |
| **SMK-06** | Identity verify | `test_smk06_identity_verify_valid_token` | HTTP 200, `agent_id` matches claim |
| **SMK-06b** | Identity auth fail | `test_smk06b_identity_verify_invalid_token` | HTTP **401** (not 503, not 200+deny) |
| **SMK-06c** | Unknown agent | `test_smk06c_identity_verify_unknown_agent` | HTTP **401** |

**Total:** 8 smoke tests (SMK-01..06 inclusive of 06b, 06c). CI job `Smoke gate` runs `pytest -m smoke`.

**Note:** Smoke runs against `tests/fixtures/config` (production schema after NEW-2). Manual `scripts/smoke_acp.sh --live` covers live HTTP. Identity: HS256 dev stub or JWKS RS256 when `ACP_JWKS_URL` set (MB-S2-8).

**Automated:** `tests/test_smoke.py` (marker `@pytest.mark.smoke`)  
**Script:** `scripts/smoke_acp.sh` — CI: pytest smoke; `scripts/smoke_acp.sh --live` — optional live curl

**Khi nào bắt buộc:** Sau mọi thay đổi `api/server.py`, `config/loader.py`, `core/` contracts; trước Phase 2; trước commit Standard+.

**Thứ tự gate đầy đủ (5 lớp + smoke):**

```text
L1 ruff → L2 mypy → L3 pytest full → L4 integration → SMK-01..06 smoke
```

### 5.6 Session **Evolve**

- Comment issue: done / blocked / cần review
- Cập nhật `ARCHITECTURE.md` hoặc README nếu contract đổi (#14, #13)
- `CHANGELOG.md` khi release tag (chưa bắt buộc mỗi PR)
- Pitfall lặp → mở issue `debt` hoặc ghi vào PR description

**Commit / push:** chỉ khi human yêu cầu. Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.

---

## 6. Quy trình cập nhật task (Update task)

Khi **đổi scope**, **thêm yêu cầu**, hoặc **resume** session:

| Bước | Hành động |
| ---- | --------- |
| 1 | **Pause** — không patch thêm; nêu delta so với approve trước |
| 2 | Cập nhật issue comment: goal mới, file list |
| 3 | **Anchor** lại: done / pending / hủy |
| 4 | **Confirm** nếu delta chạm invariant, `models.py`, policy YAML, hoặc public API |
| 5 | Chạy lại impact (Step 1) cho phần **mới** |
| 6 | Sau code: **Check** + cập nhật issue (không chỉ chat) |

Không coi “update nhỏ” là miễn protocol nếu chạm policy evaluation, config schema, hoặc TypeScript bridge contract.

---

## 7. Chín bước trước khi commit (ACP)

### Step 1 — Cross-module impact

Liệt kê file **sẽ đổi** vs **bị ảnh hưởng**:

| Layer | Path | Rule |
| ----- | ---- | ---- |
| Contracts | `src/ai_control_plane/core/models.py` | Mọi type mới ở đây |
| Policy | `core/policies.py` | Pure logic, no I/O |
| HTTP bridge | `api/server.py` | Sole TS bridge |
| CLI | `cli/*.py` | HTTP only — no `core.policies` import |
| MCP | `mcp/git_server.py` | Facade — policy via HTTP |
| Config | `config/*.yml`, `config/loader.py` | `ACP_CONFIG_DIR` |
| Tests | `tests/`, `tests/fixtures/config/` | Dùng `conftest.py` |
| Apex | `apex/` | SAPAL loop live (Milestone C, PR #63); không `NotImplementedError` stub |

- Xác nhận path tồn tại; **đọc nội dung** trước patch.
- Config runtime: `ACP_CONFIG_DIR`, `ACP_API_URL`, shipped `config/`.

### Step 2 — I/O analysis

Mỗi hàm/endpoint mới:

- Input / output types (Pydantic v2, type hints đầy đủ)
- **Fail-closed** paths: API 503 + `allowed=false`; MCP → `McpError`
- `core/policies.py`: không network, không filesystem
- Async cho I/O (`httpx`, FastAPI handlers); CLI có thể sync — ghi exception trong PR nếu cần (#18)
- Side effects: in-memory task store, quota store, approval gate

### Step 3 — Workflow before / after

Mô tả luồng với evidence:

- Policy: `RBAC → ABAC deny → ABAC allow → guardrails → default deny/allow`
- Assign: `agentctl` → `POST /policy/evaluate` → `POST /tasks`
- MCP: `tools/call` → HTTP policy → forwarder (stub hoặc cyanheads)
- Invariants preserved: liệt kê #1–#8 ✅ / ⚠️

### Step 4 — Blind spot (15 mục ACP)

Mỗi mục: ✅ / ⚠️ + mitigation / N/A có lý do.

| ID | Câu hỏi |
| -- | ------- |
| BS-01 | **Default-allow trap?** Policy fail có trả `allowed=true` không? |
| BS-02 | **Model drift?** Type mới có trong `models.py` không? |
| BS-03 | **Duplicate type?** `api/schemas` có copy model từ `core` không? |
| BS-04 | **Config vs runtime?** YAML có thực sự load vào engine không? |
| BS-05 | **Tool naming?** | `core/tool_names.py` — `resolve_policy_tool_name()` at API/MCP; `normalize_tool_name()` at YAML load |
| BS-06 | **Fixture drift?** Test YAML cùng schema production? |
| BS-07 | **CLI bypass?** `cli/` có import `core.policies` không? |
| BS-08 | **Git in Python?** Logic git chỉ ở TS forwarder? |
| BS-09 | **OSS in core?** CrewAI/LangChain/AutoGen? |
| BS-10 | **Secrets?** API keys / prod cluster IDs trong diff? |
| BS-11 | **Invariant #2?** `registry`/`telemetry` khớp `models.py`? |
| BS-12 | **Milestone guard?** `apex/` có logic thật trước Milestone C? — ✅ N/A sau PR #63 |
| BS-13 | **Thread safety?** `InMemoryQuotaStore` / shared `AppState`? |
| BS-14 | **Policy timeout?** 2s — có deny đúng không? |
| BS-15 | **Regression tests?** `core/` module có test tương ứng? |

### Step 5 — Sandbox (5 layers)

| Layer | Lệnh |
| ----- | ---- |
| L1 Lint | `ruff check src/ tests/` |
| L2 Types | `mypy src/ai_control_plane` |
| L3 Unit | `pytest tests/ -v` |
| L4 Integration | `pytest tests/test_api_server.py -v` (khi có) |
| L5 Smoke | `pytest tests/test_smoke.py -v -m smoke` hoặc `scripts/smoke_acp.sh` |

`ACP_CONFIG_DIR=tests/fixtures/config` — conftest autouse hoặc export thủ công.

### Step 6 — Patch discipline

- Một anchor rõ ràng mỗi file; không patch mù.
- Multi-file: nếu một file fail gate → dừng batch, fix root cause.
- Scope tối thiểu — không refactor không liên quan issue.
- Sau đổi `models.py` → cập nhật mọi consumer + tests cùng PR.

### Step 7 — Test report

- Test module bị chạm trước; sau đó full `pytest tests/`.
- Policy tests: **real `PolicyEngine`**, không mock engine (`.cursorrules`).
- **Không commit** khi regression chưa hiểu root cause.

### Step 8 — Commit message

```text
<type>: <imperative subject>

- Why (1–3 câu)
- Invariants: #2 models, #6 api bridge, fail-closed, ...
- Tests: pytest N passed; ruff clean
- Issues: #7, #43
```

Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`.

### Step 9 — Recovery

- Checkpoint: branch hoặc stash trước High-risk change.
- API in-memory state mất khi reload — document, không coi là bug Milestone A (#20).
- Revert: `git revert` hoặc PR revert; không force-push `master`.

---

## 8. Quy tắc bổ sung (ACP)

| ID | Quy tắc |
| -- | ------- |
| **D1** | `core/policies.py` không bị thay bởi OSS PolicyEngine (Invariant #1) |
| **D2** | `core/models.py` owns all contracts — không duplicate trong `api/schemas` (Invariant #2) |
| **D3** | `cli/` không import `core.policies` — chỉ HTTP tới `api/` (Invariant #4) |
| **D4** | `mcp/git_server.py` facade only — không git logic Python (Invariant #3) |
| **D5** | Fail-closed: lỗi policy → deny; không fallback allow (Invariant fail-closed) |
| **D6** | `config/` shipped + `ACP_CONFIG_DIR` runtime (Invariant #8) |
| **D7** | `QuotaStore` inject — không hardcode Redis URL (Invariant #7) |
| **D8** | `apex/` SAPAL adapters + `SapalLoop` live since Milestone C (PR #63); pre-C stubs removed |
| **D9** | Tool names: `snake_case` canonical (`git_read`, `k8s_apply_prod`) |
| **D10** | Mỗi file `core/*.py` có `tests/test_*.py` tương ứng |

---

## 9. Checklist nhanh (Standard+ task)

- [ ] Đã đọc `ARCHITECTURE.md` + issue GitHub
- [ ] P0 gate respected (§4) nếu chạm policy/config/models
- [ ] Step 1–3: impact, I/O, workflow
- [ ] Step 4: 15 blind spots (hoặc N/A có lý do)
- [ ] Step 5–7: ruff + pytest (+ mypy) pass
- [ ] Step 8–9: commit message + rollback ghi nhận
- [ ] Không vi phạm 8 invariants / `.cursorrules`
- [ ] Issue cập nhật hoặc PR link issue

**Milestone A:** **CLOSED** ([#38](https://github.com/DataXMind/AI-Control-Plane/issues/38)) — archive §4.1. **Milestone B:** **CLOSED** (PR #48–#51). **Milestone C:** **CLOSED** (PR [#63](https://github.com/DataXMind/AI-Control-Plane/pull/63), `6dfffdf`).

---

## 10. Ví dụ ngắn (ACP)

**Task:** P0-2c — `load_policies()` adapter (#43)

- **Impact:** `config/loader.py`, `api/server.py`, `config/policies.yml`, `tests/test_policies.py`, `ARCHITECTURE.md`
- **Invariants:** #8 config wire; #1 custom PolicyEngine; fail-closed unchanged
- **Blind spots:** BS-04 (YAML loaded), BS-05 (snake_case), BS-06 (fixture unify #40)
- **Check:** `pytest tests/test_policies.py -v`; `curl /health` shows `policy_rules_count > 0` (#39)
- **Evolve:** Close #43; unblock #7, #40

**Task:** Trivial — sửa typo `README.md`

- **Check:** preview markdown only; no 9-step full

---

## 11. Tham chiếu

| Tài liệu | Đường dẫn |
| -------- | --------- |
| Architecture | [`ARCHITECTURE.md`](../ARCHITECTURE.md) |
| Cursor rules | [`.cursorrules`](../.cursorrules) |
| Open source readiness | [`docs/OPEN_SOURCE_READINESS.md`](OPEN_SOURCE_READINESS.md) |
| Milestone A governance archive | [`docs/governance/`](governance/) — §4.1 |
| Cursor prompts (Phase 1) | [`docs/prompts/`](prompts/) |
| GitHub backlog | https://github.com/DataXMind/AI-Control-Plane/issues |
| Milestone A DoD (closed) | https://github.com/DataXMind/AI-Control-Plane/issues/38 |
| Issue bootstrap scripts | `scripts/create_milestone_a_issues.sh`, `scripts/create_new_gap_issues.sh` |
| Template gốc (ACOP) | `D:\Projects\giapha-do-van\docs\DEVELOPMENT_PROTOCOL.md` (import v2.0) |
| Template gốc (AEOS) | `D:\Projects\aeos\docs\DEVELOPMENT_PROTOCOL.md` (9-step + PACE) |

---

**Version:** 1.4 · **Last updated:** 2026-06-22 (Milestone C pre-merge — apex live, gate counts)  
**Supersedes:** ACOP-DEV-PROTOCOL-001 import (nội dung ACOP-specific đã loại bỏ)  
**Project:** [DataXMind/AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane) (private until public-beta gates)
