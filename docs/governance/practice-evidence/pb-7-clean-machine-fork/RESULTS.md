# PB-7 — Clean-machine fork — Results

> **REMINDER:** WSL `dmin@MSI` @ `/mnt/d/Projects/ai-control-plane` = **WARM** — see [`artifacts/warm-fork-user-msi-2026-06-27.md`](artifacts/warm-fork-user-msi-2026-06-27.md). This PASS is **Ubuntu `ubuntu@MSI`** @ `/mnt/d/DataXMind/Projects/AI-Control-Plane`.

**Document ID:** ACP-GOV-PRACTICE-PB7-RESULTS  
**Status:** **PASS**  
**Run date:** 2026-06-27  
**Operator:** ubuntu@MSI  
**Path:** **A — Docker Compose**

---

## Verdict

| Overall | ≤15 min? | Blocks PB-12? |
|---------|----------|---------------|
| **PASS** | ✅ (~3–6 min active steps post-clone) | **No** — evidence recorded; catalog gate update @ maintainer flip |

---

## Test matrix

| ID | Step | Expected | Actual | Elapsed | Result |
|----|------|----------|--------|---------|--------|
| PB7-1 | `git clone` | Repo on disk | `/mnt/d/DataXMind/Projects/AI-Control-Plane` | T0 | ✅ |
| PB7-2 | Stack start | Container healthy | `minimal-acp-api-1` Built ~54s, Started | ~1 min | ✅ |
| PB7-3 | `GET /health` | `ok`, rules > 0 | 8 rules, 3 agents | < 2 min | ✅ |
| PB7-4 | Policy allow | `allowed: true` | `action permitted` | < 3 min | ✅ |
| PB7-4b | Policy deny | `allowed: false` | `unknown agent or role` | < 3 min | ✅ |
| PB7-5 | Total time | ≤ 15 min | ≤ 15 min | — | ✅ |
| PB7-6 | Governance verify | v1.3.3 · 13 patterns | PASS after CRLF fix | < 5 min | ✅ |
| PB7-7 | agentctl (optional) | task created | `2e395f6a-…` PENDING | < 6 min | ✅ |

---

## Machine profile

| Field | Value |
|-------|-------|
| Label | **CLEAN** (Ubuntu user; MSI hardware caveat) |
| OS | Ubuntu @ MSI |
| `master` SHA | `082c5f9` (reconcile @ clone) |
| Docker | Compose v2 · `minimal-acp-api` |

See [`artifacts/machine-profile.md`](artifacts/machine-profile.md).

---

## Artifacts

- [x] [`artifacts/timing.md`](artifacts/timing.md)
- [x] [`artifacts/health.json`](artifacts/health.json)
- [x] [`artifacts/policy-allow.json`](artifacts/policy-allow.json)
- [x] [`artifacts/machine-profile.md`](artifacts/machine-profile.md)
- [x] [`artifacts/clean-ubuntu-msi-2026-06-27.md`](artifacts/clean-ubuntu-msi-2026-06-27.md)

---

## Notes

- First `verify_governance_status_runtime.sh` failed: CRLF on scripts when repo on `/mnt/d` — fixed with `sed -i 's/\r$//'`.
- `agentctl` on host N/A without `pip install`; used `docker exec minimal-acp-api-1 agentctl …` — valid for Path A.
- Does not close `gates_remaining` in `governance_catalog.py` until maintainer catalog bump — runtime may still list PB-7 until then.
