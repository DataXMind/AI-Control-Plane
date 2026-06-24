# Public Beta — Go / No-Go Assessment

**Document ID:** ACP-GOV-PB-GNG-001  
**Date:** 2026-06-24  
**Baseline:** `master` @ `de931b5`  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md)

---

## Verdict (today)

| Question | Answer |
|----------|--------|
| **GO** — flip repository public now? | **NO** |
| **GO** — start staging soak? | **YES** (after human confirms PB-5 deploy path) |
| **GO** — legal/trust artifacts in repo? | **YES** (PB-1..4 delivered this sprint prep) |

---

## Checklist — OPEN_SOURCE_READINESS §Go/No-Go

| Item | Status | Notes |
|------|--------|-------|
| Milestone B closed | ✅ | PR #51 |
| Production stable ≥30 days | ❌ | Soak not started — PB-10 |
| README + ARCHITECTURE + `examples/` ≤15 min | 🔄 | PB-5 added; human PB-7 verify |
| LICENSE, SECURITY, CONTRIBUTING, CoC | ✅ | PB-1..4 |
| OpenAPI published; CI green | 🔄 | PB-6 export script; publish on flip |
| `config/` no production secrets | ✅ | Shipped config is template-only |
| Maintainer + security contact in README | 🔄 | Add on PB-12 prep |
| Public beta `0.x` disclaimer | 🔄 | README section on flip |

---

## Track PB-P — Branch protection API

**Probe (2026-06-24):**

```bash
gh api repos/DataXMind/AI-Control-Plane/branches/master/protection
```

**Result:** HTTP **403** — *"Upgrade to GitHub Pro or make this repository public to enable this feature."*

| Option | Effect on PB-11 |
|--------|-----------------|
| GitHub Team on private org | Run `scripts/setup_github_milestones_and_protection.sh --protection-only` |
| Flip public (PB-12) | Protection API may become available on public repo |
| Process-only (current) | [`BRANCH_PROTECTION.md`](BRANCH_PROTECTION.md) team workflow |

**Decision:** PB-11 **blocked on platform** until Team upgrade **or** public flip. CI + PR convention remains mandatory.

---

## Track PB-O — Soak plan

### Staging (PB-9) — target ≥14 days

| Day | Activity |
|-----|----------|
| 0 | Deploy `examples/minimal` stack; `ACP_DATA_DIR` + fixture or staging config |
| 1–14 | Simulated agent workload: policy eval, quota, MCP stub, `/apex/trigger` hourly |
| 14 | Review: SEV-1/2 count, p99 `/policy/evaluate`, disk growth on telemetry |

**Start criteria:** PB-5 green locally; maintainer signs soak start in issue comment.

### Production (PB-10) — target ≥30 days

After staging pass: same SLO targets on production-like config (`config/` not fixtures).

| SLO (example) | Target |
|-----------------|--------|
| `POST /policy/evaluate` p99 | < 500 ms |
| Availability | ≥ 99.5% |
| SEV-1 from control plane | 0 |

---

## Track PB-L — Legal (parallel, done in prep)

Artifacts at repo root — see sprint plan PB-1..4.

---

## Sign-off roles

| Role | PB-12 public flip |
|------|-------------------|
| Maintainer | All checklist ✅ + soak complete |
| Security | SECURITY.md process acknowledged |
| Org admin | Branch protection or public-repo policy |

---

**Next review:** After PB-9 day 14 or material regression.
