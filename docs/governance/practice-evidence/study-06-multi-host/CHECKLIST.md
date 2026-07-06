# Study 06 — Multi-host — Checklist & hướng đi

**Document ID:** ACP-GOV-PRACTICE-STUDY-06-CHECKLIST  
**Status:** **PASS** — 2026-06-25 (full bidirectional LAN, round B policy+assign @ 17:34)  
**Full runbook:** [`RUNBOOK.md`](RUNBOOK.md)

---

## Bạn đã xong Study 01–05 — bước tiếp theo

Study 06 **không chạy được trên 1 terminal giả lập** — cần **2 endpoint mạng** (2 máy, hoặc 1 máy + thiết bị/VM khác).

---

## Topology cụ thể (operator)

| Setup | Doc |
|-------|-----|
| **Laptop Windows (WSL) + Mac Mini M2** — LAN + Tailscale | [**TOPOLOGY_WINDOWS_MAC.md**](TOPOLOGY_WINDOWS_MAC.md) |

---

## Chọn topology (generic)

| Option | Máy A (API) | Máy B (client) | Độ khó |
|--------|-------------|----------------|--------|
| **A** (khuyến nghị) | Laptop WSL `uvicorn 0.0.0.0:8000` | Laptop/PC thứ 2 cùng Wi-Fi | Trung bình |
| **B** | Server / VM Linux Docker | Laptop dev | Cao hơn (firewall) |
| **C** (tối thiểu) | MSI WSL bind `0.0.0.0` | Điện thoại/tablet `curl` qua LAN | Thấp — chỉ health/gov |

---

## Phase 0 — Trước khi bắt đầu

- [x] Study 05 PASS
- [x] IP LAN: Laptop `<LAN_IP_REDACTED>`, Mac `192.168.1.99` (WSL `<WSL_LAN_IP_REDACTED>` chỉ portproxy)
- [x] Mac `ping <LAN_IP_REDACTED>` — 0% loss
- [x] Port 8000 trống trước start; bind `0.0.0.0:8000`
- [x] **Không** dùng `127.0.0.1` cho remote client

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

- [x] Local smoke: rules **8**
- [x] Windows Admin portproxy + firewall `ACP-Study06-TCP8000`

Ghi: Round A API = `<LAN_IP_REDACTED>:8000` (via portproxy); Round B API = `192.168.1.99:8000`

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

- [x] Test 6-1 remote health (round A Mac → Laptop)
- [x] Test 6-2 gov status (cả hai chiều)
- [x] Test 6-3 policy allow (round A)
- [x] Test 6-4 assign + server log (round A; WSL thấy `192.168.16.1`)
- [x] Round B đảo vai: Mac API, Laptop full suite @ 17:34 (`ae6c13a4-...`)

---

## Phase 3 — Evidence

Đã điền [`RESULTS.md`](RESULTS.md) + artifacts:

- `artifacts/topology-lan.json`
- `artifacts/direction-a-health-remote.json`
- `artifacts/direction-a-policy-assign.json`
- `artifacts/direction-b-remote-gov.json`
- `artifacts/direction-b-policy-assign.json`
- `terminal-direction-a-laptop-server.md` / `terminal-direction-a-mac-client.md`
- `terminal-direction-b-mac-server.md` / `terminal-direction-b-laptop-client.md`

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
