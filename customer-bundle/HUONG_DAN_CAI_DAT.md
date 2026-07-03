# Hướng dẫn cài đặt ACP — Gói khách hàng (Path C)

**Mã tài liệu:** ACP-CUSTOMER-BUNDLE-RUN-VI-001  
**Đối tượng:** Operator / DevOps triển khai ACP cho khách — **không** cần fork hay clone repo `AI-Control-Plane`  
**Tích hợp ứng dụng (Task 2):** xem [`docs/CLIENT_INTEGRATION.md`](../docs/CLIENT_INTEGRATION.md) (tiếng Anh) — client chỉ cần `ACP_API_URL`

---

## Bạn đang làm gì?

Chạy **dịch vụ AI Control Plane (ACP)** trên máy chủ: policy engine + Redis + file cấu hình YAML.  
Ứng dụng/agent của khách gọi HTTP `POST /policy/evaluate` — **không** sửa mã nguồn ACP.

```text
[Máy khách]  production-config/*.yml  →  Docker (ACP + Redis)  :8000
                                                      ↑
[Người tích hợp]  ACP_API_URL ────────────────────────┘
```

---

## Yêu cầu trước khi cài

- [ ] Docker Compose **v2** (`docker compose version` → v2.x)
- [ ] Linux VPS, WSL2, hoặc macOS (Docker Desktop)
- [ ] Cổng **8000** trống (hoặc đổi `ACP_HOST_PORT`)
- [ ] Mật khẩu Redis mạnh: `openssl rand -hex 32`
- [ ] Quyền pull image GHCR (nếu repo/package private):
  ```bash
  echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USER --password-stdin
  ```
  PAT cần scope `read:packages`.

---

## Bước 1 — Giải nén gói (không git clone)

```bash
sudo mkdir -p /opt/acp
sudo chown "$USER:$USER" /opt/acp
cd /opt/acp

# Giải nén acp-customer-bundle.tgz vào đây (vendor cung cấp)
# tar -xzf acp-customer-bundle.tgz -C /opt/acp
```

**Kiểm tra đủ file:**

```bash
ls -la docker-compose.ghcr.yml docker-compose.production.yml .env.production.example verify-pilot.sh
ls production-config/policies.yml production-config/agents.yml production-config/projects.yml
```

Nếu thiếu file → liên hệ vendor; **không** chạy `cd examples/minimal` (đường dẫn chỉ có trong repo đầy đủ).

---

## Bước 2 — Tạo file môi trường

```bash
cd /opt/acp
cp .env.production.example .env.production
chmod 600 .env.production
```

Sửa `.env.production`:

```bash
ACP_HOST_CONFIG_DIR=/opt/acp/production-config
ACP_HOST_PORT=8000
REDIS_PASSWORD=<dán kết quả openssl rand -hex 32>
```

**Kiểm tra:**

```bash
grep -q 'changeme' .env.production && echo 'LỖI: đổi REDIS_PASSWORD' || echo 'OK: mật khẩu đã đổi'
```

---

## Bước 3 — Chỉnh cấu hình policy (YAML)

Chỉnh trong `/opt/acp/production-config/`:

| File | Nội dung cần sửa |
|------|------------------|
| `agents.yml` | Mỗi bot/agent → `agent_id`, `roles`, `runner` (vd. Antigravity, VS Code) |
| `projects.yml` | Mỗi sản phẩm → `project_id` (mặc định có `rust-gateway` cho Hybrid AI Gateway) |
| `policies.yml` | Quy tắc ALLOW/DENY theo `tool_name` và `role` |

**Không** commit `.env.production` hay secret lên git.

---

## Bước 4 — Khởi động stack

```bash
cd /opt/acp
docker compose -f docker-compose.ghcr.yml \
  -f docker-compose.production.yml \
  --env-file .env.production \
  up -d
```

Đợi ~30 giây lần đầu, rồi:

```bash
bash verify-pilot.sh
```

**Tiêu chí PASS:**

| Kiểm tra | Kỳ vọng |
|----------|---------|
| `docker compose ps` | `acp-api`, `redis` đang chạy / healthy |
| `/health` | `"status": "ok"`, `"config_loaded": true` |
| `policy_rules_count` | **10** (Profile B) |

**Smoke policy thủ công:**

```bash
export ACP_API_URL=http://127.0.0.1:8000

# ALLOW — agent đã đăng ký (vd. agent2 / rust-gateway)
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

# DENY — agent không tồn tại
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"unknown-agent","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

Kỳ vọng: lần 1 `allowed: true` · lần 2 `allowed: false` + `reason` khác rỗng.

---

## Bước 5 — Bàn giao cho team tích hợp (client-of-client)

Cung cấp **chỉ**:

```bash
export ACP_API_URL=http://<IP-hoặc-DNS-máy-ACP>:8000
```

Kèm `agent_id`, `project_id`, `role` đã đăng ký.

Hướng dẫn tích hợp đa ngôn ngữ (Python / Rust / Go / TypeScript):  
[`docs/CLIENT_INTEGRATION.md`](../docs/CLIENT_INTEGRATION.md)

**Ví dụ Hybrid AI Gateway + Antigravity:** [`docs/integrations/HYBRID_AI_GATEWAY.md`](../docs/integrations/HYBRID_AI_GATEWAY.md)

**Gói client (Antigravity env + shell hook):** [`integrations/README.md`](integrations/README.md)

**Không** giao: `REDIS_PASSWORD`, file `.env.production`, hoặc toàn bộ `production-config/` trừ khi họ là operator.

---

## Vận hành hàng ngày

| Việc | Lệnh (từ `/opt/acp`) |
|------|------------------------|
| Xem log | `docker compose -f docker-compose.ghcr.yml -f docker-compose.production.yml --env-file .env.production logs -f acp-api` |
| Đổi policy | Sửa `production-config/*.yml` → `docker compose ... restart acp-api` |
| Dừng | `docker compose -f docker-compose.ghcr.yml -f docker-compose.production.yml --env-file .env.production down` |
| Nâng image | `docker compose ... pull && docker compose ... up -d` |

Config chỉ nạp lại khi **restart** API — sửa YAML xong phải restart.

---

## Bảo mật (checklist)

- [ ] `REDIS_PASSWORD` không còn giá trị mẫu `changeme`
- [ ] `.env.production` quyền `600`
- [ ] `production-config/` không world-readable (`chmod 750`)
- [ ] Internet: dùng reverse proxy + TLS, không expose thẳng `:8000`
- [ ] Thông báo disclaimer **0.x beta** cho team tích hợp

---

## Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách xử lý |
|-------------|-------------|------------|
| GHCR `denied` | Chưa login | `docker login ghcr.io` |
| Container `Restarting` | Image cũ thiếu Redis extra | `docker compose ... pull` hoặc liên hệ vendor |
| `policy_rules_count: 8` | Chạy nhầm stack demo | Phải dùng **cả hai** file compose + `production-config` |
| Client `allowed: false` | Sai `agent_id` / `role` | Kiểm tra `agents.yml` + restart API |
| `curl` JSON rỗng | API chưa sẵn sàng | Chạy lại `verify-pilot.sh` |

---

## Checklist bàn giao operator

- [ ] Bước 1–4 hoàn tất, `verify-pilot.sh` exit 0
- [ ] Allow + deny smoke PASS
- [ ] `ACP_API_URL` đã ghi cho team tích hợp
- [ ] Checklist bảo mật § trên
- [ ] Khách hiểu: **không** cần fork repo ACP

---

**Cập nhật:** 2026-07-01 · Gói: `customer-bundle/` · Image: `ghcr.io/dataxmind/ai-control-plane:demo`
