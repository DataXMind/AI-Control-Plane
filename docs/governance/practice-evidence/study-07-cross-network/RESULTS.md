# Study 07 — Cross-network — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-07  
**Status:** **PASS**  
**Run date:** 2026-06-25  
**Operator:** dmin@MSI (WSL client) + `ubuntu-vps` (API)  
**Prerequisite:** Study 06 PASS  
**Topology doc:** [`TOPOLOGY_UBUNTU_TAILSCALE.md`](TOPOLOGY_UBUNTU_TAILSCALE.md)  
**Path used:** **Tailscale only** (`100.x.x.x`) — không LAN tới VPS

---

## Verdict

| Overall | Overlay-only? | CS-05 remote soak? | Blocks PB-9? |
|---------|---------------|-------------------|--------------|
| **PASS** | **Yes** — Ubuntu log chỉ `100.102.105.47` | **Yes** — 7-5 one iter | **No** |

---

## Topology (operator)

| Host | Role | Tailscale IP | Notes |
|------|------|--------------|-------|
| **ubuntu-vps** | API | `100.94.21.33` | Cloud Linux; `uvicorn 0.0.0.0:8000`; fixture config |
| **MSI Laptop (WSL)** | Client | `100.102.105.47` | `ACP_API_URL=http://100.94.21.33:8000` |
| Mac Mini M2 | **Không dùng** | `100.72.15.27` | Xem § [Vì sao không dùng Mac Mini](#vì-sao-không-dùng-mac-mini) |

**API host option:** Runbook option **B** (`ubuntu-vps`) — hợp lệ; VPS cloud vốn **không** cùng LAN nhà với Laptop.

---

## Test matrix

| ID | Test | Expected | Actual | Result |
|----|------|----------|--------|--------|
| 7-0 | Tailnet membership | Ubuntu + Laptop online | Requests từ `100.102.105.47` trên VPS | ✅ |
| 7-0n | Không đi LAN tới API | Client chỉ reach qua TS | Ubuntu log chỉ `100.102.105.47`; client LAN ping fail — `artifacts/terminal-7-0n-negative-lan.md` | ✅ |
| 7-1 | curl `/health` via TS | 200, rules **8** | rules **8** @ 11:17:48 | ✅ |
| 7-2 | `agentctl gov status` | rules **8** | rules **8** @ 11:17:57 | ✅ |
| 7-3 | policy evaluate | `allowed: true` | implicit trong assign; explicit soak policy **True** | ✅ |
| 7-4 | `agentctl assign` | `task_id` + TS IP in log | `6206697f-eab5-49c8-83e0-0dcf887d4999`; log `100.102.105.47` @ 11:18:10 | ✅ |
| 7-5 | `soak_staging.sh` remote | `soak_iter health=ok` | `health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok` @ 11:18:21 | ✅ |

---

## Giá trị theo terminal

### Ubuntu VPS — server

| Event | Detail |
|-------|--------|
| Config | `ACP_CONFIG_DIR=tests/fixtures/config` |
| Bind | `0.0.0.0:8000` |
| Client IP (all requests) | **`100.102.105.47`** (msi Tailscale) |
| Burst @ 11:17–11:18 | health ×4, governance, policy, tasks, soak (health, policy, quota, apex) |

### Laptop WSL — client

| Event | Detail |
|-------|--------|
| `ACP_API_URL` | `http://100.94.21.33:8000` |
| health | 200, rules **8** |
| assign | `6206697f-eab5-49c8-83e0-0dcf887d4999` |
| soak | one iteration PASS |

---

## Vì sao không dùng Mac Mini?

| Lý do | Giải thích |
|-------|------------|
| **Study 06 đã dùng Mac** | Mac Mini = LAN peer + API round B — không cần lặp vai trò tương tự |
| **Client phải là Laptop** | Study 07 mô phỏng **operator remote** (máy mang đi) — Mac cố định tại nhà |
| **API nên ổn định / cloud** | `ubuntu-vps` luôn online, IP Tailscale cố định — giống staging thật hơn Mac sleep/reboot |
| **Không thêm giá trị** | Mac client từ nhà → VPS qua TS hoạt động nhưng **không** test “laptop rời mạng nhà” |
| **Witness tùy chọn** | Mac có thể so sánh LAN vs TS sau này — không bắt buộc cho PASS |

**Khi nào thêm Mac:** Study 07b witness — Mac trên LAN nhà curl VPS LAN (fail) vs TS (ok) trong khi Laptop hotspot chỉ TS.

---

## Governance mapping

| Item | Evidence |
|------|----------|
| Invariant #4 remote CLI | Laptop → `100.94.21.33:8000` |
| CS-05 PB-9 staging soak | 7-5 remote `soak_staging.sh` |
| CS-06 policy path | policy allow + assign |
| Study 06 gap (6-5, TS drill) | Covered by 7-1..7-5 |

---

## Operator notes

1. Dùng **ubuntu-vps** thay workstation Ubuntu tại nhà — hợp lệ per runbook option B.
2. Toàn bộ VPS access log = Tailscale IP client — không lẫn LAN.
3. G2-4 closed — negative LAN artifact `artifacts/terminal-7-0n-negative-lan.md` (VPS topology B).
4. Soak remote một iteration đủ practice evidence; PB-9 calendar 14 ngày vẫn riêng.

---

## Artifacts

- [x] `artifacts/topology-tailscale.json`
- [x] `artifacts/remote-health.json`
- [x] `artifacts/remote-policy-assign.json`
- [x] `artifacts/remote-soak.json`
- [x] `terminal-ubuntu-server.md`
- [x] `terminal-windows-client-external.md`
- [x] `artifacts/terminal-7-0n-negative-lan.md` (G2-4)
