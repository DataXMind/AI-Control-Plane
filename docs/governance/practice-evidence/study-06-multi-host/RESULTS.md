# Study 06 — Multi-host — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-06  
**Status:** **PASS** (bidirectional LAN)  
**Run date:** 2026-06-25  
**Operator:** dmin@MSI (WSL) + dataxmind@DataXMinds-Mac-mini  
**Prerequisite:** Study 05 PASS  
**Topology doc:** [`TOPOLOGY_WINDOWS_MAC.md`](TOPOLOGY_WINDOWS_MAC.md)  
**Source logs:** operator paste 2026-06-25; terminal captures in-repo below

---

## Verdict

| Overall | Bidirectional? | Ready for PB-9 / public repo? | Blocks PB-9? |
|---------|----------------|-------------------------------|--------------|
| **PASS** | **Yes** — 2 rounds LAN | **Yes** — multi-host invariant #4 proven | **No** |

---

## Topology (operator)

| Host | Role(s) | LAN IP | Tailscale | Notes |
|------|---------|--------|-----------|-------|
| **MSI Laptop** | API (round 1) + client (round 2) | `192.168.1.59` (Wi-Fi) | `100.102.105.47` | WSL `192.168.21.3`; portproxy `0.0.0.0:8000` → WSL (Admin) |
| **Mac Mini M2** | client (round 1) + API (round 2) | `192.168.1.99` (`en0`) | `100.72.15.27` | Native macOS uvicorn round 2 — no portproxy |

**Đường test thực tế:** **LAN** `192.168.1.0/24` (ping Mac→Win OK). Tailscale up trên cả hai; không dùng `100.x` cho drill chính.

---

## Round A — Laptop API → Mac client (Plan A + portproxy)

| ID | Test | Client | Expected | Actual | Result |
|----|------|--------|----------|--------|--------|
| 6-0 | clone + pip | both | OK | repo + `.venv` trên cả hai máy | ✅ |
| 6-1 | curl `/health` remote | Mac → `192.168.1.59:8000` | 200, rules **8** | HTTP 200; `policy_rules_count: 8` | ✅ |
| 6-2 | `agentctl gov status` | Mac | rules **8**, milestones | Framework 6-layer; rules **8**; PB-9 IN_PROGRESS | ✅ |
| 6-3 | `POST /policy/evaluate` | Mac → A | `allowed: true` | `allowed: true`, latency 4.17 ms | ✅ |
| 6-4 | `agentctl assign` | Mac → A | `task_id` + A logs remote | `03c332db-645a-481f-834f-6b9420fb9375`; WSL log `192.168.16.1` ×5 @ 16:59:55 | ✅ |

**Server log (WSL):** Remote requests hiện source `192.168.16.1` (Windows host NAT qua portproxy), không phải `192.168.1.99` trực tiếp — **bình thường** với WSL2 + `netsh portproxy`.

**Windows Admin:** `portproxy` `0.0.0.0:8000` → `192.168.21.3:8000`; firewall `ACP-Study06-TCP8000`; `curl.exe http://192.168.1.59:8000/health` → rules **8**. Đã xóa portproxy sau round A.

---

## Round B — Mac API → Laptop client (Plan B / đảo vai)

| ID | Test | Client | Expected | Actual | Result |
|----|------|--------|----------|--------|--------|
| 6-1† | remote reachability | WSL → `192.168.1.99:8000` | API up | `agentctl gov status` thành công (HTTP tới Mac) | ✅ |
| 6-2 | `agentctl gov status` | WSL | rules **8** khớp Mac API | rules **8**; milestones khớp round A | ✅ |
| 6-3 | policy evaluate | WSL → Mac | — | **không ghi** trong operator paste | ⏭️ |
| 6-4 | assign | WSL → Mac | — | **không ghi** trong operator paste | ⏭️ |

† Round B chứng minh **chiều ngược** qua CLI governance; Mac server log: `GET /governance/status` từ **`192.168.1.59`** @ 17:03:54 — IP LAN Laptop hiện trực tiếp (macOS bind native, không qua WSL NAT).

