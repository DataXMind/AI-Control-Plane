# Current session anchor — copy-paste block (living snapshot)

**Document ID:** ACP-PROMPT-ANCHOR-CURRENT-001  
**Update rule:** Maintainer or closing agent updates this file after **major merge** to `master`.  
**Structure SSOT:** [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md)

---

## Canonical one-liner (2026-07-27 post-F-01-merge resync)

```text
SESSION ANCHOR: master @ 02574f8 (#211, 2026-07-27) · governance 1.6.0 · pytest 253 · risk LOW
PUBLIC: repo flipped 2026-07-06 · release v0.1.0-beta.1 · PB-10 deferred #78 (clock not started)
PB-9: CLOSED #77 · catalog gates_remaining=1 (PB-10 only)
2026-07-19 review pass (F-01/F-02/F-03) — ALL 3 FIXED AND MERGED as of 2026-07-27:
  F-01 (ABAC Deny-prod-k8s bypass, ConditionEvaluator actions-key exact-match vs wildcard) -> #210
  F-02 (role-trust escalation on /policy/evaluate) -> #209
  F-03 (test coroutine warning) -> #208
  Prod-k8s approval gate bypass is CLOSED. Do not re-open without new evidence.
OPEN (real, unresolved): Q-15 — session.create missing from backend.allowed_actions in both
  config/policies.yml and customer-bundle/production-config/policies.yml. AEOS runs with
  ACP_ENABLED=false because of this. Ready-to-approve diff drafted in
  STATE/HUMAN_REVIEW_QUEUE.md §B item 6 — needs Human approve before any agent touches
  policies.yml (CRITICAL, always human-approve-first).
OPEN (process, no code): mục B items 7-11, mục C items 12-13 in STATE/HUMAN_REVIEW_QUEUE.md —
  product/cross-repo/credential decisions, not executable by an agent. See that file for plain-
  language explanations of each.
Verify: GET /governance/status → phase Public Beta 0.x · gates_blocking_pb12 []
SSOT for detail: STATE/HUMAN_REVIEW_QUEUE.md (entry point — read first) · STATE/PROGRESS.md
  (window-close narrative) · STATE/DECISIONS.md (open questions + resolved decisions)
```

**Last updated:** 2026-07-27 · post-merge resync — 2026-07-19 review pass fully closed (F-01/F-02/F-03), risk back to LOW, only Q-15 + product/process decisions remain open

**⚠️ If you are a new session/agent reading this:** this repo runs multiple concurrent agent sessions on the same checkout(s) — branch and working-tree state can change between your turns without you doing it (this happened during the exact session that wrote this line). Before editing anything, run `git fetch origin && git log <your-branch>..origin/master --oneline` to check you're not already behind. Do not trust a cached mental model of "current state" older than this file's date — re-read `STATE/HUMAN_REVIEW_QUEUE.md` fresh every time, it is the entry point.
