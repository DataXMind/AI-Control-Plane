# PB-7 — Clean-machine fork — Results

> **REMINDER — CLEAN machine required:** MSI WSL = **WARM** (does not count). Use a **separate laptop/VM** with no prior `AI-Control-Plane` clone, no Docker `minimal-acp-api-1`, no `.venv`. Target ≤15 min — [`RUNBOOK.md`](RUNBOOK.md).

**Document ID:** ACP-GOV-PRACTICE-PB7-RESULTS  
**Status:** **PAUSED** — operator will run on separate laptop  
**Run date:** —  
**Operator:** —  
**Path:** — (A Docker / B native)

---

## Verdict

| Overall | ≤15 min? | Blocks PB-12? |
|---------|----------|---------------|
| **PENDING** | — | Yes until PASS |

---

## Test matrix

| ID | Step | Expected | Actual | Elapsed | Result |
|----|------|----------|--------|---------|--------|
| PB7-1 | `git clone` | Repo on disk | — | — | ☐ |
| PB7-2 | Stack start | Container healthy / uvicorn up | — | — | ☐ |
| PB7-3 | `GET /health` | `ok`, rules > 0 | — | — | ☐ |
| PB7-4 | Policy allow | `allowed: true` | — | — | ☐ |
| PB7-5 | Total time | ≤ 15 min | — | — | ☐ |

---

## Machine profile

| Field | Value |
|-------|-------|
| Label | CLEAN / WARM |
| OS | |
| `master` SHA | |
| Docker version | |

---

## Artifacts

- [ ] `artifacts/timing.md`
- [ ] `artifacts/health.json`
- [ ] `artifacts/policy-allow.json`
- [ ] `artifacts/machine-profile.md`

---

## Notes

_(Operator: blockers, network slow pull, etc.)_