**Kết luận round B:** Đủ cho invariant **remote HTTP / `ACP_API_URL` trên host thứ 2**; full 6-3/6-4 lặp lại trên round B là tùy chọn (round A đã cover policy + assign).

---

## Test matrix (tổng hợp)

| ID | Drill | Direction | Result |
|----|-------|-----------|--------|
| 6-0 | Setup both hosts | A + B | ✅ |
| 6-1 | Remote health | A (Mac client) | ✅ |
| 6-2 | Gov status match | A + B | ✅ |
| 6-3 | Policy allow | A (Mac client) | ✅ |
| 6-4 | Assign + server log | A (Mac client) | ✅ |
| 6-5 | `soak_staging.sh` remote | — | ⏭️ optional (không chạy) |

---

## Giá trị theo terminal

### Direction A — Laptop server (WSL)

| Event | Detail |
|-------|--------|
| Config | `ACP_CONFIG_DIR=tests/fixtures/config` |
| Bind | `0.0.0.0:8000` |
| Local smoke | rules **8** @ 15:14–15:15 |
| Remote burst | `GET /health`, `GET /governance/status`, `POST /policy/evaluate` ×2, `POST /tasks` @ **16:59:55** from `192.168.16.1` |
| Shutdown | Ctrl+C sau round A |

### Direction A — Mac client

| Event | Detail |
|-------|--------|
| `ACP_API_URL` | `http://192.168.1.59:8000` |
| Ping Win | `192.168.1.59` 0% loss (avg ~25 ms) |
| assign | `task_id` `03c332db-645a-481f-834f-6b9420fb9375`, state `PENDING` |

### Direction B — Mac server (native)

| Event | Detail |
|-------|--------|
| Config | `ACP_CONFIG_DIR=tests/fixtures/config` |
| Bind | `0.0.0.0:8000` |
| Remote | `GET /governance/status` 200 from **`192.168.1.59:59566`** @ 17:03:54 |

### Direction B — Laptop client (WSL)

| Event | Detail |
|-------|--------|
| `ACP_API_URL` | `http://192.168.1.99:8000` |
| `agentctl gov status` | rules **8**, PB-9 case studies listed |

---

## Operator notes

1. **Portproxy bắt buộc Admin** — PowerShell thường fail `requires elevation`; round A chỉ PASS sau Admin + firewall rule.
2. **Sai IP đầu tiên:** Mac ping `192.168.21.3` (WSL) → timeout; đúng là ping / curl **`192.168.1.59`** (Windows Wi-Fi).
3. **WSL log IP:** Client qua portproxy → `192.168.16.1`; Mac native API → log **`192.168.1.59`** — dùng để phân biệt đường WSL vs macOS.
4. **Tailscale:** `tailscale up` trên Mac trước khi test; drill chính dùng LAN (ổn định, latency ~2–3 ms sau warmup).
5. **Dọn:** `netsh interface portproxy delete` port 8000 sau study (đã thực hiện).

---

## Governance mapping

| Invariant / CS | Evidence |
|----------------|----------|
| Invariant #4 — CLI HTTP-only, `ACP_API_URL` | Round A + B |
| CS-05 PB-9 staging path | `gov status` → soak_staging hint |
| CS-06 fail-closed path | Round A policy allow (positive path remote) |
| L3 multi-host ops | WSL portproxy + bidirectional roles |

---

## Next

- [**Study 07 — Cross-network**](../study-07-cross-network/RUNBOOK.md): Ubuntu API + Laptop mạng ngoài qua Tailscale
- PB-9 calendar soak tiếp tục (Study 06 ≠ đóng PB-9)
- Tùy chọn trên Study 06: round B full 6-3/6-4 — hoặc cover qua Study 07

---

## Artifacts

- [x] `artifacts/topology-lan.json`
- [x] `artifacts/direction-a-health-remote.json`
- [x] `artifacts/direction-a-policy-assign.json`
- [x] `artifacts/direction-b-remote-gov.json`
- [x] `terminal-direction-a-laptop-server.md`
- [x] `terminal-direction-a-mac-client.md`
- [x] `terminal-direction-b-mac-server.md`
- [x] `terminal-direction-b-laptop-client.md`
