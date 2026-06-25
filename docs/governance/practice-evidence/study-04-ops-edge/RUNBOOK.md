# Study 04 — Ops edge cases — Runbook

**Document ID:** ACP-GOV-PRACTICE-STUDY-04-RUNBOOK  
**Prerequisite:** Study 01–03 PASS  
**Môi trường:** 1 máy, WSL, 2 terminal Cursor, repo `/mnt/d/Projects/ai-control-plane`  
**Mục tiêu:** Gây lỗi **có chủ đích**, ghi nhận hành vi, tránh nhầm trong production.

**Quy tắc:** Sau mỗi drill **4a → 4b → 4c**, dọn port trước drill tiếp theo.

```bash
# Dọn nhanh giữa các drill
pkill -f "uvicorn ai_control_plane" 2>/dev/null || true
docker compose -f examples/minimal/docker-compose.yml down 2>/dev/null || true
ss -tlnp | grep ':8000' || echo "port 8000 free"
```

---

## Drill 4a — Port conflict

**Học:** Chỉ một process được bind `:8000`.

### Terminal 1 — giữ server A chạy

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

Đợi: `Application startup complete.` **Không Ctrl+C.**

### Terminal 2 — cố start server B (phải FAIL)

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

**Kỳ vọng T2:**

```text
ERROR: [Errno 98] Address already in use
```

### Terminal 2 — xác nhận client vẫn OK qua server A

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/health" | python3 -m json.tool
```

**Kỳ vọng:** HTTP 200, `policy_rules_count: 8`.

### Dọn 4a

- **T1:** `Ctrl+C` uvicorn  
- Chạy lệnh dọn ở đầu runbook.

---

## Drill 4b — `ACP_API_URL` lệch port

**Học:** Client phải trỏ đúng port instance đang chạy.

### Terminal 1 — API trên **8002**

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8002
```

### Terminal 2a — SAI (trỏ 8000)

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/health" | python3 -m json.tool
# hoặc
agentctl gov status
```

**Kỳ vọng (một trong):**

- `Connection refused` / curl exit ≠ 0  
- Hoặc dữ liệu từ **instance cũ/zombie** trên 8000 (nếu còn process) — `policy_rules_count` không khớp 8

Ghi lại bạn thấy gì — đó là “stale endpoint” risk.

### Terminal 2b — ĐÚNG (trỏ 8002)

```bash
export ACP_API_URL=http://localhost:8002
curl -s "$ACP_API_URL/health" | python3 -m json.tool
agentctl gov status
```

**Kỳ vọng:** `policy_rules_count: 8`, gov status rules **8**.

### Dọn 4b

- **T1:** `Ctrl+C`  
- Dọn port 8002 nếu cần: `ss -tlnp | grep 8002`

---

## Drill 4c — Đổi config không restart server

**Học:** `ACP_CONFIG_DIR` chỉ có hiệu lực lúc **process khởi động**.

### Terminal 1 — start với **fixture** (8 rules)

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 — baseline

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print('rules', d['policy_rules_count'], 'agents', len(d['agents_loaded']))"
```

**Kỳ vọng:** `rules 8 agents 3`

### Terminal 2 — đổi env **không** restart T1

```bash
unset ACP_CONFIG_DIR
# KHÔNG restart uvicorn
curl -s "$ACP_API_URL/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print('rules', d['policy_rules_count'], 'agents', len(d['agents_loaded']))"
agentctl gov status | head -5
```

**Kỳ vọng:** Vẫn **rules 8 agents 3** — server không đổi.

### Terminal 1 — restart đúng cách → shipped config

```bash
# Ctrl+C trên T1, rồi:
unset ACP_CONFIG_DIR
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 — sau restart

```bash
curl -s "$ACP_API_URL/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print('rules', d['policy_rules_count'], 'agents', len(d['agents_loaded']))"
```

**Kỳ vọng:** `rules 10 agents 4`

### Dọn 4c

- **T1:** `Ctrl+C`

---

## Ghi evidence sau khi chạy

Điền [`RESULTS.md`](RESULTS.md) + paste log vào `terminal-1-server.md` / `terminal-2-client.md` + JSON vào `artifacts/`.

| Drill | Pass criteria |
|-------|----------------|
| 4a | T2 uvicorn fails errno 98; T2 curl :8000 OK |
| 4b | Wrong URL fails/stale; correct :8002 shows rules 8 |
| 4c | Shell env change alone does nothing; restart → rules 10 |

---

## Next

→ [Study 05 — Advanced surprises](../study-05-advanced-surprises/RUNBOOK.md)  
→ [Study 06 — Multi-host](../study-06-multi-host/RUNBOOK.md)
