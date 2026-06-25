# Study 03 — Profile C (Docker / PB-9 soak)

**Document ID:** ACP-GOV-PRACTICE-STUDY-03  
**Profile:** C — `docker compose -f examples/minimal/docker-compose.yml`  
**Host:** MSI, WSL, 1 máy / 2 terminal  
**Repo path:** `/mnt/d/Projects/ai-control-plane`  
**Git baseline:** `master` @ `6030ffc`  
**Run date:** 2026-06-25  
**Operator:** local dev (dmin@MSI)  
**Prior:** [Study 01](../study-01-profile-a/RESULTS.md) PASS · [Study 02](../study-02-profile-b/RESULTS.md) PASS

---

## Verdict

| Overall | Ready for Study 04 (ops edge cases) |
|---------|-------------------------------------|
| **PASS** | **Yes** — optional học lỗi vận hành; không chặn PB-9 clock |

---

## Test matrix

| ID | Test | Terminal | Expected | Actual | Result |
|----|------|----------|----------|--------|--------|
| C0 | `docker compose up --build` | T1 | Image build + container start | Built 25.7s, `minimal-acp-api-1` up | ✅ |
| C1 | `GET /health` (host) | T2 | rules=**8**, fixture agents/projects | Khớp Study 01 fixture | ✅ |
| C2 | `soak_staging.sh` ×1 | T2 | `health=ok policy_allowed=True apex=ok` | Khớp @ 05:39:51Z | ✅ |
| C3 | `agentctl gov status` | T2 | rules **8**, CS-01..06 | Khớp | ✅ |
| C4 | `soak_staging.sh` ×2 + log file | T2 | 2 lines in `/tmp/acp-soak-staging.log` | 2 iterations OK | ✅ |
| C5 | Docker healthcheck | T1 | periodic `GET /health` 200 | ~10s interval 127.0.0.1 | ✅ |
| C6 | `docker compose down` | T1 | Clean teardown | Container + network removed | ✅ |

---

## Delta vs Study 02 (điểm đặc biệt)

| Field | Study 02 (uvicorn shipped) | Study 03 (Docker) |
|-------|---------------------------|-------------------|
| Runtime | native uvicorn | **container** `minimal-acp-api-1` |
| Config | `config/` | **fixture** (`ACP_CONFIG_DIR` in compose) |
| `policy_rules_count` | 10 | **8** |
| Client IP in logs | 127.0.0.1 | **172.27.0.1** (host) + 127.0.0.1 (healthcheck) |
| PB-9 soak script | not run | **`soak_staging.sh` PASS** (CS-05 partial) |

**Quan trọng:** rules=8 trong Study 03 **không phải lỗi** — compose cố ý mount fixture; đúng `examples/minimal/docker-compose.yml`.

---

## Giá trị theo terminal

### Terminal 1 — Docker API

| Key | Value |
|-----|--------|
| Command | `docker compose -f examples/minimal/docker-compose.yml up --build` |
| Image | `minimal-acp-api:latest` |
| Container | `minimal-acp-api-1` |
| Bind | `0.0.0.0:8000` (published to host) |
| Build time | ~25.7s |
| Soak workload (from host) | `POST /policy/evaluate`, `GET /quota/rust-gateway`, `POST /apex/trigger` — all **200** @ 05:39:50–51, 05:40:46–47 |
| Governance | `GET /governance/status` 200 @ 05:40:11, 05:41:07 |
| Teardown | `docker compose ... down` — clean exit |

### Terminal 2 — Client / soak

| Key | Value |
|-----|--------|
| `ACP_API_URL` | `http://localhost:8000` |
| `/health` `policy_rules_count` | **8** |
| Soak iteration 1 | `2026-06-25T05:39:51Z` health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok |
| Soak iteration 2 | `2026-06-25T05:40:47Z` (same shape) |
| Log file | `/tmp/acp-soak-staging.log` — 2 lines |

---

## Governance mapping

| Catalog ID | Validated by Study 03 |
|------------|------------------------|
| **CS-05** PB-9 soak | `soak_staging.sh` + `/health` + log file — **operator slice PASS** |
| CS-06 | Partial — `policy_allowed=True` in soak; full deny path = Study 01 A4 |

**PB-9 calendar soak (14 ngày)** vẫn chạy song song — Study 03 chỉ chứng minh **một ngày operator** đúng playbook.

---

## Ops notes

1. Docker **healthcheck** gọi `/health` mỗi ~10s từ trong container (`127.0.0.1`) — song song với soak từ host (`172.27.0.1`).
2. Operator đã **`docker compose down`** — tốt; tránh port zombie trước Profile A/B tiếp theo.
3. Soak log nằm **`/tmp/`** — không trong repo; evidence JSON trong `artifacts/soak-log-excerpt.json`.

---

## Next step

→ [**Study 04 — Ops edge**](../study-04-ops-edge/RUNBOOK.md) (optional)  
→ [**Study 05 — Advanced**](../study-05-advanced-surprises/RUNBOOK.md)  
→ [**Study 06 — Multi-host**](../study-06-multi-host/RUNBOOK.md)
