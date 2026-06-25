# Study 06 — Multi-host — Checklist & hướng đi

**Document ID:** ACP-GOV-PRACTICE-STUDY-06-CHECKLIST  
**Status:** PENDING — sẵn sàng sau Study 05 PASS  
**Full runbook:** [`RUNBOOK.md`](RUNBOOK.md)

---

## Bạn đã xong Study 01–05 — bước tiếp theo

Study 06 **không chạy được trên 1 terminal giả lập** — cần **2 endpoint mạng** (2 máy, hoặc 1 máy + thiết bị/VM khác).

---

## Chọn topology

| Option | Máy A (API) | Máy B (client) | Độ khó |
|--------|-------------|----------------|--------|
| **A** (khuyến nghị) | Laptop WSL `uvicorn 0.0.0.0:8000` | Laptop/PC thứ 2 cùng Wi-Fi | Trung bình |
| **B** | Server / VM Linux Docker | Laptop dev | Cao hơn (firewall) |
| **C** (tối thiểu) | MSI WSL bind `0.0.0.0` | Điện thoại/tablet `curl` qua LAN | Thấp — chỉ health/gov |

---

## Phase 0 — Trước khi bắt đầu

- [ ] Study 05 PASS (hoặc tối thiểu 01–04 + 05a/05b)
- [ ] Biết IP LAN máy A: `hostname -I | awk '{print $1}'`
- [ ] Máy B `ping <IP-A>` thành công
- [ ] Port 8000 trống trên A: `ss -tlnp | grep 8000`
- [ ] **Không** dùng `127.0.0.1` bind trên A

---

## Phase 1 — Máy A (Terminal 1)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

- [ ] Local smoke: `curl -s http://127.0.0.1:8000/health` → rules **8**
- [ ] (Nếu B không kết nối) mở firewall: `sudo ufw allow 8000/tcp`

Ghi: `API_HOST_IP=____________`

---

## Phase 2 — Máy B (Terminal 2)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

export ACP_API_URL=http://<API_HOST_IP>:8000   # thay IP thật

curl -v --connect-timeout 5 "$ACP_API_URL/health"
agentctl gov status
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
agentctl assign rust-gateway agent2 git_read --json
```

- [ ] Test 6-1 remote health → 200, rules **8**
- [ ] Test 6-2 gov status khớp A
- [ ] Test 6-3 policy allow true
- [ ] Test 6-4 assign → task_id; **log A** thấy request từ IP B

---

## Phase 3 — Evidence

Sau khi PASS, điền [`RESULTS.md`](RESULTS.md) + artifacts:

- `artifacts/machine-a-health.json`
- `artifacts/machine-b-health-remote.json`
- `terminal-machine-a-server.md`
- `terminal-machine-b-client.md`

---

## Troubleshooting nhanh

| Vấn đề | Sửa |
|--------|-----|
| B timeout | A dùng `0.0.0.0`; firewall; cùng subnet |
| rules lệch | B chỉ đọc API A — không set `ACP_CONFIG_DIR` để “đổi” server |
| WSL2 + Windows | Thử IP Windows host (`ipconfig`) hoặc mirrored networking |

---

## Sau Study 06

- Merge PR practice-evidence (#87) khi CI xanh
- Tiếp PB-9 soak calendar (không thay thế Study 06)
- Tùy chọn: lặp 5e với sửa `GOVERNANCE_VERSION`; lặp 5g với RUNBOOK §5g mới
