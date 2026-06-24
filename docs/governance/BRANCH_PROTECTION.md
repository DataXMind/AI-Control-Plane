# Branch protection — team workflow (GAP-BP-1)

> **Status:** Documented workflow until GitHub Team / public repo enables API enforcement  
> **Script:** [`scripts/setup_github_milestones_and_protection.sh`](../../scripts/setup_github_milestones_and_protection.sh)

---

## Constraint

Private repositories on **GitHub Free** (org `DataXMind`) cannot enforce branch protection via the API. The Rulesets UI may appear, but enforcement requires **GitHub Team** or making the repository **public**.

Until upgrade, protection is **process-based**, not platform-enforced.

---

## Required team workflow (master)

1. **No direct pushes to `master`** — all changes via pull request.
2. **CI must be green** before merge:
   - `Smoke gate`
   - `Full suite`
3. **At least one approving review** on every PR (author may not self-approve production merges).
4. **Resolve all review threads** before merge (`required_conversation_resolution` when API protection is enabled).
5. **Squash or merge commit** per repo convention; no force-push to `master`.

---

## Enabling API protection (when plan allows)

```bash
bash scripts/setup_github_milestones_and_protection.sh --protection-only
```

Expected settings on `master`:

| Setting | Value |
|---------|-------|
| Required status checks | `Smoke gate`, `Full suite` (strict) |
| Required PR reviews | 1 approval, dismiss stale |
| Force push | disabled |
| Deletion | disabled |
| Conversation resolution | required |

---

## Verification

```bash
gh api repos/DataXMind/AI-Control-Plane/branches/master/protection --jq '.required_status_checks,.required_pull_request_reviews'
```

If the API returns `403` or mentions upgrade, continue with the manual workflow above.

---

## Related

- [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md) — GAP-BP-1
- [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) — PACE + PR gates
