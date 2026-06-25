# Study 06 — Multi-host (2+ machines) — Runbook

**Document ID:** ACP-GOV-PRACTICE-STUDY-06-RUNBOOK  
**Prerequisite:** Study 01–03 PASS trên ít nhất 1 máy  
**Mục tiêu:** API trên **máy A**, client (`curl` / `agentctl`) trên **máy B** — giống staging thật.

---

## Mô hình

```text
  ┌─────────────────────────────┐         LAN / Wi-Fi          ┌─────────────────────────────┐
  │  MÁY A — API HOST           │  ◄──── TCP :8000 ────────►  │  MÁY B — CLIENT             │
  │  Role: Terminal 1           │                              │  Role: Terminal 2           │
  │  uvicorn 0.0.0.0:8000       │                              │  ACP_API_URL=http://A:8000  │
  │  hoặc Docker publish 8000   │                              │  curl / agentctl            │
  └─────────────────────────────┘                              └─────────────────────────────┘
```

| Câu hỏi | Trả lời |
|---------|---------|
| Cần fork GitHub? | **Không** — `git clone` cùng repo trên mỗi máy |
| Path phải giống nhau? | **Không** — `/mnt/d/...` vs `~/ai-control-plane` đều OK |
| Cần mấy Cursor IDE? | **2** (mỗi máy một workspace) hoặc 1 máy + SSH |
| Cùng mạng? | **Có** — B phải ping được IP của A |

**Không dùng:** copy `.venv` qua mạng — mỗi máy `pip install -e ".[dev]"` riêng.

---

## Phase 0 — Chọn vai trò máy

| Vai trò | OS gợi ý | IP ví dụ |
|---------|----------|----------|
| **Máy A** (API) | WSL/Linux có Python 3.11+ | `192.168.1.50` |
| **Máy B** (client) | WSL/Linux hoặc laptop thứ 2 | `192.168.1.51` |

Trên **máy A**, lấy IP LAN:

```bash
hostname -I | awk '{print $1}'
# hoặc: ip -4 addr show eth0
```

Ghi `API_HOST_IP=...` — dùng trên máy B.

---

## Phase 1 — Clone & setup (CẢ HAI MÁY)

### Máy A và Máy B (lặp lại độc lập)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

**Máy B không bắt buộc** chạy Docker — chỉ cần `agentctl` + `curl`.

Đồng bộ code (sau này):

```bash
git pull origin master
```

---

## Phase 2 — Máy A (Terminal 1 = API server)

### Option A — uvicorn fixture (đơn giản nhất)

```bash
cd ~/AI-Control-Plane   # path trên máy A
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config

# QUAN TRỌNG: bind 0.0.0.0 để máy B truy cập được
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Option B — Docker (PB-9 style)

```bash
cd ~/AI-Control-Plane
docker compose -f examples/minimal/docker-compose.yml up -d --build
# compose đã publish 8000:8000
```

### Máy A — firewall (nếu B không curl được)

**Linux (ufw ví dụ):**

```bash
sudo ufw allow 8000/tcp
sudo ufw status
```

**Windows host + WSL:** có thể cần portproxy — ưu tiên cả A và B đều WSL/Linux cùng LAN trước.

### Máy A — smoke local trước khi sang B

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

**Kỳ vọng:** `config_loaded: true`, `policy_rules_count: 8` (fixture).

---

## Phase 3 — Máy B (Terminal 2 = client only)

Thay `192.168.1.50` bằng IP thật của máy A.

```bash
cd ~/AI-Control-Plane
source .venv/bin/activate
export ACP_API_URL=http://192.168.1.50:8000

# Test 6-1 — reachability
curl -v --connect-timeout 5 "$ACP_API_URL/health"
```

**Kỳ vọng:** HTTP 200, body JSON giống máy A.

```bash
# Test 6-2 — governance UX remote
agentctl gov status
agentctl gov status --json | python3 -m json.tool | head -20

# Test 6-3 — policy path remote
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

# Test 6-4 — assign qua HTTP bridge
agentctl assign rust-gateway agent2 git_read --json
```

**Kỳ vọng:** allow true; task_id trả về; trên **máy A log** thấy `POST /policy/evaluate` + `POST /tasks` từ IP máy B.

```bash
# Test 6-5 — soak một vòng từ máy B (optional)
bash scripts/soak_staging.sh --log /tmp/acp-soak-remote.log
cat /tmp/acp-soak-remote.log
```

---

## Phase 4 — 3 máy (mở rộng tùy chọn)

| Máy | Vai trò |
|-----|---------|
| **A** | API host (uvicorn/Docker) |
| **B** | Operator CLI — drill trên |
| **C** | Soak runner — `nohup bash scripts/soak_staging.sh --loop 3600 --log ... &` với `ACP_API_URL=http://A:8000` |

Máy C **không cần** clone full dev — tối thiểu: `curl`, `bash`, clone repo cho script `soak_staging.sh`.

---

## Troubleshooting

| Triệu chứng | Nguyên nhân | Sửa |
|-------------|-------------|-----|
| B: Connection refused | A bind `127.0.0.1` only | A dùng `--host 0.0.0.0` |
| B: timeout | firewall / khác subnet | mở 8000, ping A |
| rules 8 vs 10 lệch | A/B khác config | A set `ACP_CONFIG_DIR` giống doc; B chỉ đọc API |
| agentctl OK, curl fail | sai `ACP_API_URL` | `echo $ACP_API_URL` trên B |

---

## Dọn tài nguyên

**Máy A:**

```bash
# uvicorn: Ctrl+C
# docker:
docker compose -f examples/minimal/docker-compose.yml down
```

**Máy B:** unset env

```bash
unset ACP_API_URL
```

---

## Evidence checklist

Sau khi chạy, điền [`RESULTS.md`](RESULTS.md):

- [ ] `artifacts/machine-a-health.json` (curl từ A localhost)
- [ ] `artifacts/machine-b-health-remote.json` (curl từ B → A)
- [ ] `artifacts/machine-b-gov-status.json`
- [ ] `terminal-machine-a-server.md`
- [ ] `terminal-machine-b-client.md`
- Ghi IP A, hostname, timestamp

---

## So với Study 01–03

| | Study 01–03 | Study 06 |
|---|-------------|----------|
| Máy | 1 | **2+** |
| `ACP_API_URL` | `localhost` | `http://<IP-A>:8000` |
| Bind | `127.0.0.1` OK | A phải `0.0.0.0` hoặc Docker publish |
