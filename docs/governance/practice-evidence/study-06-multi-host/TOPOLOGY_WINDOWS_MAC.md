# Study 06 — Topology: Windows Laptop (WSL) + Mac Mini M2

**Document ID:** ACP-GOV-PRACTICE-STUDY-06-TOPO-WIN-MAC  
**Operator topology @ 2026-06-25**

| Vai trò | Thiết bị | Ghi chú |
|---------|----------|---------|
| **Máy A — API host** | Laptop **Windows** (WSL Ubuntu) | Đang làm việc trực tiếp — giữ repo + uvicorn |
| **Máy B — Client** | **Mac Mini M2** | Cùng LAN Wi-Fi + **Tailscale** cùng tailnet |
| Cursor IDE | Chỉ cần trên Laptop | Mac chỉ Terminal + `curl` / `agentctl` |

```text
  ┌──────────────────────────────────────┐
  │  LAPTOP WINDOWS                       │
  │  ┌─────────────┐   portproxy :8000   │
  │  │ WSL Ubuntu  │◄────────────────────┼───┐
  │  │ uvicorn     │   (Windows host)    │   │
  │  │ 0.0.0.0:8000│                     │   │  LAN 192.168.x.x
  │  └─────────────┘                     │   │  hoặc
  │  Tailscale 100.x.x.x (Windows)       │   │  Tailscale 100.x.x.x
  └──────────────────────────────────────┘   │
                    ▲                         │
                    └─────────────────────────┘
  ┌──────────────────────────────────────┐
  │  MAC MINI M2 — client only            │
  │  ACP_API_URL=http://<IP-A>:8000       │
  │  curl / agentctl (không chạy uvicorn) │
  └──────────────────────────────────────┘
```

---

## Phân tích — chọn hướng đúng

### Vì sao **Laptop = API**, **Mac = Client**?

| Lý do | Chi tiết |
|-------|----------|
| Bạn đang dev trên Laptop | Repo, `.venv`, Study 01–05 đã ở WSL — không cần setup lại trên Mac |
| Mac chỉ cần client | `git clone` + `pip install` + env `ACP_API_URL` — không chiếm port 8000 trên Mac |
| Study 06 đo **remote HTTP** | Invariant #4: CLI trên B gọi API trên A |

### Vì sao **không** bind `127.0.0.1` trên WSL?

Mac không thể gọi `127.0.0.1` của Laptop — đó là loopback **từng máy**.

### WSL2 — điểm then chốt

Uvicorn chạy **trong WSL**, nhưng Mac kết nối tới **IP Windows** (LAN hoặc Tailscale). Cần **một trong hai**:

| Cách | Khi nào dùng |
|------|----------------|
| **① Portproxy Windows → WSL** | WSL2 classic — **khuyến nghị ổn định** |
| **② WSL mirrored networking** | Win11 + WSL mới — thử trước nếu đã bật; có thể không cần portproxy |

### LAN vs Tailscale — thứ tự thử

| Thứ tự | Đường | Ưu điểm |
|--------|-------|---------|
| **1** | **LAN** `192.168.x.x` | Đơn giản, latency thấp, debug dễ |
| **2** | **Tailscale** `100.x.x.x` | IP ổn định, vẫn hoạt động khi Wi-Fi đổi subnet; giống staging VPN |

Cả hai đều trỏ tới **cùng Windows host IP** + port **8000** (sau portproxy).

### Plan B (nếu portproxy Windows quá phiền)

Đảo vai: **Mac Mini = API** (`uvicorn 0.0.0.0:8000` native macOS), **Laptop = client**. Mac ít vướng WSL; chỉ dùng khi Plan A fail sau ~30 phút troubleshoot.

---

## Phase 0 — Thu thập IP (làm một lần)

### Trên Laptop — WSL

```bash
hostname -I | awk '{print $1}'
# Ghi: WSL_IP=________________  (vd 172.x.x.x)
```

### Trên Laptop — PowerShell (không Admin)

```powershell
ipconfig
# Ghi: WINDOWS_LAN_IP=________________  (IPv4 Wi-Fi/Ethernet, vd 192.168.1.xx)

tailscale ip -4
# Ghi: WINDOWS_TAILSCALE_IP=________________  (vd 100.x.x.x)
```

### Trên Mac Mini

```bash
# LAN
ipconfig getifaddr en0
# hoặc: ifconfig | grep "inet "

tailscale ip -4
# Ghi: MAC_TAILSCALE_IP=________________

# Kiểm tra cùng tailnet
tailscale status | head -20
```

**Checklist:**

- [ ] Mac `ping WINDOWS_LAN_IP` OK (LAN)
- [ ] Mac `ping WINDOWS_TAILSCALE_IP` OK (Tailscale)
- [ ] Cả hai máy thấy nhau trong `tailscale status`

---

## Phase 1 — Máy A: Laptop Windows (WSL) — API

### Terminal WSL (Cursor terminal 1 — giữ chạy)

```bash
cd /mnt/d/Projects/ai-control-plane   # hoặc path repo của bạn
source .venv/bin/activate

# Dọn port cũ
pkill -f "uvicorn ai_control_plane" 2>/dev/null || true
docker compose -f examples/minimal/docker-compose.yml down 2>/dev/null || true
ss -tlnp | grep ':8000' || echo "8000 free"

export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

Đợi: `Application startup complete.`

**Smoke trong WSL:**

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
# Kỳ vọng: policy_rules_count: 8
```

### PowerShell **Admin** trên Windows — portproxy (WSL2)

> Chạy **một lần** mỗi khi WSL IP đổi (sau reboot WSL đôi khi đổi).

