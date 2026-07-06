# Study 07 — Cross-network — Checklist

**Document ID:** ACP-GOV-PRACTICE-STUDY-07-CHECKLIST  
**Status:** **PASS** — 2026-06-25  
**Topology:** [`TOPOLOGY_UBUNTU_TAILSCALE.md`](TOPOLOGY_UBUNTU_TAILSCALE.md)  
**Runbook:** [`RUNBOOK.md`](RUNBOOK.md)

---

## Điều kiện topology

| Host | Vai trò | Thực tế operator |
|------|---------|------------------|
| **ubuntu-vps** | API | `<VPS_TAILSCALE_IP>` (cloud — option B) |
| **Laptop Windows** | Client | `<CLIENT_TAILSCALE_IP>`; `ACP_API_URL=http://<VPS_TAILSCALE_IP>:8000` |
| Mac Mini | Không dùng | Study 06 đã cover; xem RESULTS § Mac |

- [x] Study 06 PASS
- [x] Ubuntu + Windows cùng tailnet
- [x] Ubuntu log chỉ `<CLIENT_TAILSCALE_IP>` (overlay-only)
- [x] curl health via TS → 200, rules **8**

---

## Phase 1 — Ubuntu API

- [x] `uvicorn 0.0.0.0:8000` + fixture config
- [x] Local health rules **8**

---

## Phase 2 — Windows client

- [x] 7-1 health via TS
- [x] 7-2 gov status rules **8**
- [x] 7-3 policy allow (assign + soak)
- [x] 7-4 assign `6206697f-eab5-49c8-83e0-0dcf887d4999`
- [x] 7-5 `soak_staging.sh` → `health=ok policy_allowed=True apex=ok`

---

## Phase 3 — Evidence

- [x] [`RESULTS.md`](RESULTS.md)
- [x] `artifacts/topology-tailscale.json`
- [x] `artifacts/remote-health.json`
- [x] `artifacts/remote-policy-assign.json`
- [x] `artifacts/remote-soak.json`
- [x] `terminal-ubuntu-server.md`
- [x] `terminal-windows-client-external.md`
