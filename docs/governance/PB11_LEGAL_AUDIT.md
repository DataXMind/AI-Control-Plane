# PB-11 — Legal & trust artifacts audit

**Document ID:** ACP-GOV-PB11-AUDIT-001  
**Audit date:** 2026-06-26  
**Auditor:** Cursor (Phương án E)  
**Baseline:** `master` @ `dd16769`  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`GOVERNANCE_POST_CLAUDE_EXECUTION_AUDIT.md`](GOVERNANCE_POST_CLAUDE_EXECUTION_AUDIT.md)

---

## Verdict

| Question | Answer |
|----------|--------|
| **Legal files present?** | ✅ **YES** — not absent as Claude HTML claimed (stale) |
| **Content sufficient for PB-12 prep?** | ✅ **YES** with noted placeholders |
| **Hard blocker for private beta ops?** | ❌ **NO** |
| **Hard blocker for public flip?** | 🔄 **Review placeholders** before PB-12 |

---

## Checklist

| Artifact | Path | Status | Notes |
|----------|------|--------|-------|
| LICENSE | `LICENSE` | ✅ | MIT per `pyproject.toml` |
| SECURITY.md | `SECURITY.md` | ✅ | 72h ack / 14d fix SLA; **replace `security@dataxmind.com` before public flip** |
| CONTRIBUTING.md | `CONTRIBUTING.md` | ✅ | 8 invariants, PACE, smoke §5.5, L2 risk, session anchor |
| CODE_OF_CONDUCT.md | `CODE_OF_CONDUCT.md` | ✅ | Contributor Covenant 2.1 |
| No secrets in shipped config | `config/*.yml` | ✅ | Template-only; `DATA_CLASSIFICATION.md` |
| README maintainer contact | `README.md` | ✅ | Linked |
| Branch protection API | `BRANCH_PROTECTION.md` | ⚠️ **Waiver** | 403 private repo — process-only until PB-12 (approved 2026-06-22) |
| OpenAPI export | `scripts/` | 🔄 | PB-6 — publish on flip |
| Full deploy runbook | `examples/minimal/` + systemd | 🔄 | PB-9 soak; VPS 24/7 documented |

---

## Claude HTML correction

`practice_studies_architecture_review.html` pane PB listed legal as **ABSENT** — **incorrect** at audit date. Files existed pre-PR #99. Use this audit + `OPEN_SOURCE_READINESS.md` as SSOT.

---

## Pre-PB-12 actions

1. Confirm `SECURITY.md` contact email is live.
2. Complete PB-9 calendar (≥14 days).
3. Human PB-7: clean-machine fork ≤15 min.
4. Re-probe branch protection API after public flip or Team upgrade.

---

**Operator sign-off:** ☐ Maintainer acknowledges before PB-12 Gate E
