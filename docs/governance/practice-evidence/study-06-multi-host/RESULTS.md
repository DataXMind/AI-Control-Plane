# Study 06 — Multi-host — Results (template)

**Document ID:** ACP-GOV-PRACTICE-STUDY-06  
**Status:** PENDING  
**Topology:** _e.g. A=192.168.1.50 API, B=192.168.1.51 client_

| ID | Test | Machine | Expected | Actual | Result |
|----|------|---------|----------|--------|--------|
| 6-0 | git clone + pip install | A, B | both OK | | ☐ |
| 6-1 | curl health remote | B → A | 200, rules 8 | | ☐ |
| 6-2 | agentctl gov status | B | rules match A | | ☐ |
| 6-3 | policy evaluate | B → A | allowed true | | ☐ |
| 6-4 | agentctl assign | B → A | task_id + A logs B IP | | ☐ |
| 6-5 | soak_staging.sh | B → A | soak_iter ok | optional | ☐ |

## Machine A

| Key | Value |
|-----|--------|
| IP | |
| Bind | 0.0.0.0:8000 / Docker |
| Config | |

## Machine B

| Key | Value |
|-----|--------|
| IP | |
| ACP_API_URL | |
