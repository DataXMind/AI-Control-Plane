# Study 04 — Ops edge cases — Results (template)

**Document ID:** ACP-GOV-PRACTICE-STUDY-04  
**Status:** PENDING operator run  
**Run date:** _fill_  
**Prerequisite:** Study 01–03 PASS

---

## Verdict

| Overall | Blocks PB-9 / public repo? |
|---------|----------------------------|
| _PASS / FAIL_ | **No** — optional ops training |

---

## Test matrix

| ID | Drill | T1 | T2 | Expected | Actual | Result |
|----|-------|----|----|----------|--------|--------|
| 4a | Port conflict | uvicorn :8000 keep alive | 2nd uvicorn :8000 | errno 98 | | ☐ |
| 4a | | | curl health | 200, rules 8 | | ☐ |
| 4b | URL mismatch | uvicorn :8002 | curl `ACP_API_URL=:8000` | refuse/stale | | ☐ |
| 4b | | | curl `ACP_API_URL=:8002` | rules 8 | | ☐ |
| 4c | Config no restart | fixture uvicorn | unset env, curl | still rules 8 | | ☐ |
| 4c | | restart shipped | curl | rules 10, agents 4 | | ☐ |

---

## Operator notes

_Fill unexpected behavior, timestamps, PIDs._

---

## Artifacts checklist

- [ ] `artifacts/drill-4a-port-conflict.json`
- [ ] `artifacts/drill-4b-url-mismatch.json`
- [ ] `artifacts/drill-4c-config-restart.json`
