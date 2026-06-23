# Claude Task Packet — Phase 2 Tab 7: Telemetry (#23, Q3)

> **Role:** Architecture / review / task spec — **không patch code** trừ khi human chỉ định.  
> **Executor:** Cursor sau khi Claude approve spec này.  
> **Repo:** DataXMind/AI-Control-Plane (branch `master`, commit sau P0 + NEW-2)

---

## Context — đã hoàn thành (không làm lại)

| Gate | Status |
|------|--------|
| P0-1 | `TelemetryEvent` có `event_id`, `event_hash`, `previous_hash`, `id` trong `core/models.py` |
| P0-2..4 | Config wired; `ControlPlaneError`; `/health` proof |
| NEW-2 | `tests/fixtures/config/policies.yml` = production `rbac`/`abac` schema |
| Smoke | SMK-01..05 pass (`tests/test_smoke.py`, `scripts/smoke_acp.sh`) |
| Tests | **42 pytest pass** — **không có** `tests/test_telemetry.py` |

**Artifact gốc:** `phase2_adjusted_prompts.html` tab 7 — **điều chỉnh** theo code thật bên dưới (không dùng tên `EventStore`).

---

## Files bắt buộc đọc trước khi viết spec

```
@src/ai_control_plane/core/telemetry.py
@src/ai_control_plane/core/models.py          # TelemetryEvent
@src/ai_control_plane/mcp/git_server.py       # _emit_tool_call — chưa seal hash chain
@src/ai_control_plane/api/server.py           # chưa wire TelemetryStore
@src/ai_control_plane/cli/logs.py             # stub Milestone A
@tests/conftest.py
@docs/DEVELOPMENT_PROTOCOL.md                 # §5.5 smoke, §7 D10
@ARCHITECTURE.md
```

---

## Hiện trạng code (evidence)

### `core/telemetry.py` — đã implement

- `compute_event_hash(previous_hash, event)` — SHA-256, excludes `event_hash`, `previous_hash`, `id`
- `seal_event()` — gắn chain metadata
- `verify_event_chain(events)` — verify ordered sequence
- `TelemetryStore` ABC + `InMemoryTelemetryStore` (append, get, list_events, verify_chain)
- `TelemetryWriter.emit()` — wrapper

### Gap / drift

1. **`mcp/git_server.py`** — `_emit_tool_call()` tạo `TelemetryEvent` thô, append list **không** qua `InMemoryTelemetryStore` / **không** seal hash chain
2. **`api/server.py`** — không có `TelemetryStore` trên `AppState`; không có `POST /telemetry` (nếu spec cần — Milestone A minimum?)
3. **`tests/test_telemetry.py`** — **thiếu** (issue Q3 / #23)
4. **OTel export** — dependency có trong `pyproject.toml` nhưng **defer** Milestone A (chỉ structlog/OTel wiring nếu explicit — không bắt buộc tab 7)
5. **cli/logs** — stub; MB4 defer

---

## Yêu cầu Claude deliverable

Viết **task spec** cho Cursor (1 PR scope) gồm:

### 1. Scope (Milestone A — tab 7)

| In scope | Out of scope |
|----------|--------------|
| `tests/test_telemetry.py` đầy đủ Q3 acceptance | Redis / persistent telemetry store |
| Wire MCP emit qua `TelemetryWriter` + sealed chain | `cli/logs` live stream (MB4) |
| Optional: expose store trên `AppState` nếu cần test integration | OTel collector / exporter production |
| Document hash-chain contract trong `ARCHITECTURE.md` (1 đoạn) | Apex `learn.py` logic thật |

### 2. Acceptance criteria (bắt buộc)

```text
- [ ] tests/test_telemetry.py:
      - compute_event_hash deterministic (same input → same hash)
      - seal_event sets previous_hash + event_hash correctly
      - verify_event_chain True for valid chain; False if tampered
      - InMemoryTelemetryStore.append seals + verify_chain() True after N appends
      - get(event_id) returns sealed copy
- [ ] mcp/git_server.py: _emit_tool_call uses TelemetryWriter/InMemoryTelemetryStore (hoặc callback inject store) — events sealed
- [ ] Không vi phạm invariant #2 (types chỉ trong models.py)
- [ ] Không vi phạm invariant #3 (git_server vẫn facade — chỉ emit telemetry, không git logic)
- [ ] pytest tests/test_telemetry.py -v pass; full suite 0 regression
- [ ] ruff clean; mypy không thêm lỗi mới ngoài apex stubs đã biết
- [ ] SMK-01..05 vẫn pass sau thay đổi
```

### 3. API contract decision (Claude quyết định + justify)

Trả lời rõ:

- Milestone A có cần `POST /telemetry/ingest` trên `api/server.py` không?
- Hay chỉ in-process store + MCP emit đủ cho PoC?
- Nếu có endpoint: Pydantic schema ở `api/schemas.py` — re-export từ `TelemetryEvent` hay wrapper?

### 4. Wiring diagram (before / after)

Mô tả luồng:

```text
tools/call → policy HTTP → forwarder
         → TelemetryWriter.emit(sealed event)
         → InMemoryTelemetryStore (PoC)
         → [optional] POST /telemetry for TS bridge
```

### 5. Test plan cho Cursor (copy-paste ready)

```bash
pytest tests/test_telemetry.py -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/ -v
ruff check src/ tests/
```

### 6. Blind spots (BS-01..15 từ DEVELOPMENT_PROTOCOL)

Đánh giá ít nhất: BS-02 model drift, BS-11 registry/telemetry, BS-13 thread safety (InMemory store), BS-15 regression tests.

### 7. Dependencies & issue mapping

- Closes / advances: **#23 Q3**, **#2 B2** (verification), liên quan **#12** MCP tests nếu thêm
- Blocks: không block tab 8 (core tests) — có thể song song `test_registry`, `test_quota`

---

## Cảnh báo — không tái phạm (từ audit)

| Trap | Instruction |
|------|-------------|
| Đổi tên class | Dùng `InMemoryTelemetryStore`, **không** `EventStore` |
| Duplicate model | `TelemetryEvent` chỉ trong `core/models.py` |
| Unsealed MCP events | MCP phải emit **sealed** events hoặc qua store.append |
| Default-allow | Telemetry failure không ảnh hưởng policy deny path |

---

## Output format yêu cầu

Claude trả lời bằng:

1. **Verdict** — ready for Cursor execute? (yes/no + điều kiện)
2. **Spec** — file-by-file change list
3. **Acceptance criteria** — checklist final
4. **Cursor prompt** — 1 block copy-paste để Cursor thực thi (giống format P0-2 adapter packet)

---

## Verify gate sau khi Cursor implement (Claude review)

```python
from ai_control_plane.core.telemetry import InMemoryTelemetryStore, TelemetryWriter
from ai_control_plane.core.models import TelemetryEvent

store = InMemoryTelemetryStore()
writer = TelemetryWriter(store)
e1 = writer.emit(TelemetryEvent(event_type="tool.call", agent_id="a", project_id="p", payload={}))
e2 = writer.emit(TelemetryEvent(event_type="tool.call", agent_id="a", project_id="p", payload={"n": 2}))
assert e1.event_hash != e2.event_hash
assert e2.previous_hash == e1.event_hash
assert store.verify_chain()
print("TAB7 telemetry verified OK")
```
