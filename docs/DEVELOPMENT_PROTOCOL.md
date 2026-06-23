# AI Control Plane — Development Protocol

> **Purpose:** Chuẩn hóa mọi thay đổi code/docs trên **ai-control-plane** — chất lượng, 8 hard invariants, fail-closed governance, tránh schema/wiring drift.

**Document ID:** ACP-DEV-PROTOCOL-001  
**Version:** 1.1  
**Created:** 2026-06-22 (rebased từ ACOP/AEOS Development Protocol template)  
**Last updated:** 2026-06-22 — Tab 7 telemetry + SMK v2 + CI (#23, #25) merged to master  
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
| **Execution backlog** | [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues) | Labels: `bug`, `spec-gap`, `debt`, `quality`, `milestone-b` |
| **Milestone A tracking** | Issue [#38](https://github.com/DataXMind/AI-Control-Plane/issues/38) | Definition of Done — đóng phase PoC |

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

---

## 4. P0 gate — trước Phase 2 prompts

**P0 gate: PASSED (2026-06-22)** — Phase 2 (telemetry, CI, core test coverage) có thể bắt đầu sau Claude review telemetry tab 7.

| Thứ tự | Nội dung | Issues | Status |
| ------ | -------- | ------ | ------ |
| **P0-1** | `models.py` — TelemetryEvent hash fields, TaskStatus.progress, registry types | #1, #2, #10 | ✅ |
| **NEW-5** | `load_policies()` adapter YAML → PolicyRule | #43 | ✅ |
| **NEW-3/4** | apex/ 6 stubs + `test_apex_loop.py` | #41, #42 | ✅ |
| **P0-2** | Wire `PolicyEngine` at API startup | #7 | ✅ |
| **P0-3** | `ControlPlaneError` + xóa api stubs | #3, #15 | ✅ |
| **P0-4** | Wire agents/projects/quotas + `/health` proof | #5, #6, #39 | ✅ |
| **P0-2b** | Tool naming adapter (`normalize_tool_name`) | #8 | ⚠️ Runtime OK; shipped YAML vẫn dot notation |
| **NEW-2** | Unify fixture policies schema | #40 | ✅ Production `rbac`/`abac` schema; adapter path only |

**Verify gate (passed):**

```bash
python -c "from ai_control_plane.core import registry, telemetry; print('P0 OK')"
pytest tests/ -v
# Current: 49 passed (7 telemetry + 5 smoke + 37 other)
curl -s http://localhost:8000/health | jq .
# Expect: config_loaded=true, policy_rules_count>0, agents_loaded, projects_loaded
```

**Phase 2 execution order (sau P0 + NEW-2):**

1. ~~**Claude prompt tab 7** — telemetry hash-chain patch (#23)~~ ✅
2. ~~SMK v2 + CI smoke gate (#25)~~ ✅
3. Core module tests (#21–24): `test_models`, `test_registry`, `test_quota` — `test_telemetry` ✅
4. CI + pre-commit (#25–27), structlog (#19) — CI ✅; pre-commit pending
5. README runbook (#13), ARCHITECTURE sync (#14)
6. Close tracking issue #38

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

### 5.5 ACP Smoke Gate — 5 tests (gold pattern)

> **Nguồn:** Harness CI/CD smoke pattern + qa-checklist.dev + ISTQB build verification — rút gọn cho control-plane PoC.

**Mục tiêu:** Xác nhận build/deploy **ổn định đủ** để tiếp tục regression/Phase 2 — chạy **&lt; 2 phút**, fail-closed.

| ID | Tên | Lệnh / test | Pass criteria |
| -- | --- | ----------- | ------------- |
| **SMK-01** | Core import | Python `import ai_control_plane.core.registry, telemetry` | No ImportError |
| **SMK-02** | Readiness | `GET /health` hoặc `test_smk02_health_readiness` | HTTP 200, `config_loaded=true`, `policy_rules_count>0` |
| **SMK-03** | Policy allow | `POST /policy/evaluate` backend + `git_read` | `allowed=true` |
| **SMK-04** | Fail-closed deny | `POST /policy/evaluate` unknown agent | `allowed=false`, non-empty `reason` |
| **SMK-05** | Quota/config read | `GET /quota/rust-gateway` | HTTP 200, `tokens_remaining >= 100000` |

**Note:** Smoke runs against `tests/fixtures/config` (production schema after NEW-2). Manual `scripts/smoke_acp.sh --live` covers live HTTP. `POST /identity/verify` — defer SMK-06 to Milestone B.

**Automated:** `tests/test_smoke.py` (marker `@pytest.mark.smoke`)  
**Script:** `scripts/smoke_acp.sh` — CI: pytest smoke; `scripts/smoke_acp.sh --live` — optional live curl

**Khi nào bắt buộc:** Sau mọi thay đổi `api/server.py`, `config/loader.py`, `core/` contracts; trước Phase 2; trước commit Standard+.

**Thứ tự gate đầy đủ (5 lớp + smoke):**

```text
L1 ruff → L2 mypy → L3 pytest full → L4 integration → SMK-01..05 smoke
```

### 5.5 Session **Evolve**

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
| Apex | `apex/` | Stubs only until Milestone C |

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
| BS-05 | **Tool naming?** `git.read` vs `git_read` — đã normalize? |
| BS-06 | **Fixture drift?** Test YAML cùng schema production? |
| BS-07 | **CLI bypass?** `cli/` có import `core.policies` không? |
| BS-08 | **Git in Python?** Logic git chỉ ở TS forwarder? |
| BS-09 | **OSS in core?** CrewAI/LangChain/AutoGen? |
| BS-10 | **Secrets?** API keys / prod cluster IDs trong diff? |
| BS-11 | **Invariant #2?** `registry`/`telemetry` khớp `models.py`? |
| BS-12 | **Milestone guard?** `apex/` có logic thật trước Milestone C? |
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
| **D8** | `apex/` stub `NotImplementedError` until Milestone C (`.cursorrules`) |
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

**Milestone A closed khi:** [#38](https://github.com/DataXMind/AI-Control-Plane/issues/38) + P0 + quality issues done.

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
| GitHub backlog | https://github.com/DataXMind/AI-Control-Plane/issues |
| Milestone A DoD | https://github.com/DataXMind/AI-Control-Plane/issues/38 |
| Issue bootstrap scripts | `scripts/create_milestone_a_issues.sh`, `scripts/create_new_gap_issues.sh` |
| Template gốc (ACOP) | `D:\Projects\giapha-do-van\docs\DEVELOPMENT_PROTOCOL.md` (import v2.0) |
| Template gốc (AEOS) | `D:\Projects\aeos\docs\DEVELOPMENT_PROTOCOL.md` (9-step + PACE) |

---

**Version:** 1.1 · **Last updated:** 2026-06-22 (P0 gate complete)  
**Supersedes:** ACOP-DEV-PROTOCOL-001 import (nội dung ACOP-specific đã loại bỏ)  
**Project:** [DataXMind/AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane) (private until public-beta gates)
