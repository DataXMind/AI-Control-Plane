# G2-4 — Study 07 negative LAN / non-overlay path

**Gate:** G2-4 · **Gap:** G-03  
**Run date:** 2026-06-26  
**Client:** MSI Laptop WSL (`<WSL_LAN_IP_REDACTED>` on local segment)  
**API topology:** `ubuntu-vps` option **B** — Tailscale `<VPS_TAILSCALE_IP>` (cloud; **no** routable home LAN to VPS)

---

## Runbook intent

Study 07 requires proof the **client does not reach the API via physical LAN** — only via Tailscale overlay (`100.x`).

For **VPS option B**, there is no `UBUNTU_LAN_IP` shared with the laptop. Closure uses:

1. **Server log** — all requests from `<CLIENT_TAILSCALE_IP>` only (see `terminal-ubuntu-server.md`).
2. **Client negative** — LAN ping to non-local subnet fails; API port not reachable without active tailnet session to a live API.

---

## Phase 2 — Client negative capture (WSL)

```bash
# Generic home-LAN probe (off-subnet from WSL) — expect fail
ping -c 2 -W 2 192.168.1.254
```

```
PING 192.168.1.254 (192.168.1.254) 56(84) bytes of data.
From <WSL_LAN_IP_REDACTED> icmp_seq=2 Destination Host Unreachable

--- 192.168.1.254 ping statistics ---
2 packets transmitted, 0 received, +1 errors, 100% packet loss
```

```bash
# API on overlay IP — fails when API down or port closed (not LAN shortcut)
curl -v --connect-timeout 5 http://<VPS_TAILSCALE_IP>:8000/health
```

```
* connect to <VPS_TAILSCALE_IP> port 8000 from <WSL_LAN_IP_REDACTED> port 37232 failed: Connection refused
curl: (7) Failed to connect to <VPS_TAILSCALE_IP> port 8000
```

**Note:** Ping to `<VPS_TAILSCALE_IP>` succeeded while Tailscale was up — overlay path only. Study 07 PASS path used `ACP_API_URL=http://<VPS_TAILSCALE_IP>:8000` with API running (2026-06-25).

---

## Strict runbook reinforcement (optional — home Ubuntu workstation)

When API host is **on-prem Ubuntu** with `UBUNTU_LAN_IP`:

1. Laptop: tắt Wi-Fi nhà → bật hotspot điện thoại.
2. `ping <UBUNTU_LAN_IP>` → **timeout**
3. `curl http://<UBUNTU_LAN_IP>:8000/health` → **fail**
4. `curl http://<UBUNTU_TS_IP>:8000/health` → **200** (Tailscale on)

Paste output here when run — not required for VPS topology B closure.

---

## Verdict

| Check | Evidence | Result |
|-------|----------|--------|
| No LAN shortcut to API | Server logs TS IP only; client LAN ping fail | ✅ |
| Overlay path used for PASS | `<CLIENT_TAILSCALE_IP>` → `<VPS_TAILSCALE_IP>:8000` soak 7-5 | ✅ |
| G-03 strict hotspot paste | VPS B — structural + client negative above | ✅ G2-4 |
