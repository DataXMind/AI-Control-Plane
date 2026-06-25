# Study 01 — Profile A (fixture / CI)

**Document ID:** ACP-GOV-PRACTICE-STUDY-01  
**Profile:** A — `ACP_CONFIG_DIR=tests/fixtures/config`  
**Host:** MSI, WSL, 1 máy / 2 terminal / 1 Cursor workspace  
**Repo path:** `/mnt/d/Projects/ai-control-plane`  
**Git baseline:** `master` @ `6030ffc` (PR #86 governance UX)  
**Run date:** 2026-06-25  
**Operator:** local dev (dmin@MSI)

---

## Verdict

| Overall | Ready for Study 02 (Profile B) |
|---------|--------------------------------|
| **PASS** | **Yes** — dừng uvicorn T1 (`Ctrl+C`), chuyển `unset ACP_CONFIG_DIR`, start lại Profile B |

---

## Test matrix

| ID | Test | Terminal | Expected | Actual | Result |
|----|------|----------|----------|--------|--------|
| A0 | `pip install -e ".[dev]"` | T1 | Success | Success | ✅ |
| A0b | uvicorn `:8000` (lần 1) | T1 | Start | `Address already in use` | ⚠️ ops |
| A0c | uvicorn `:8000` (lần 2) | T1 | Start | `Application startup complete` | ✅ |
| A1 | `GET /health` | T2 | `policy_rules_count: 8`, agents 1–3, `rust-gateway` | Khớp | ✅ |
| A2 | `agentctl gov status` | T2 | Framework 6-layer, rules 8, CS-01..06 | Khớp | ✅ |
| A2b | `GET /governance/status` | T2 | `policy_rules_count: 8`, milestones | Khớp (head -30) | ✅ |
| A3 | Policy allow `agent2` + `git_read` | T2 | `allowed: true` | `allowed: true`, reason `action permitted` | ✅ |
| A4 | Policy deny unknown agent (CS-06) | T2 | `allowed: false` + reason | `agent 'unknown-agent' not authorized...` | ✅ |
| A5 | `pytest test_smoke.py -m smoke` | T2 | 8 passed | 8 passed in 2.19s | ✅ |

---

## Giá trị theo terminal (tóm tắt)

### Terminal 1 — API server

| Key | Value |
|-----|--------|
| `ACP_CONFIG_DIR` | `tests/fixtures/config` |
| Bind | `127.0.0.1:8000` |
| Uvicorn PID (worker) | 4668 (reloader 4663) |
| Startup | 2026-06-25 ~12:13 UTC+7 |
| Requests served | `GET /health`, `GET /governance/status` ×2, `POST /policy/evaluate` ×2 — all **200** |

### Terminal 2 — Client / gates

| Key | Value |
|-----|--------|
| `ACP_API_URL` | `http://localhost:8000` |
| `ACP_CONFIG_DIR` (pytest) | `tests/fixtures/config` |
| `/health` `policy_rules_count` | **8** |
| `/health` `agents_loaded` | agent1, agent2, agent3 |
| `/health` `projects_loaded` | rust-gateway |
| `/health` `model_profiles_loaded` | claude-pro-backend, claude-team-infra, claude-team-review |
| Governance `framework` | 6-layer-karpathy v1.0 |
| Governance `public_beta.phase` | PB-9 staging soak |
| Policy allow latency | 0.57 ms |
| Policy deny latency | ~0.007 ms |
| Smoke SMK-01..06c | **8/8 PASSED** |

---

## Governance mapping (runtime case studies)

| Catalog ID | Validated by Study 01 |
|------------|------------------------|
| CS-06 Fail-closed | A4 — unknown agent denied with reason |
| CS-05 PB-9 soak | Partial — health OK; full soak = Study 03 + `soak_staging.sh` |
| CS-02 doc_links | A2 — `ux_runtime` path in governance response |

---

## Ops notes (không fail)

1. **Port conflict lần đầu** — process cũ giữ :8000; retry thành công. Khuyến nghị: `ss -tlnp | grep 8000` trước khi start.
2. **Smoke pytest** dùng `TestClient` in-process — không cần uvicorn cho A5; uvicorn vẫn cần cho A1–A4 live HTTP.
3. Log operator gốc: ngoài repo tại `TestCase/Study01/terminal1.md`, `terminal2.md` (path Windows operator).

---

## Next step

→ [**Study 02 — Profile B**](../study-02-profile-b/README.md) (shipped `config/`, kỳ vọng `policy_rules_count: 10`)
