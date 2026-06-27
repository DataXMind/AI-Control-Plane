# PB-11 — Legal & trust artifacts audit

**Document ID:** ACP-GOV-PB11-AUDIT-001  
**Audit date:** 2026-06-27 (delta refresh)  
**Auditor:** Cursor — PR `low/docs-legal-pb12-delta`  
**Baseline:** `master` post PR #110 + legal delta  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`SECURITY.md`](../../SECURITY.md)

---

## Verdict

| Question | Answer |
|----------|--------|
| **Legal files present?** | ✅ **YES** |
| **Content sufficient for PB-12 prep?** | ✅ **YES** — delta applied; **one human gate** remains (live contact) |
| **Hard blocker for private beta ops?** | ❌ **NO** |
| **Hard blocker for public flip?** | 🔄 **Human:** confirm `security@dataxmind.com` live + PB-9/PB-7/PB-10 |

---

## Checklist (post-delta)

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| LICENSE | `LICENSE` | ✅ | MIT per `pyproject.toml` |
| SECURITY.md | `SECURITY.md` | ✅ | 48h ack SLA; tiered CRITICAL/HIGH/MED/LOW; GH Security Advisories; AI CRITICAL table |
| CONTRIBUTING.md | `CONTRIBUTING.md` | ✅ | 8 invariants, PACE, branch naming, PR checklist, `/health` vs `/governance/status`, `shipped_config` HIGH+ |
| CODE_OF_CONDUCT.md | `CODE_OF_CONDUCT.md` | ✅ | Full Contributor Covenant **2.1** + enforcement contact |
| No secrets in shipped config | `config/*.yml` | ✅ | Template-only |
| README maintainer contact | `README.md` | ✅ | Linked |
| CONTRACT_TESTS pre-flip | `docs/CONTRACT_TESTS.md` | ✅ | PB-6 gate documented |
| OpenAPI export | `docs/openapi/` | 🔄 | Regenerate + publish on PB-12 flip |
| Branch protection API | `BRANCH_PROTECTION.md` | ⚠️ **Waiver** | 403 private repo until public / Team |
| Full deploy runbook | `docs/RUNBOOK.md` + systemd | ✅ | Operator SSOT |

---

## Delta applied (2026-06-27)

| Item | Before | After |
|------|--------|-------|
| Ack SLA | 72h | **48h** all severities |
| Remediation SLA | 14d flat | Tiered CRITICAL 30d / HIGH 60d / MED 90d |
| GH Security Advisories | Missing | ✅ Preferred path |
| AI CRITICAL scope | Implicit | Explicit table + kill switch note |
| CONTRIBUTING branch naming | Missing | ✅ |
| CONTRIBUTING PR checklist | Partial | ✅ Full checklist |
| CoC | Abbreviated | Full CC 2.1 |
| Claude HTML “legal ABSENT” | Stale | Banner updated |

---

## Pre-PB-12 actions (human)

1. **Confirm** `security@dataxmind.com` (or replacement) is live and monitored.
2. **Complete** PB-9 calendar soak (≥14 days) — [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md).
3. **PB-7** clean-machine fork ≤15 min on **CLEAN** host.
4. **PB-10** production soak ≥30 days after PB-9 pass.
5. **PB-6** regenerate OpenAPI + publish static spec on flip.
6. Re-probe branch protection API after public flip or Team upgrade.

---

## Verify (docs-only PR)

```bash
test -f SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md
grep -q CRITICAL SECURITY.md
grep -q Invariant CONTRIBUTING.md
grep -q "48 hours" SECURITY.md
grep -q "Contributor Covenant" CODE_OF_CONDUCT.md
```

---

**Operator sign-off:** ☐ Maintainer confirms contact inbox live before PB-12 Gate E
