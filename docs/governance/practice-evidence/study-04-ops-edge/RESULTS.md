# Study 04 — Ops edge cases — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-04  
**Status:** **PASS**  
**Run date:** 2026-06-25  
**Operator:** dmin@MSI (WSL)  
**Mode:** Continuous run 4a → 4b → 4c on 2 terminals  
**Prerequisite:** Study 01–03 PASS  
**Source logs:** `TestCase/Study04/terminal1-cs04.md`, `terminal2-cs04.md`

---

## Verdict

| Overall | Ready for Study 05? | Blocks PB-9 / public repo? |
|---------|---------------------|----------------------------|
| **PASS** | **Yes** | **No** — optional ops training |

---

## Test matrix

| ID | Drill | Terminal | Expected | Actual | Result |
|----|-------|----------|----------|--------|--------|
| 4a | Port conflict | T2 | 2nd uvicorn `:8000` → errno 98 | `ERROR: [Errno 98] Address already in use` | ✅ |
| 4a | Health via server A | T2 | curl `:8000` → rules 8 | `policy_rules_count: 8`, agents 3 | ✅ |
| 4a | Server A | T1 | uvicorn fixture `:8000` | PID 6549, health 200 @ 14:05:01 | ✅ |
| 4b | API down / wrong URL | T2 | curl `:8000` when no listener | `Expecting value: line 1` (empty/refused) | ✅ |
| 4b | CLI fail-closed | T2 | `agentctl gov` API down | `ConnectError` → `RuntimeError: governance status unavailable` | ✅ |
| 4b | Correct URL | T1 | uvicorn `:8002` | PID 6610, health + governance 200 | ✅ |
| 4b | Correct URL | T2 | `ACP_API_URL=:8002` | curl rules 8; gov status rules 8 | ✅ |
| 4c | Baseline fixture | T2 | rules 8, agents 3 | `rules 8 agents 3` @ 14:08–14:09 | ✅ |
| 4c | Env change no restart | T2 | `unset ACP_CONFIG_DIR`, no T1 restart | still `rules 8 agents 3`; gov rules 8 | ✅ |
| 4c | Restart shipped | T1 | `unset ACP_CONFIG_DIR`, uvicorn `:8000` | PID 6676, health 200 @ 14:10:11 | ✅ |
| 4c | After restart | T2 | rules 10, agents 4 | `rules 10 agents 4` | ✅ |

---

## Giá trị theo terminal

### Terminal 1 — server lifecycle

| Phase | Config | Port | Worker PID | Key events |
|-------|--------|------|------------|------------|
| Pre-clean | — | — | — | port 8000 free |
| **4a** | `ACP_CONFIG_DIR=fixtures` | 8000 | 6549 | `GET /health` 200 @ 14:05:01 → Ctrl+C |
| **4b** | fixtures | **8002** | 6610 | health 14:07:08; governance 14:07:19 → Ctrl+C |
| **4c** (fixture) | fixtures | 8000 | 6649 | health 14:08:35, 14:09:00; governance 14:09:05 → Ctrl+C |
| **4c** (shipped) | **unset** | 8000 | 6676 | health 200 @ 14:10:11 → Ctrl+C |

### Terminal 2 — client observations

| Phase | `ACP_API_URL` | Shell `ACP_CONFIG_DIR` | Outcome |
|-------|---------------|------------------------|---------|
| **4a** | `:8000` | fixtures | curl health → rules **8** |
| **4b** (gap) | `:8000` | fixtures | API down → curl JSON error; agentctl **fail-closed** |
| **4b** | `:8002` | fixtures | curl rules **8**; gov status rules **8** |
| **4c** before restart | `:8000` | unset (T2 only) | still rules **8**, agents **3** |
| **4c** after T1 restart | `:8000` | unset | rules **10**, agents **4** |

---

## Operator notes (continuous run)

1. **4a→4b gap:** Sau `Ctrl+C` T1 (4a), T2 thử `curl`/`agentctl` `:8000` khi chưa có listener — đúng bài học **API down / wrong endpoint** (mạnh hơn stale zombie).
2. **4b ideal extra (optional):** Chưa ghi nhận curl `:8000` **trong lúc** T1 chạy `:8002` (stale instance trên 8000). Không fail study — có thể lặp trong Study 05 drill 5a.
3. **4c:** Chứng minh rõ `ACP_CONFIG_DIR` trên T2 **không** đổi runtime server; restart T1 với shipped → **10 rules / 4 agents**.

---

## Governance mapping

| Lesson | Evidence |
|--------|----------|
| Port isolation (L3 ops) | 4a errno 98 |
| `ACP_API_URL` must match (Invariant #4) | 4b :8002 OK; :8000 down → CLI error |
| Config at startup | 4c 8→8→10 only after T1 restart |

---

## Next step

→ [**Study 05 — Advanced surprises**](../study-05-advanced-surprises/RUNBOOK.md)

**Suggested first drills:** 5a (API down — đã thấy sơ bộ ở 4b gap), 5b (policy deny), 5c (422 validation).

---

## Artifacts

- [x] `artifacts/drill-4a-port-conflict.json`
- [x] `artifacts/drill-4b-url-mismatch.json`
- [x] `artifacts/drill-4c-config-restart.json`
