# Public Beta — Go / No-Go Assessment

**Document ID:** ACP-GOV-PB-GNG-001  
**Date:** 2026-06-24 (updated **2026-06-28** — practice gates sync)  
**Baseline:** `master` @ catalog v1.3.3 · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_SPRINT_PLAN.md`](PUBLIC_BETA_SPRINT_PLAN.md)

---

## Verdict (2026-07-06 — PB-12 GO)

| Question | Answer |
|----------|--------|
| **GO** — flip repository public now? | **YES** — PB-9 Day 14 PASS · pre-flip complete · [`pb-12-public-flip/RESULTS.md`](practice-evidence/pb-12-public-flip/RESULTS.md) |
| **GO** — start staging soak? | **COMPLETE** — [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) closed |
| **GO** — legal/trust artifacts in repo? | **YES** |
| **PB-10** | **DEFERRED GA** — 0.x beta ships without 30-day production soak |
| **PB-11** | Re-evaluate branch protection API post-public flip |

**Operator:** mobilexmind · **Date:** 2026-07-06

---

## Verdict (2026-06-22 — post human approve) — superseded

| Question | Answer |
|----------|--------|
| **GO** — flip repository public now? | ~~NO~~ → **YES @ 2026-07-06** |
| **GO** — start staging soak? | **STARTED** 2026-06-22 — [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) |
| **GO** — legal/trust artifacts in repo? | **YES** |
| **PB-11** | **Approved:** process-only until PB-12 public flip (API 403 unchanged) |

---

## Gate summary @ 2026-06-28 (practice vs catalog)

> **Drift guard:** Practice PASS below does **not** remove items from `GET /governance/status` → `public_beta.gates_remaining` until maintainer catalog bump @ PB-12 flip. Runtime may still show **7** gates.

| Gate | Practice evidence | Catalog @ flip | Evidence |
|------|-------------------|----------------|----------|
| PB-1..4 Legal | ✅ CLOSED | closed | PR #112–#113 |
| PB-5 `examples/minimal` | ✅ CLOSED | — | CI `examples-minimal-smoke` |
| PB-6 OpenAPI runtime | ✅ CLOSED | — | `verify_openapi_runtime.sh` |
| PB-6 static publish | 🔄 synced | listed | `export_openapi.py` → `docs/openapi/openapi.json` (no diff @ 2026-06-28 dry-run) |
| **PB-7** clean fork ≤15 min | ✅ **PASS** | listed | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) 2026-06-27 |
| **PB-8** `v0.1.0-rc.1` tag | ✅ **pushed early** | listed | Tag @ `c58b4cc` 2026-06-28 — **before** Day 14; accepted; **do not re-tag** |
| PB-9 staging soak ≥14d | 🔄 IN PROGRESS | listed | Ticks through 2026-06-28 · review ~07-06 |
| PB-10 production soak 30d | ❌ **DEFERRED GA** | listed | 0.x beta policy — explicit accept @ PB-12 |
| PB-11 branch protection | DEFERRED | — | Process-only (API 403) |
| **security@** live test | ✅ **PASS** | listed | [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) 2026-06-28 |
| PB-12 human go/no-go | ⏳ | listed | ~2026-07-10 post Day 14 PASS |

---

## Checklist — OPEN_SOURCE_READINESS §Go/No-Go

| Item | Status | Notes |
|------|--------|-------|
| Milestone B closed | ✅ | PR #51 |
| Production stable ≥30 days | ⏳ **Deferred for 0.x beta** | PB-10 — required for GA; see § PB-10 scope |
| README + ARCHITECTURE + `examples/` ≤15 min | ✅ | **PB-7 PASS** — [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) (CLEAN Ubuntu @ MSI 2026-06-27) |
| LICENSE, SECURITY, CONTRIBUTING, CoC | ✅ | PB-1..4 |
| OpenAPI published; CI green | 🔄 | Runtime ✅; static synced — `export_openapi.py` (commit on flip if diff) |
| `config/` no production secrets | ✅ | Shipped config is template-only |
| Maintainer + security contact in README | ✅ | Maintainer + SECURITY.md linked |
| security@ mailbox live test | ✅ | PASS 2026-06-28 — [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) |
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
**Evidence window:** first logged iteration **2026-06-26** — see [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) § clock vs evidence.  
**Machine logs:** MSI `PB9_SOAK_ITERATION_LOG.md` · VPS `pb-9-day14-review/artifacts/vps-soak-iteration.log` (CUR-04).

### Production (PB-10) — target ≥30 days

**PB-10 scope @ 0.x Public Beta (2026-06-27):** Production soak is a **GA (1.0.0) operational gate**, not a hard blocker for **0.x beta flip** if maintainer records explicit acceptance in PB-12 go/no-go. `gates_remaining` in catalog is unchanged until flip-time catalog update.

**PB-12 acceptance text (draft):** *AI Control Plane 0.1.0-beta ships without 30-day production soak. Operator-facing disclaimer: 0.x API may change; not recommended for production.*

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

## Pre-flip checklist (~07-07, post Day 14 PASS)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
python scripts/export_openapi.py
git diff docs/openapi/openapi.json   # commit only if changed
pytest tests/test_smoke.py -v -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

**Already done (do not repeat unless regression):**

| Step | Status | Note |
|------|--------|------|
| `git tag v0.1.0-rc.1` | ✅ @ `c58b4cc` 2026-06-28 | Pre-dated Day 14 — record in PB-12 decision; release `v0.1.0-beta.1` from tag @ flip |
| security@ live test | ✅ 2026-06-28 | [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) |
| PB-7 CLEAN fork | ✅ 2026-06-27 | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) |

**Reject:** `curl … > docs/openapi.json` — SSOT is `docs/openapi/openapi.json` via `scripts/export_openapi.py`.

**Templates:** [`PB9_DAY14_REVIEW_TEMPLATE.md`](PB9_DAY14_REVIEW_TEMPLATE.md) · [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md)

---

## PB-12 flip action (human, post Day 14 PASS)

- GitHub Settings → Change visibility → **Public**
- Enable GitHub Security Advisories · Dependabot alerts
- GitHub Release: **`v0.1.0-beta.1`** from existing `v0.1.0-rc.1` tag (or document if retagging)
- Release notes: **0.x disclaimer** — API may change; not for production

---

## Sign-off roles

| Role | PB-12 public flip |
|------|-------------------|
| Maintainer | Day 14 PASS + checklist ✅ |
| Security | SECURITY.md + security@ PASS acknowledged |
| Org admin | Branch protection or public-repo policy |

---

**Next review:** PB-9 Day 14 ~**2026-07-06** or material regression.
