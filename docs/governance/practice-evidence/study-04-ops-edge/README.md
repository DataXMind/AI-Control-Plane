# Study 04 — Ops edge cases (optional)

**Purpose:** Học có chủ đích các lỗi vận hành — không phải profile runtime mới.

| ID | Scenario | How to trigger | Expected learning |
|----|----------|----------------|-------------------|
| 4a | Port conflict | Start uvicorn :8000 twice | `Address already in use` |
| 4b | `ACP_API_URL` mismatch | API on 8002, curl :8000 | Wrong/stale data or connection error |
| 4c | Config without restart | Change `ACP_CONFIG_DIR` in T2 only | Server keeps old config until restart |

**Prerequisite:** Study 01–03 PASS (this track).

**Evidence:** Add `study-04-ops-edge/` after operator runs optional drills.

**Note:** Study 04 does **not** block PB-9 calendar soak or public repo flip.
