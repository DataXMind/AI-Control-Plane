# Current session anchor — copy-paste block (living snapshot)

**Document ID:** ACP-PROMPT-ANCHOR-CURRENT-001  
**Update rule:** Maintainer or closing agent updates this file after **major merge** to `master`.  
**Structure SSOT:** [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md)

---

## Canonical one-liner (2026-07-20 window-close resync)

```text
SESSION ANCHOR: master @ 9607dbc (#205, 2026-07-16) · governance 1.6.0 · pytest 221 · risk CRITICAL — 2 unpatched findings on PolicyEngine
PUBLIC: repo flipped 2026-07-06 · release v0.1.0-beta.1 · PB-10 deferred #78 (clock not started)
PB-9: CLOSED #77 · catalog gates_remaining=1 (PB-10 only)
SACP prod ACP: B1+B2 VPS CLOSED @ 2026-07-06 · Q-15 policy regression on VPS still unpatched (session.create missing from backend allowed_actions) — AEOS running with ACP_ENABLED=false since
🔴 F-01 CRITICAL (NEW, found 2026-07-19, code-verified): ABAC `Deny-prod-k8s` does NOT block `k8s.apply` in prod — wildcard/exact-match mismatch at `core/policies.py` ConditionEvaluator `actions` key. Falls through to default_allow=True. UNPATCHED on master.
🔴 F-02 CRITICAL (found 2026-07-09, fix ready unmerged): client-supplied `role` in `/policy/evaluate` trusted without registry check — privilege escalation. Fix on branch `critical/policy-trust-hardening` @ `12d7a97`, NOT merged — still live on master.
F-01 + F-02 chained = full bypass of the prod-k8s approval gate, ACP's highest-value control.
Branch fragmentation: 6+ unmerged branches touch this repo (see STATE/PROGRESS.md "Bản đồ nhánh"); local git was 10 days / 6 commits behind origin until this resync.
Verify: GET /governance/status → phase Public Beta 0.x · gates_blocking_pb12 []
SSOT for detail: STATE/PROGRESS.md (window-close section) + STATE/HUMAN_REVIEW_QUEUE.md (action items) + STATE/DECISIONS.md (open questions)
```

**Last updated:** 2026-07-20 · window-close resync after 10-day local/origin drift · 2 CRITICAL findings surfaced, neither merged yet

**⚠️ If you are a new session/agent reading this:** this repo has multiple active branches from parallel sessions (see `STATE/PROGRESS.md`). Before editing anything, run `git fetch origin && git log master..origin/master --oneline` to check you're not already behind. Do not trust a cached mental model of "current state" older than this file's date.
