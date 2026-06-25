# Study 02 — Profile B (shipped config)

**Document ID:** ACP-GOV-PRACTICE-STUDY-02  
**Profile:** B — `unset ACP_CONFIG_DIR` → shipped `config/`  
**Host:** MSI, WSL, 1 máy / 2 terminal / 1 Cursor workspace  
**Repo path:** `/mnt/d/Projects/ai-control-plane`  
**Git baseline:** `master` @ `6030ffc` (PR #86 governance UX)  
**Run date:** 2026-06-25  
**Operator:** local dev (dmin@MSI)  
**Prior study:** [Study 01 — Profile A](../study-01-profile-a/RESULTS.md) PASS

---

## Verdict

| Overall | Ready for Study 03 (Profile C / Docker) |
|---------|------------------------------------------|
| **PASS** | **Yes** — dừng uvicorn T1 (`Ctrl+C`), chạy `docker compose down` nếu có, rồi Profile C |

---

## Test matrix

| ID | Test | Terminal | Expected | Actual | Result |
|----|------|----------|----------|--------|--------|
| B0 | `unset ACP_CONFIG_DIR` + uvicorn | T1 | Start on :8000 | `Application startup complete` | ✅ |
| B1 | `GET /health` | T2 | rules=**10**, agent1–**4**, 2 projects | Khớp | ✅ |
| B2 | `agentctl gov status` | T2 | Policy rules **10**, CS-01..06 | Khớp | ✅ |
| B3 | `agentctl assign` | T2 | Task PENDING, policy path OK | task_id returned, state PENDING | ✅ |
| B3b | `POST /policy/evaluate` + `POST /tasks` | T1 log | 200, `X-Agent-Id: agent2` | Khớp | ✅ |

**Không chạy trong Study 02 (đã cover Study 01):** smoke pytest, policy deny unknown agent — vẫn hợp lệ cho Profile B.

---

## Delta vs Study 01 (giá trị đặc biệt)

| Field | Study 01 (fixture) | Study 02 (shipped) |
|-------|-------------------|-------------------|
| `ACP_CONFIG_DIR` | `tests/fixtures/config` | unset → `config/` |
| `policy_rules_count` | 8 | **10** |
| `agents_loaded` | agent1–3 | agent1–**4** |
| `projects_loaded` | rust-gateway | rust-gateway + **datax-analytics** |
| `model_profiles_loaded` | 3 profiles | **4** (+ `claude-team-analytics`) |

Đây là bằng chứng **shipped template** khác fixture CI — quan trọng trước PB-10 production soak.

---

## Giá trị theo terminal

### Terminal 1 — API server

| Key | Value |
|-----|--------|
| `ACP_CONFIG_DIR` | unset (default `config/`) |
| Bind | `127.0.0.1:8000` |
| Uvicorn PID (worker) | 5010 (reloader 4947) |
| Startup | 2026-06-25 ~12:26 |
| Requests | `GET /health`, `GET /governance/status`, `POST /policy/evaluate`, `POST /tasks` — all **200** |
| CLI trace | `agent_id=agent2` on policy + tasks (HTTP-only CLI path) |

### Terminal 2 — Client

| Key | Value |
|-----|--------|
| `ACP_API_URL` | `http://localhost:8000` |
| `/health` `policy_rules_count` | **10** |
| `/health` `agents_loaded` | agent1, agent2, agent3, agent4 |
| `/health` `projects_loaded` | datax-analytics, rust-gateway |
| `agentctl assign` | task `5fcbe7f5-c943-4e0e-9e3e-d3897597f5ae`, state `PENDING` |

---

## Chú ý đặc biệt trước Study 03

1. **Dừng uvicorn T1** — Profile C (Docker) cũng bind `:8000` → conflict nếu không `Ctrl+C`.
2. **Docker trong WSL** — cần `docker compose` hoạt động; Study 03 không dùng uvicorn local.
3. **Config trong container** — `docker-compose.yml` dùng **fixture** lại → kỳ vọng `policy_rules_count: 8` (không phải 10). Đây là hành vi đúng của PB-9 minimal stack.
4. **Port 8001** — nếu còn process cũ, không ảnh hưởng Study 03 trừ khi bạn đổi port compose.

---

## Next step

→ **Study 03 — Profile C** — `docs/governance/practice-evidence/study-03-profile-c/` (sẽ thêm sau operator run)

Commands:

```bash
# T1: Ctrl+C uvicorn
docker compose -f examples/minimal/docker-compose.yml up --build
# T2:
export ACP_API_URL=http://localhost:8000
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log
```
