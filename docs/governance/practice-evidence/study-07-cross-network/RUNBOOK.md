# Study 07 — Cross-network — Runbook

**Document ID:** ACP-GOV-PRACTICE-STUDY-07-RUNBOOK  
**Prerequisite:** Study 06 PASS  
**Extends:** Study 06 (same-LAN) → **khác LAN, chỉ overlay VPN**

---

## Mô hình

```text
  ┌─────────────────────────────┐          Tailscale tailnet          ┌─────────────────────────────┐
  │  UBUNTU WORKSTATION (nhà)   │  ◄──── 100.x.x.x :8000 ──────────►  │  LAPTOP WINDOWS (ngoài)     │
  │  API: uvicorn 0.0.0.0:8000  │       (KHÔNG qua LAN 192.168.x)    │  ACP_API_URL=http://100.x:8000│
  │  LAN: 192.168.x.x (local)   │                                      │  Hotspot / Wi-Fi khác       │
  └─────────────────────────────┘                                      └─────────────────────────────┘
```

| Câu hỏi | Trả lời |
|---------|---------|
| Khác Study 06? | Study 06 = **cùng subnet LAN**; Study 07 = **khác mạng vật lý**, bắt buộc Tailscale |
| Ubuntu là VPS được không? | **Có** — `ubuntu-vps` trong tailnet phù hợp nếu workstation chưa sẵn |
| Laptop WSL portproxy? | **Không** khi Laptop chỉ là client; portproxy chỉ khi Laptop host API |
| Mac Mini? | Witness tùy chọn: ping LAN Ubuntu OK trong khi Laptop (ngoài) không ping được |

---

## Phase 0 — Chọn máy Ubuntu

| Option | Host | Ghi chú |
|--------|------|---------|
| **A** (khuyến nghị) | Workstation Ubuntu tại nhà | Giống “staging box” cố định |
| **B** | `ubuntu-vps` (`100.94.21.33` trong tailnet hiện tại) | Cloud Linux, không WSL |

Trên Ubuntu:

```bash
tailscale status
tailscale ip -4    # UBUNTU_TS_IP
hostname -I        # UBUNTU_LAN_IP (chỉ dùng witness / Mac)
```

---

## Phase 1 — Ubuntu: clone + API

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Firewall (Ubuntu)

```bash
# Nếu ufw active — chỉ mở trên tailscale (an toàn hơn mở toàn LAN)
sudo ufw allow in on tailscale0 to any port 8000 proto tcp
# hoặc tạm thời drill:
sudo ufw allow 8000/tcp
```

Smoke local:

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

---

## Phase 2 — Laptop Windows: tách khỏi LAN nhà

1. **Ngắt** Wi-Fi nhà (`192.168.1.x`).
2. Bật **hotspot điện thoại** hoặc Wi-Fi văn phòng / quán cafe.
3. Tailscale vẫn **Connected** trên Windows (`tailscale status` → thấy ubuntu + mac).

**Negative test (bắt buộc):**

```powershell
ping <UBUNTU_LAN_IP>          # phải timeout — chứng minh không cùng LAN
curl.exe http://<UBUNTU_LAN_IP>:8000/health   # phải fail
```

**Positive test (WSL client):**

```bash
export ACP_API_URL=http://<UBUNTU_TS_IP>:8000

curl -v --connect-timeout 10 "$ACP_API_URL/health"
agentctl gov status
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
agentctl assign rust-gateway agent2 git_read --json
```

Ubuntu server log kỳ vọng: request từ **`100.102.105.47`** (Tailscale IP Laptop) hoặc Tailscale IP của client.

---

## Phase 3 — Optional drills

### 7-5 Remote soak (CS-05)

```bash
export ACP_API_URL=http://<UBUNTU_TS_IP>:8000
bash scripts/soak_staging.sh --log /tmp/acp-soak-remote-external.log
cat /tmp/acp-soak-remote-external.log
```

Một iteration đủ cho practice evidence; `--loop 3600` cho PB-9 calendar soak thật.

### Witness (Mac Mini trên LAN nhà)

```bash
curl http://<UBUNTU_LAN_IP>:8000/health    # LAN OK
export ACP_API_URL=http://<UBUNTU_TS_IP>:8000
agentctl gov status                         # overlay OK
```

Chứng minh hai đường cùng lúc — operator ngoài chỉ có đường thứ hai.

### Đảo vai (khó hơn — không bắt buộc)

Laptop (ngoài) host API qua WSL + portproxy + Tailscale serve/funnel — chỉ khi cần drill ngược. Study 07 **không yêu cầu**; Study 06 đã cover Laptop-as-API trên LAN.

---

## Test matrix

| ID | Test | Expected |
|----|------|----------|
| 7-0 | Tailnet membership | Ubuntu + Windows online |
| 7-0n | LAN negative | Laptop (ngoài) không ping/curl Ubuntu LAN |
| 7-1 | Remote health via TS | 200, rules 8 |
| 7-2 | gov status | khớp Ubuntu |
| 7-3 | policy evaluate | allowed true |
| 7-4 | assign | task_id; Ubuntu log IP Tailscale client |
| 7-5 | soak_staging.sh remote | `soak_iter health=ok` (optional) |

---

## Troubleshooting

| Triệu chứng | Sửa |
|-------------|-----|
| Tailscale timeout | `tailscale up` cả hai; kiểm tra ACL tailnet |
| LAN vẫn ping được Ubuntu | Laptop chưa rời Wi-Fi nhà — tắt Wi-Fi, chỉ dùng hotspot |
| curl TS OK từ Mac, fail từ Win | `ufw` Ubuntu; bind `0.0.0.0` |
| WSL curl fail, Windows curl.exe OK | Dùng WSL; hoặc `curl.exe` với cùng URL |
| rules lệch | Ubuntu thiếu `ACP_CONFIG_DIR=tests/fixtures/config` |

---

## Governance mapping

| Item | Study 07 evidence |
|------|-------------------|
| CS-05 PB-9 staging | 7-5 remote soak |
| Invariant #4 | CLI remote qua `ACP_API_URL` |
| L4 multi-site ops | Tailscale-only path |

---

## Next

Sau PASS → điền [`RESULTS.md`](RESULTS.md). Study 07 đóng khoảng trống giữa “cùng Wi-Fi” (06) và “staging VPS thật” (PB-9).