```powershell
$wslIp = (wsl hostname -I).Trim().Split(" ")[0]
Write-Host "WSL IP: $wslIp"

netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 2>$null
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIp

netsh interface portproxy show all
```

**Firewall inbound (Admin PowerShell):**

```powershell
New-NetFirewallRule -DisplayName "ACP-Study06-TCP8000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000 -ErrorAction SilentlyContinue
```

### Smoke từ Windows (không qua WSL)

```powershell
curl http://127.0.0.1:8000/health
```

Nếu OK → portproxy hoạt động. Mac có thể thử tiếp.

---

## Phase 2 — Máy B: Mac Mini M2 — Client

### Terminal (Terminal.app / iTerm) — lần đầu setup

```bash
# Công cụ (nếu chưa có)
xcode-select -p 2>/dev/null || xcode-select --install
# Python 3.11+ — Homebrew nếu cần:
# brew install python@3.12

git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Chọn URL — thử LAN trước

```bash
# Thay bằng WINDOWS_LAN_IP thật từ Phase 0
export ACP_API_URL=http://192.168.1.XX:8000
```

**Test 6-1 — reachability:**

```bash
curl -v --connect-timeout 5 "$ACP_API_URL/health"
```

Kỳ vọng: HTTP 200, JSON `policy_rules_count: 8`.

**Nếu LAN timeout** → chuyển Tailscale:

```bash
export ACP_API_URL=http://100.XX.XX.XX:8000   # WINDOWS_TAILSCALE_IP
curl -v --connect-timeout 5 "$ACP_API_URL/health"
```

### Test 6-2 — Governance UX

```bash
agentctl gov status
agentctl gov status --json | head -25
```

Kỳ vọng: `Policy rules: 8`, framework 6-layer.

### Test 6-3 — Policy allow

```bash
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

Kỳ vọng: `"allowed": true`.

### Test 6-4 — CLI assign (HTTP bridge)

```bash
agentctl assign rust-gateway agent2 git_read --json
```

Kỳ vọng: `task_id` + `"state": "PENDING"`.

**Trên Laptop WSL log uvicorn** — tìm dòng từ IP Mac (LAN hoặc 100.x):

```text
POST /policy/evaluate ... 
POST /tasks ...
```

### Test 6-5 — Soak một vòng (tùy chọn)

```bash
bash scripts/soak_staging.sh --log /tmp/acp-soak-remote-mac.log
cat /tmp/acp-soak-remote-mac.log
```

---

## Phase 3 — Ghi evidence Study 06

**Operator run 2026-06-25 — PASS:** [`RESULTS.md`](RESULTS.md) (bidirectional LAN).

| Field | Giá trị operator |
|-------|------------------|
| Topology | Windows WSL API + Mac client (round A); đảo vai round B |
| Round A `ACP_API_URL` | `http://192.168.1.59:8000` |
| Round B `ACP_API_URL` | `http://192.168.1.99:8000` |
| Windows LAN IP | `192.168.1.59` |
| Windows Tailscale IP | `100.102.105.47` |
| Mac LAN IP | `192.168.1.99` |
| Path used | **LAN** (Tailscale up; không drill `100.x`) |

Artifacts: `artifacts/topology-lan.json`, `direction-a-*.json`, `direction-b-remote-gov.json`, `terminal-direction-*.md`.

---

## Troubleshooting

| Triệu chứng | Nguyên nhân | Sửa |
|-------------|-------------|-----|
| Mac timeout LAN | Portproxy chưa set / firewall | Làm lại Phase 1 PowerShell Admin |
| `127.0.0.1` OK trên Windows, Mac fail | Chưa publish ra LAN | `listenaddress=0.0.0.0` trong portproxy |
| LAN fail, Tailscale OK | Router AP isolation | Dùng **Tailscale IP** làm chính |
| Tailscale fail, LAN OK | Dùng LAN cho Study 06 | Ghi rõ trong evidence |
| WSL IP đổi sau sleep | portproxy trỏ IP cũ | Chạy lại lệnh `netsh portproxy add...` |
| Mac `agentctl` lỗi, curl OK | Sai `ACP_API_URL` | `echo $ACP_API_URL` |
| rules 10 vs 8 | A không dùng fixture | A: `export ACP_CONFIG_DIR=tests/fixtures/config` + restart uvicorn |

### Dọn sau Study 06

**PowerShell Admin (Laptop):**

```powershell
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
# Tùy chọn: Remove-NetFirewallRule -DisplayName "ACP-Study06-TCP8000"
```

**WSL:** `Ctrl+C` uvicorn.

**Mac:** `unset ACP_API_URL`

---

## Khuyến nghị cuối cho setup của bạn

1. **Hôm nay:** LAN trước (`WINDOWS_LAN_IP`) — ít biến số nhất.  
2. **Sau khi PASS:** lặp lại Test 6-1 bằng **Tailscale IP** — ghi 2 dòng evidence (LAN + TS).  
3. **Giữ Laptop làm việc bình thường** — chỉ thêm 1 tab WSL uvicorn + 1 lần portproxy Admin.  
4. **Mac không cần Cursor** — chỉ Terminal ~10 phút.  
5. Nếu portproxy block >30 phút → **Plan B:** API trên Mac Mini, client trên Laptop WSL (`ACP_API_URL=http://<MAC_LAN>:8000`).

---

## Liên kết

- [CHECKLIST.md](CHECKLIST.md) — checklist chung  
- [RUNBOOK.md](RUNBOOK.md) — Study 06 multi-host drill
- [`docs/RUNBOOK.md`](../../../RUNBOOK.md) — operator SSOT (Windows/WSL LAN bind)
