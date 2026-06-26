# Study 05 — Advanced surprises — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-05  
**Status:** **PASS** (7/7 drills; 5e G2-2 @ 2026-06-26)  
**Run date:** 2026-06-25  
**Operator:** dmin@MSI (WSL)  
**Prerequisite:** Study 04 PASS  
**Source logs:** `TestCase/Study05/terminal01-cs05.md`, `terminal02-cs05.md`

---

## Verdict

| Overall | Ready for Study 06? | Blocks PB-9? |
|---------|-------------------|--------------|
| **PASS** (7/7 drills) | **Yes** — cần **máy thứ 2** hoặc VM cùng LAN | **No** |

---

## Test matrix

| ID | Drill | Expected | Actual | Result |
|----|-------|----------|--------|--------|
| 5a | API down + `agentctl gov` | connection / runtime error | `RuntimeError: governance status unavailable` | ✅ |
| 5a | API down + `agentctl assign` | no local task | `policy service unavailable` | ✅ |
| 5b | Policy allow path | `allowed: true` | agent1+git_read → permitted | ✅ |
| 5b | Policy deny reviewer push | `allowed: false` + reason | `git_push denied for role reviewer`, `rbac-reviewer` | ✅ |
| 5c | Invalid body (`agent_id` only) | reject, no default-allow | `allowed: false`, validation in reason; T1 **HTTP 503** | ✅† |
| 5d | Docker holds :8000 | uvicorn errno 98 | `Address already in use` | ✅ |
| 5d | Stable rules under Docker | rules constant | curl ×3 → **8, 8, 8** | ✅ |
| 5e | Docker rebuild / version | detect stale vs fresh | `governance_version` **1.2** → **1.2.1** after src bump + rebuild (05e-r G2-2) | ✅ |
| 5f | Bad JWT `identity/verify` | reject | `allowed: false`, `invalid request`; T1 **HTTP 503** | ✅ |
| 5g | Kill switch | deny all if active | `allowed: false`, `kill_switch_active: study-05-drill-5g-g2` | ✅ |

† Runbook ghi HTTP 422; ACP thực tế **503 + fail-closed body** trên `/policy/evaluate` — đúng thiết kế server.

---

## Giá trị theo terminal

### Terminal 1

| Drill | Events |
|-------|--------|
| 5b–5c | uvicorn PID **6937**; policy evaluate 200 ×2; evaluate **503** @ 14:26:29 (invalid body) |
| 5d–5e | `docker compose up -d --build`; health **rules 8**; governance_version **1.0** (×2 rebuild) |
| 5f | uvicorn PID **7345**; `POST /identity/verify` **503** @ 14:32:31 |

### Terminal 2

| Drill | Key output |
|-------|------------|
| 5a | `agentctl gov status` ConnectError; `assign` → policy service unavailable |
| 5b | allow: agent1/git_read; deny: agent3/git_push |
| 5c | `allowed: false`, missing `project_id` / `tool_name` in reason |
| 5d | uvicorn conflict; rules **8** stable ×3 |
| 5f | identity verify `allowed: false`, `invalid request` |

---

## Operator notes

1. **5c / 5f:** Fail-closed trả **503** + JSON (không phải 422 thuần FastAPI) — cập nhật kỳ vọng runbook sau merge.
2. **5e:** Chưa sửa `governance_catalog.py` nên version không đổi — drill chưa chứng minh stale image; lặp lại khi cần PB-9 hardening.
3. **5g:** G2-1 PASS — artifact `artifacts/terminal-5g-g2-killswitch.md` (ephemeral config; không commit `policies.yml`).

---

## Governance mapping

| CS / invariant | Drill |
|----------------|-------|
| CS-06 fail-closed | 5a, 5c, 5f |
| RBAC deny | 5b |
| PB-9 Docker ops | 5d, 5e (partial) |

---

## Next — Study 06

Xem [`study-06-multi-host/RUNBOOK.md`](../study-06-multi-host/RUNBOOK.md) và **CHECKLIST.md** (mới).

**Điều kiện tối thiểu:**

1. Máy A + máy B cùng LAN (hoặc laptop + phone curl, hoặc VM thứ 2).
2. Máy A: `uvicorn --host 0.0.0.0 --port 8000` (không `127.0.0.1`).
3. Máy B: `ACP_API_URL=http://<IP-A>:8000`.
4. Firewall mở TCP 8000 trên A.

**Nếu chỉ có 1 máy vật lý:** dùng VM (Hyper-V/WSL2 bridged) hoặc tạm bind `0.0.0.0` và test từ thiết bị khác trên Wi-Fi.

---

## Artifacts

- [x] `artifacts/drill-5a-api-down.json`
- [x] `artifacts/drill-5b-policy-deny.json`
- [x] `artifacts/drill-5c-validation.json`
- [x] `artifacts/drill-5d-docker-conflict.json`
- [x] `artifacts/drill-5e-docker-version.json`
- [x] `artifacts/drill-5f-identity-bad-token.json`
- [x] `artifacts/terminal-5g-g2-killswitch.md` (G2-1)
- [x] `artifacts/terminal-5e-r-g2-docker.md` (G2-2)
