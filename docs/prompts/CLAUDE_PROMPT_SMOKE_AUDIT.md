# Claude Task Packet — Audit SMK-01..05 Smoke Gate

> **Role:** Architecture review / audit — verify smoke suite đúng gold pattern và đủ cho ACP fail-closed governance.  
> **Không implement** — chỉ audit, đề xuất chỉnh `tests/test_smoke.py`, `docs/DEVELOPMENT_PROTOCOL.md` §5.5, `scripts/smoke_acp.sh`.

---

## Context

Cursor đã thêm **5 smoke tests** theo Harness / qa-checklist / ISTQB build-verification pattern, documented trong `DEVELOPMENT_PROTOCOL.md` v1.1 §5.5.

**Repo state:** P0 gate + NEW-2 complete; 42 pytest pass; smoke script passes.

---

## Files bắt buộc đọc

```
@tests/test_smoke.py
@scripts/smoke_acp.sh
@docs/DEVELOPMENT_PROTOCOL.md              # §5.4, §5.5, Step 5 L5
@tests/test_api_server.py                  # overlap với SMK-02..05?
@tests/conftest.py                         # ACP_CONFIG_DIR autouse
@src/ai_control_plane/api/server.py        # /health, /policy/evaluate, /quota
@ARCHITECTURE.md
```

---

## SMK hiện tại (Cursor implementation)

| ID | Test | Assertion summary |
|----|------|-------------------|
| SMK-01 | `test_smk01_p0_core_import` | subprocess import registry + telemetry |
| SMK-02 | `test_smk02_health_readiness` | GET /health 200, config_loaded, counts |
| SMK-03 | `test_smk03_policy_allow_critical_path` | POST evaluate git_read allowed |
| SMK-04 | `test_smk04_policy_deny_fail_closed` | unknown agent denied |
| SMK-05 | `test_smk05_quota_dependency_read` | GET /quota/rust-gateway tokens_remaining>0 |

**Script:** `scripts/smoke_acp.sh` — SMK-01 shell + `pytest -m smoke`

**Marker:** `@pytest.mark.smoke` in `pyproject.toml`

---

## Gold pattern reference (audit against)

Industry smoke gate thường gồm (~5 checks, <2 min):

1. **Readiness** — service responds; health/ready OK
2. **Auth/identity** — basic identity path (nếu product yêu cầu login)
3. **Core read** — critical GET path
4. **Core write / govern** — one idempotent critical action
5. **Dependency** — DB/cache/config connectivity signal

ACP mapping (Cursor đề xuất):

| Gold pattern | SMK mapping | Gap? |
|--------------|-------------|------|
| Readiness | SMK-02 | ? |
| Identity | *missing* — no POST /identity/verify | ? |
| Core read | SMK-05 quota | ? |
| Core govern | SMK-03 allow + SMK-04 deny | ? |
| Dependency | SMK-01 import + SMK-02 config_loaded | ? |

---

## Câu hỏi audit (Claude trả lời từng mục)

### A. Coverage

1. SMK-01..05 có **đủ** cho ai-control-plane PoC fail-closed governance không?
2. Có **overlap thừa** với `test_api_server.py` không? Nên merge, giữ riêng, hay smoke chỉ gọi subset?
3. Thiếu check nào **critical** so với ARCHITECTURE 8 invariants? (vd. CLI `agentctl assign` HTTP path, MCP facade import)

### B. Correctness

4. SMK-03/04 dùng `TestClient(create_app())` — có test **production config path** (`config/policies.yml`) hay chỉ fixture qua `conftest` autouse?
5. SMK-04 unknown agent → HTTP 200 + `allowed=false` — đúng fail-closed contract? Hay phải 503?
6. SMK-05 `tokens_remaining > 0` — có phải assertion yếu? Nên assert exact limit từ fixture?

### C. Operability

7. `scripts/smoke_acp.sh` có nên start uvicorn và chạy **curl** thật (manual smoke §5.4) thay vì chỉ TestClient?
8. CI (#25) nên chạy smoke như thế nào? (`pytest -m smoke` only vs full script)
9. SMK-01 subprocess — redundant với pytest import collection?

### D. Documentation

10. `DEVELOPMENT_PROTOCOL.md` §5.5 có khớp implementation không?
11. Có cần **SMK-06** (identity verify) hoặc đổi SMK-02/03 cho Milestone A?

### E. Verdict

12. **APPROVE** / **APPROVE WITH CHANGES** / **REJECT** — kèm danh sách thay đổi cụ thể cho Cursor (nếu có)

---

## Deliverable format

Claude trả:

```markdown
## Smoke Audit Verdict: [APPROVE | APPROVE WITH CHANGES | REJECT]

### Findings (ordered by severity)
| ID | Severity | Finding | Recommendation |

### SMK matrix (gold pattern ↔ ACP)
| Gold | SMK | Status | Action |

### Proposed SMK-01..05 v2 (if changes)
| ID | Name | Test/command | Pass criteria |

### Cursor follow-up prompt (if changes needed)
[copy-paste block]

### CI recommendation (#25)
[how to wire smoke in GitHub Actions]
```

---

## Constraints

- Giữ suite **< 2 phút** total runtime
- Không thêm Redis, Docker, external services cho smoke Milestone A
- Fail-closed: smoke failure = block merge (khi CI có)
- Không duplicate 15+ checks (regression territory)

---

## Current verify commands (for Claude to re-run mentally)

```bash
pytest tests/test_smoke.py -v -m smoke
./scripts/smoke_acp.sh
pytest tests/test_api_server.py -v
```

Expected: all pass with `ACP_CONFIG_DIR=tests/fixtures/config` (conftest autouse).
