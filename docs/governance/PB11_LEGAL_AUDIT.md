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
| **Content sufficient for PB-12 prep?** | ✅ **YES** — legal delta + maintainer sign-off @ 2026-06-27 |
| **Hard blocker for private beta ops?** | ❌ **NO** |
| **Hard blocker for public flip?** | 🔄 **Ops:** PB-9 / PB-7 / PB-10 calendar; mailbox live test before flip |

---

## Maintainer approval (2026-06-27)

| # | Gate | Status | Notes |
|---|------|--------|-------|
| 1 | `security@dataxmind.com` as contact | ☑ **Approved** | Mailbox + **live test PASS** 2026-06-28 — [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) |
| 2 | GitHub Discussions | ☑ **Approved** | Enable in repo Settings (see §GitHub Discussions) |
| 3 | PB-9 calendar soak | ☑ **Acknowledged** | Execution in progress — [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) |
| 4 | PB-7 clean-machine fork | ☑ **Acknowledged** | Operator: separate CLEAN laptop |
| 5 | PB-10 production soak 30d | ☑ **Acknowledged** | Starts after PB-9 Day 14 pass |
| 6 | PB-12 human go/no-go | ☑ **Acknowledged** | After checklist complete |

---

## Contact setup (`security@dataxmind.com`)

**Cần tạo ngay không?** **Chưa bắt buộc** trong giai đoạn private + PB-9. **Bắt buộc trước PB-12** (public flip) — gửi email thử và đáp ứng SLA 48h.

**Không đưa vào git:** password, app password, API key email provider, OAuth tokens.

| Bước | Việc làm |
|------|----------|
| 1 | Chọn provider: Google Workspace, Microsoft 365, Zoho Mail, hoặc **Cloudflare Email Routing** (alias → maintainer inbox) |
| 2 | DNS: thêm **MX records** cho `dataxmind.com` theo hướng dẫn provider |
| 3 | Tạo mailbox **`security@`** hoặc **alias** forward tới inbox maintainer đang monitor |
| 4 | (Tuỳ chọn) SPF + DKIM + DMARC — giảm spam khi public |
| 5 | **Trước PB-12:** gửi email thử từ account ngoài → xác nhận nhận được trong 48h |

**Đường báo cáo không cần email:** [GitHub Security Advisories](https://github.com/DataXMind/AI-Control-Plane/security/advisories/new) — hoạt động khi repo private/public; maintainer nhận notification GitHub.

---

## GitHub Discussions

**Bật (UI):**

1. Repo → **Settings** → **General**
2. Cuộn **Features** → bật **Discussions**
3. (Tuỳ chọn) **Set up discussions** → chọn category mặc định *General / Ideas / Q&A*

**Hoặc CLI (org admin):**

```bash
gh api repos/DataXMind/AI-Control-Plane -X PATCH -f has_discussions=true
```

CONTRIBUTING trỏ câu hỏi how-to → Discussions; bugs → Issues.

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

1. ~~**Confirm** `security@dataxmind.com`~~ → ☑ **PASS** — live test 2026-06-28 (two-way send/ack)
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

**Operator sign-off:** ☑ Maintainer **DataXMind** @ **2026-06-27** — contact `security@dataxmind.com` approved; gates 1–6 acknowledged; mailbox live test required before PB-12 Gate E.
