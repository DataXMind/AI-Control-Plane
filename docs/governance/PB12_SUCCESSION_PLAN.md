# PB-12 Succession Plan

**Purpose:** Ensure PB-12 public flip can proceed even if primary maintainer is unavailable.
**Target date:** ~2026-07-10

## Authorization Matrix

| Role | Name | Contact | Authority | Quorum required |
|---|---|---|---|---|
| Primary Maintainer | **dmin** — Primary Maintainer & PB-12 Release Authority | maintainer@dataxmind.com | Full PB-12 authority | Solo sufficient |
| Secondary Maintainer | **dataxmind** — Secondary Maintainer (Deputy; Mac witness host) | maintainer@dataxmind.com | PB-12 authority with Deputy | 2 of 2 with Primary |
| Operator (non-maintainer) | — | — | Cannot authorize PB-12 alone | Must engage maintainer |

## Primary Maintainer Unavailability Protocol

### If unavailable < 3 days before target (07-10):
1. Delay PB-12 by 3 days — no governance impact
2. Notify any waiting stakeholders
3. Resume when available

### If unavailable > 3 days (medical, emergency):
1. Secondary Maintainer may proceed IF:
   - Day 14 PB-9 PASS evidence exists (RESULTS.md completed)
   - Smoke 8/8 PASS on day of flip
   - Pre-flip checklist completed (export_openapi.py etc.)
2. Secondary Maintainer documents decision in PB-12 sign-off with note: "Primary unavailable — succession activated"
3. Primary Maintainer ratifies decision on return (retroactive sign-off)

## PB-12 Checklist (Complete Before Any Flip)
- [ ] Day 14 PB-9 RESULTS.md complete — PASS verdict
- [ ] Smoke 8/8 PASS on flip day (not from earlier)
- [ ] export_openapi.py run — no diff or diff committed
- [ ] verify_governance_status_runtime.sh PASS
- [ ] verify_openapi_runtime.sh PASS
- [ ] CHANGELOG entry for v0.1.0-beta.1 verified
- [ ] PB-10 defer text recorded in this sign-off
- [ ] GitHub Security Advisories enabled (post-flip immediate action)
- [ ] Dependabot enabled (post-flip immediate action)
- [ ] Release v0.1.0-beta.1 created from existing v0.1.0-rc.1 tag

## Digital Authorization Format
PB-12 sign-off is a commit to master with this format:
```
docs(pb-12): operator sign-off — GO for public flip

Authorized by: [Name] ([role])
Date: YYYY-MM-DD HH:MM UTC
Day 14 PASS: yes — see pb-9-day14-review/RESULTS.md
Smoke: 8/8 @ [SHA]
PB-10 defer: accepted — GA track per go/no-go §PB-10
```

## If PB-12 Must Be Delayed
Delay criteria (update SESSION_ANCHOR one-liner if delayed):
- Day 14 FAIL → extend soak per ROLLBACK_PROTOCOL.md Scenario 1
- SEV-1 found pre-flip → pause, fix, re-verify
- Maintainer unavailable + no Secondary → delay, do not delegate to non-maintainer
