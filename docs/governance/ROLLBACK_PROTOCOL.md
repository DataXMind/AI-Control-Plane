# ACP Rollback Protocol

**Document ID:** ACP-GOV-ROLLBACK-001  
**Scope:** PB-9 soak failure · post-flip SEV-1 · emergency hotfix · operator version rollback  
**Related:** [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) · [`SECURITY.md`](../../SECURITY.md)

---

## Scenario 1 — PB-9 Day 14 FAIL

If Day 14 review finds SEV-1 or SEV-2:

1. DO NOT close #77
2. Extend soak by N days (minimum **7** additional days per SEV-1, **3** per SEV-2)
3. Document in `PB9_STAGING_SOAK_LOG.md`: `Extended due to [SEV type] on [date]`
4. Re-run Day 14 template at new target date
5. Day 14 extended = `new_target_date`. Do NOT use 2026-07-06 in future references.
6. Notify: update `docs/prompts/SESSION_ANCHOR_TEMPLATE.md` one-liner with new date

---

## Scenario 2 — SEV-1 After Public Flip (PB-12)

If critical bug found after repo goes public:

1. DO NOT make repo private (breaks external forks/references)
2. Tag a hotfix: `git tag v0.1.0-beta.1-hotfix.1 -m "SEV-1: [description]"`
3. Commit fix on new branch: `hotfix/[issue-id]-[description]`
4. PR → `master` (bypass docs-only rule for security hotfix ONLY)
5. Post GitHub Security Advisory immediately
6. Notify `security@dataxmind.com` thread with internal incident record
7. Update `CHANGELOG.md` with hotfix entry

---

## Scenario 3 — Hotfix Bypass of Governance (Emergency Only)

**Trigger:** SEV-1 security vulnerability in production

**Authorization:** Maintainer + one additional team member (**quorum 2**)

**Bypass:** Karpathy docs-only rule suspended for hotfix PR ONLY

**Evidence required:** Incident record in `docs/governance/practice-evidence/incidents/`

**Return to docs-only:** Immediately after hotfix merge

---

## Scenario 4 — Version Rollback Request

ACP does not support runtime downgrade in 0.x.

For operators needing previous behavior: `git checkout [previous-tag]` in their deployment.

Document: operator pins version in their `docker-compose.yml` via image tag.

---

## What Cannot Be Rolled Back

- GitHub visibility change (public → private breaks community trust)
- PB-8 tag (do not re-tag `v0.1.0-rc.1`; see go/no-go)
- Merged `CHANGELOG.md` entries (append-only)
- `security@` live test (one-time verification, no rollback needed)

---

**Last updated:** 2026-06-28 · Catalog v1.3.3 · `master` @ `7ea0224`
