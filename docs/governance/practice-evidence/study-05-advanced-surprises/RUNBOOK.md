# Study 05 — Advanced / surprise scenarios — Runbook

**Document ID:** ACP-GOV-PRACTICE-STUDY-05-RUNBOOK  
**Độ khó:** Cao — tình huống “không ngờ” khi vận hành  
**Prerequisite:** Study 01–03 PASS; nên làm Study 04 trước  
**Môi trường:** 1 máy, 2 terminal (một số drill cần Docker)

**Mục tiêu:** Kiểm tra **fail-closed**, từ chối policy, stack conflict, API down — không chỉ happy path.

---

## Chuẩn bị chung

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
```

Dọn trước mỗi drill: port 8000/8002 trống, không docker + uvicorn cùng lúc (trừ drill 5d cố ý).

---

## Drill 5a — API down, CLI phải lỗi rõ (fail-closed client)

**Liên quan:** CS-06, Invariant #4

### Terminal 1

**Không chạy API** — hoặc `Ctrl+C` nếu đang có uvicorn.

```bash
ss -tlnp | grep ':8000' || echo "8000 free — good"
```

### Terminal 2

```bash
export ACP_API_URL=http://localhost:8000
agentctl gov status
```

**Kỳ vọng:** Lỗi kết nối / timeout (httpx) — **không** in framework giả hay rules=0 im lặng.

```bash
agentctl assign rust-gateway agent2 git_read --json
```

**Kỳ vọng:** Lỗi — không tạo task local “ảo”.

---

## Drill 5b — Policy deny: agent không thuộc project

### Terminal 1

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2

```bash
export ACP_API_URL=http://localhost:8000
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent1","project_id":"rust-gateway","tool_name":"git_read","role":"infra"}' \
  | python3 -m json.tool
```

**Ghi chú:** agent1 trong fixture gắn `rust-gateway` — nếu allow, thử `agent3` (reviewer) + `git_push` hoặc tool bị deny:

```bash
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent3","project_id":"rust-gateway","tool_name":"git_push","role":"reviewer"}' \
  | python3 -m json.tool
```

**Kỳ vọng:** `"allowed": false` + `reason` có nghĩa (reviewer read-only / denied action).

---

## Drill 5c — Request body invalid (API validation)

### Terminal 1 — uvicorn đang chạy (5b)

### Terminal 2

```bash
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2"}' \
  | python3 -m json.tool
```

**Kỳ vọng:** HTTP **422** validation error — không 500, không default-allow.

---

## Drill 5d — Docker + uvicorn cùng port 8000 (stack war)

**Liên quan:** Study 03 teardown — nếu quên `down`, drill này tái hiện chaos.

### Terminal 1 — start Docker

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -s http://localhost:8000/health | python3 -m json.tool
```

Ghi `policy_rules_count` (kỳ vọng **8**).

### Terminal 2 — cố uvicorn cùng port

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

**Kỳ vọng:** `Address already in use` HOẶC (tùy Docker/WSL) bind lỗi — **không** có hai API healthy cùng port.

### Terminal 2 — curl liên tục trong lúc nghi ngờ conflict

```bash
for i in 1 2 3; do
  curl -sf "$ACP_API_URL/health" | python3 -c "import sys,json; print(json.load(sys.stdin)['policy_rules_count'])"
  sleep 1
done
```

**Kỳ vọng:** Cùng một số rules ổn định (8 từ container) — không nhảy 8↔10.

### Dọn

```bash
docker compose -f examples/minimal/docker-compose.yml down
```

---

## Drill 5e — Stale image sau đổi code (Docker surprise)

**Liên quan:** PB-9 — phải `--build` sau thay đổi `src/`.

### Terminal 1

```bash
docker compose -f examples/minimal/docker-compose.yml up -d
# Sửa tạm comment trong src/ai_control_plane/core/governance_catalog.py (GOVERNANCE_VERSION)
# KHÔNG rebuild:
docker compose -f examples/minimal/docker-compose.yml up -d
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/governance/status" | python3 -c "import sys,json; print(json.load(sys.stdin).get('governance_version'))"
```

Ghi version. Sau đó:

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -s "$ACP_API_URL/governance/status" | python3 -c "import sys,json; print(json.load(sys.stdin).get('governance_version'))"
```

**Kỳ vọng:** Không `--build` → version cũ trong container; `--build` → khớp code working tree (hoặc thay đổi của bạn).

**Hoàn tác:** `git checkout -- src/...` nếu sửa thử.

### Dọn

```bash
docker compose -f examples/minimal/docker-compose.yml down
```

---

## Drill 5f — Identity verify: token xấu (live HTTP)

### Terminal 1

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2

```bash
export ACP_API_URL=http://localhost:8000
curl -s -X POST "$ACP_API_URL/identity/verify" \
  -H "Content-Type: application/json" \
  -d '{"token":"not-a-valid-jwt","agent_id":"agent2"}' \
  | python3 -m json.tool
```

**Kỳ vọng:** `valid: false` hoặc HTTP 4xx — không `valid: true`.

---

## Drill 5g — Kill switch (nếu bật trong config)

Đọc `tests/fixtures/config/policies.yml` → `kill_switch.active`.

Nếu `false`, **chỉ ghi nhận** “skipped — kill_switch inactive”.  
Để test thật (chỉ trên branch local / không commit):

1. Sửa tạm `kill_switch.active: true` trong fixture copy hoặc override file test.  
2. Restart uvicorn.  
3. `POST /policy/evaluate` allow path → kỳ vọng **deny** toàn cục.

**Không commit** thay đổi kill_switch vào repo.

---

## Ghi evidence

Điền `study-05-advanced-surprises/RESULTS.md` sau khi chạy. Mỗi drill một dòng PASS/FAIL.

| Drill | Mức độ |
|-------|--------|
| 5a | API down / CLI |
| 5b | Policy deny |
| 5c | Validation 422 |
| 5d | Port stack war |
| 5e | Docker stale image |
| 5f | Identity bad token |
| 5g | Kill switch (optional) |

---

## Next

→ [Study 06 — Multi-host](../study-06-multi-host/RUNBOOK.md)
