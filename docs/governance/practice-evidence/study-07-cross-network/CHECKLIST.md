# Study 07 — Cross-network — Checklist

**Document ID:** ACP-GOV-PRACTICE-STUDY-07-CHECKLIST  
**Status:** PENDING — sau Study 06 PASS  
**Topology:** [`TOPOLOGY_UBUNTU_TAILSCALE.md`](TOPOLOGY_UBUNTU_TAILSCALE.md)  
**Runbook:** [`RUNBOOK.md`](RUNBOOK.md)

---

## Điều kiện topology

| Host | Vai trò | Mạng vật lý | Kết nối tới API |
|------|---------|-------------|-----------------|
| **Ubuntu workstation** | API (máy A) | LAN nhà / rack (ổn định) | bind `0.0.0.0:8000` |
| **Laptop Windows** | Client (máy B) | **Mạng ngoài** (hotspot 4G, Wi-Fi khác) | **chỉ** `100.x.x.x` Tailscale |
| Mac Mini (tùy chọn) | Witness | LAN nhà | so sánh LAN vs overlay |

- [ ] Study 06 PASS
- [ ] Cả Ubuntu + Windows cùng **tailnet** (`tailscale status` thấy nhau)
- [ ] Laptop **ngắt** Wi-Fi nhà (`192.168.1.x`) trước drill chính
- [ ] `ping <ubuntu_lan_ip>` từ Laptop (mạng ngoài) → **fail** (chứng minh không đi LAN)
- [ ] `curl http://<ubuntu_tailscale_ip>:8000/health` từ Laptop → **200**

---

## Phase 1 — Ubuntu API

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

- [ ] `tailscale ip -4` ghi `UBUNTU_TS_IP=`
- [ ] Local: `curl -s http://127.0.0.1:8000/health` → rules **8**
- [ ] Firewall (nếu `ufw`): cho phép `8000/tcp` trên `tailscale0` hoặc tạm `allow 8000/tcp`

---

## Phase 2 — Windows client (mạng ngoài)

```bash
export ACP_API_URL=http://<UBUNTU_TS_IP>:8000
curl -v --connect-timeout 10 "$ACP_API_URL/health"
agentctl gov status
curl -s -X POST "$ACP_API_URL/policy/evaluate" ...
agentctl assign rust-gateway agent2 git_read --json
```

- [ ] 7-1 remote health → 200, rules **8**
- [ ] 7-2 gov status khớp Ubuntu
- [ ] 7-3 policy allow
- [ ] 7-4 assign + Ubuntu log thấy IP Tailscale Laptop (`100.x`)
- [ ] 7-5 (optional) `bash scripts/soak_staging.sh --log /tmp/acp-soak-remote.log`

---

## Phase 3 — Evidence

- [ ] [`RESULTS.md`](RESULTS.md)
- [ ] `artifacts/topology-tailscale.json`
- [ ] `artifacts/remote-health.json`
- [ ] `terminal-ubuntu-server.md`
- [ ] `terminal-windows-client-external.md`

---

## Sau Study 07

- Ghi nhận trong PB-9: remote operator path qua Tailscale
- Tùy chọn Study 06 follow-ups: round B full policy, drill `100.x` trên cùng LAN (đã cover ở Study 07)
