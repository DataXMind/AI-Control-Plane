# security@ — Live email test (pre-PB-12)

**Document ID:** ACP-GOV-SECURITY-EMAIL-LIVE-001  
**Mailbox:** `security@dataxmind.com`  
**Gate:** `public_beta.gates_remaining` — closes in **practice evidence** only until catalog bump @ flip  
**Parent:** [`PB11_LEGAL_AUDIT.md`](../../PB11_LEGAL_AUDIT.md) §Contact setup

---

## Prerequisites (operator confirmed @ 2026-06-28)

- [x] DNS MX / routing configured for `dataxmind.com`
- [x] Mailbox or alias `security@` → inbox monitored by maintainer
- [ ] **Live test** — this runbook

**Never commit:** passwords, app passwords, API keys.

---

## Step-by-step live test

### 1 — Send test from external account

Use a **personal email** (Gmail, Outlook, etc.) — not the same inbox as forward target.

**To:** `security@dataxmind.com`  
**Subject:** `[ACP LIVE TEST] security@ mailbox verification — YYYY-MM-DD`  
**Body (minimal):**

```text
AI Control Plane — pre-PB-12 security contact live test.
Operator: DataXMind
Date: YYYY-MM-DD UTC
Expected: receipt within 48h per SECURITY.md SLA.
```

### 2 — Confirm receipt

- [ ] Email arrived in maintainer inbox (or alias forward target)
- [ ] Not in spam (if spam → note SPF/DKIM follow-up)
- [ ] Timestamp recorded (UTC)

### 3 — Optional reply (recommended)

Reply from maintainer acknowledging receipt (proves two-way path if needed):

```text
Received — ACP security@ live test OK @ <timestamp UTC>.
```

### 4 — Record evidence

Fill [`RESULTS.md`](RESULTS.md) and commit:

```bash
git add docs/governance/practice-evidence/security-email-live-test/
git commit -m "docs: security@ live test PASS evidence"
```

### 5 — Do not

- Paste credentials into repo
- Mark `governance_catalog.py` gate closed without maintainer flip approve
- Use GitHub Issues for this test (optional parallel: GitHub Security Advisories path remains valid)

---

## SLA reference

[`SECURITY.md`](../../../SECURITY.md) — 48h acknowledgment target for real reports.
