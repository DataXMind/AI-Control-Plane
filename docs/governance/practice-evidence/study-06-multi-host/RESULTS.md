# Study 06 — Multi-host — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-06  
**Status:** **PASS** (bidirectional LAN, full suite both rounds)  
**Run date:** 2026-06-25  
**Operator:** dmin@MSI (WSL) + dataxmind@DataXMinds-Mac-mini  
**Prerequisite:** Study 05 PASS  
**Topology doc:** [`TOPOLOGY_WINDOWS_MAC.md`](TOPOLOGY_WINDOWS_MAC.md)  
**Source logs:** operator paste 2026-06-25; terminal captures in-repo below

---

## Verdict

| Overall | Bidirectional? | Full 6-1..6-4 both rounds? | Ready for Study 07? |
|---------|----------------|------------------------------|-------------------|
| **PASS** | **Yes** — 2 rounds LAN | **Yes** (round B completed @ 17:34) | **Yes** |

---

## Topology (operator)

| Host | Role(s) | LAN IP | Tailscale | Notes |
|------|---------|--------|-----------|-------|
| **MSI Laptop** | API (round A) + client (round B) | `<LAN_IP_REDACTED>` (Wi-Fi) | `<CLIENT_TAILSCALE_IP>` | WSL `<WSL_LAN_IP_REDACTED>`; portproxy round A only |
| **Mac Mini M2** | client (round A) + API (round B) | `192.168.1.99` (`en0`) | `<MAC_TAILSCALE_IP>` | Native macOS uvicorn — no portproxy |

**Đường test:** **LAN** `192.168.1.0/24`. Tailscale up; drill chính dùng LAN IP.

---

## Round A — Laptop API → Mac client

| ID | Test | Client | Expected | Actual | Result |
|----|------|--------|----------|--------|--------|
| 6-0 | clone + pip | both | OK | repo + `.venv` | ✅ |
| 6-1 | curl `/health` remote | Mac → `<LAN_IP_REDACTED>:8000` | 200, rules **8** | HTTP 200; rules **8** | ✅ |
| 6-2 | `agentctl gov status` | Mac | rules **8** | rules **8**; PB-9 IN_PROGRESS | ✅ |
| 6-3 | `POST /policy/evaluate` | Mac → A | `allowed: true` | `allowed: true`, 4.17 ms | ✅ |
| 6-4 | `agentctl assign` | Mac → A | `task_id` + A logs | `03c332db-645a-481f-834f-6b9420fb9375`; WSL `192.168.16.1` @ 16:59:55 | ✅ |

---

## Round B — Mac API → Laptop client (full suite)

| ID | Test | Client | Expected | Actual | Result |
|----|------|--------|----------|--------|--------|
| 6-1 | remote reachability | WSL → `192.168.1.99:8000` | API up | gov @ 17:03:54; policy @ 17:34:35 | ✅ |
| 6-2 | `agentctl gov status` | WSL | rules **8** | rules **8**; milestones khớp | ✅ |
| 6-3 | policy evaluate | WSL → Mac | `allowed: true` | `allowed: true`, latency **1.47 ms** | ✅ |
| 6-4 | assign | WSL → Mac | `task_id` + Mac log `<LAN_IP_REDACTED>` | `ae6c13a4-0281-4321-b6fc-95a9e37ff777`; Mac log `<LAN_IP_REDACTED>` @ 17:34:39 | ✅ |

Mac server log round B: `GET /governance/status`, `POST /policy/evaluate` ×2, `POST /tasks` từ **`<LAN_IP_REDACTED>`** — IP LAN Laptop trực tiếp (native macOS API).

---

## Test matrix (tổng hợp)

| ID | Drill | Direction | Result |
|----|-------|-----------|--------|
| 6-0 | Setup both hosts | A + B | ✅ |
| 6-1 | Remote health | A + B | ✅ |
| 6-2 | Gov status | A + B | ✅ |
| 6-3 | Policy allow | A + B | ✅ |
| 6-4 | Assign + server log | A + B | ✅ |
| 6-5 | `soak_staging.sh` remote LAN | — | ⏭️ optional (Study 07 cover qua TS) |

---

## Giá trị theo terminal

### Round B supplement (@ 17:34)

| Host | Event |
|------|-------|
| Mac API | `POST /policy/evaluate` 200; `POST /tasks` 200 from `<LAN_IP_REDACTED>:59576` / `:59592` |
| Laptop client | `allowed: true`; assign `ae6c13a4-0281-4321-b6fc-95a9e37ff777` |

(Xem terminal captures đầy đủ trong `terminal-direction-b-*.md`.)

---

## Operator notes

1. Round A: portproxy Admin bắt buộc; WSL log client = `192.168.16.1` (NAT).
2. Round B: Mac native API → log client = `<LAN_IP_REDACTED>` (LAN trực tiếp).
3. Round B full policy + assign hoàn tất sau lần ghi evidence đầu — cập nhật 2026-06-25 @ 17:34.

---

## Governance mapping

| Invariant / CS | Evidence |
|----------------|----------|
| Invariant #4 — CLI HTTP-only | Round A + B đầy đủ |
| CS-06 policy path | 6-3 both rounds |
| L3 multi-host ops | portproxy (A) + native bind (B) |

---

## Next

→ [**Study 07 — Cross-network**](../study-07-cross-network/RESULTS.md) **PASS**

---

## Artifacts

- [x] `artifacts/topology-lan.json`
- [x] `artifacts/direction-a-health-remote.json`
- [x] `artifacts/direction-a-policy-assign.json`
- [x] `artifacts/direction-b-remote-gov.json`
- [x] `artifacts/direction-b-policy-assign.json`
- [x] `terminal-direction-a-laptop-server.md`
- [x] `terminal-direction-a-mac-client.md`
- [x] `terminal-direction-b-mac-server.md`
- [x] `terminal-direction-b-laptop-client.md`
