# Public Beta — Go / No-Go Assessment

**Document ID:** ACP-GOV-PB-GNG-001  
**Date:** 2026-06-24  
**Baseline:** `master` @ `638250c` (post G1 wave #91–#96)  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md)

---

## Verdict (2026-06-22 — post human approve)

| Question | Answer |
|----------|--------|
| **GO** — flip repository public now? | **NO** — PB-9 soak in progress |
| **GO** — start staging soak? | **STARTED** 2026-06-22 — [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) |
| **GO** — legal/trust artifacts in repo? | **YES** |
| **PB-11** | **Approved:** process-only until PB-12 public flip (API 403 unchanged) |

---

## Checklist — OPEN_SOURCE_READINESS §Go/No-Go

| Item | Status | Notes |
|------|--------|-------|
| Milestone B closed | ✅ | PR #51 |
| Production stable ≥30 days | ❌ | Soak not started — PB-10 |
| README + ARCHITECTURE + `examples/` ≤15 min | 🔄 | PB-7 runbook @ `practice-evidence/pb-7-clean-machine-fork/`; operator CLEAN verify pending |
| LICENSE, SECURITY, CONTRIBUTING, CoC | ✅ | PB-1..4 |
| OpenAPI published; CI green | 🔄 | PB-6 export script; publish on flip |
| `config/` no production secrets | ✅ | Shipped config is template-only |
| Maintainer + security contact in README | ✅ | Maintainer + SECURITY.md linked |
| Public beta `0.x` disclaimer | 🔄 | Pre-release notice in README; full on PB-12 |

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

**Decision (2026-06-22):** Maintainer approved **process-only** workflow until PB-12 public flip. Re-evaluate API enforcement when repo goes public or org upgrades to Team.

---

## Track PB-O — Soak plan

### Staging (PB-9) — target ≥14 days

| Day | Activity |
|-----|----------|
| 0 | Deploy `examples/minimal` stack; `ACP_DATA_DIR` + fixture or staging config |
| 1–14 | Simulated agent workload: policy eval, quota, MCP stub, `/apex/trigger` hourly |
| 14 | Review: SEV-1/2 count, p99 `/policy/evaluate`, disk growth on telemetry |

**Start criteria:** ✅ Maintainer approved 2026-06-22. Tracker: [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md).

**Clock:** Day 0 = 2026-06-22 · Target review = **2026-07-06**.

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
