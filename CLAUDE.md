# CLAUDE.md — AI Control Plane

**Behavioral constitution** for AI coding agents on this repo.  
**Derived from:** Andrej Karpathy's observations on LLM coding pitfalls (adapted for ACP).  
**Layer:** L0 — companion to [`.cursorrules`](.cursorrules) (6-layer stack)  
**Audience:** Claude Code, Cursor, and other coding agents  
**Full governance:** [`.cursorrules`](.cursorrules) · [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`AGENTS.md`](AGENTS.md) (ML5 entry)

---

## 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs before implementation.

Before any code:

1. State explicitly which files you will touch
2. List assumptions you are making — if uncertain, ask
3. Name the verify command that confirms success
4. If a simpler approach exists, present it before the complex one

For ABAC, policy, or authentication tasks: explicitly list condition keys / behaviors you will implement vs skip. Skip without flagging = silent assumption (**P-04** anti-pattern).

---

## 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked
- No abstractions for single-use code in this repo
- If 50 lines suffice, do not write 200
- No error handling for impossible scenarios (trust Pydantic validation)

**Senior engineer test:** Would a reviewer ask "why this complex?" — if yes, simplify before submit.

The **8 invariants** in `ARCHITECTURE.md` define boundaries; inside them, always prefer the simpler implementation.

---

## 3. Surgical changes

Touch only what you must. Every changed line traces to the request.

- Do **not** improve adjacent code, comments, or formatting unless asked
- Do **not** refactor code that your task did not break
- Match existing style (structlog, Pydantic v2, async/await)
- Dead code you notice → mention in PR body; do **not** delete unless the task includes cleanup

**File scope discipline (P-02):**

- docs-only task → `*.md` and `docs/**` only; need `src/` → stop and reclassify (MEDIUM)
- test-only task → `tests/**` only; need `src/` → MEDIUM, not LOW

After changes: remove only imports/variables **your** changes made unused. Pre-existing dead code stays unless cleanup is explicitly in scope.

---

## 4. Goal-driven execution

Define success criteria. Loop until verified.

| Instead of | Transform to |
|------------|--------------|
| Fix the policy bug | Write test reproducing failure, then make it pass |
| Add ABAC condition | `test_policies.py` covers new condition, then implement |
| Refactor quota logic | All existing quota tests pass before and after |

**ACP verify gate (run in this order):**

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config   # HIGH+ / config touch
```

Multi-step tasks: state plan with verify per step **before** executing step 1.

---

## ACP-specific rules

### 8 invariants (`ARCHITECTURE.md` — never violate)

1. `core/policies.py` — custom engine only; no OSS policy runtime replacement
2. `core/models.py` — all data contracts here, nowhere else
3. `mcp/git_server.py` — facade only; no Git logic in Python
4. `cli/` — HTTP/API calls only; no direct `core/policies` imports
5. `apex/` — SAPAL loop here; OSS tools called **from** apex/, not the reverse
6. `api/` — sole cross-language bridge to TypeScript
7. `core/quota.py` — `QuotaStore` ABC; swappable backend
8. `config/` — shipped defaults only; runtime path via `ACP_CONFIG_DIR`

### Risk classification

See [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) (full L2: F1–F11, per-level verify):

| Level | When |
|-------|------|
| **LOW** | docs-only; **test-only** with no `src/` in diff |
| **MEDIUM** | CLI, config, non-breaking API; tests **paired with** `src/` |
| **HIGH** | `core/`, schema, `apex/` design — Claude review **before** code |
| **CRITICAL** | PolicyEngine, ABAC, invariants, identity — **human approve** first |

### Forbidden (absolute)

- Push/merge `master` without human instruction
- Import OSS policy engines into `core/`
- Issue ranges in PR body (`Closes #52..#62`) — use individual `Closes #N` (P-03)
- Combine different risk levels in one PR (F4)
- Mark sprint DONE before all sprint PRs on `master` (P-05 / F7)
- Skip "state assumptions" for ABAC/policy/loader work (P-04 / F8)
- Delete or archive `LESSONS_LEARNED.md` entries (P-11 / F9)

### Governance memory (L5 — do not rely on chat)

Read [`docs/governance/LESSONS_LEARNED.md`](docs/governance/LESSONS_LEARNED.md) before tasks resembling past failure patterns.

| Resource | Use |
|----------|-----|
| [`AGENTS.md`](AGENTS.md) | Agent entry, approval gates, PB-9 soak rule |
| [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md) | Open every session (Tier B memory) |
| [`docs/governance/L5_MATURITY_MODEL.md`](docs/governance/L5_MATURITY_MODEL.md) | ML0–ML5 memory maturity |
| [`docs/governance/gold-patterns/GP-01-agent-session-memory.md`](docs/governance/gold-patterns/GP-01-agent-session-memory.md) | Public export pattern |
| [`docs/governance/GOVERNANCE_UX_RUNTIME.md`](docs/governance/GOVERNANCE_UX_RUNTIME.md) | CS-01..06 runtime catalog |
| [`docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md) | Operator evidence — do not over-claim |
| [`docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md`](docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md) | Gate A/C before G1+ execution |

---

## 5. Autonomous execution & continuity protocol

Extends sections 1–4 for long-running, multi-session, possibly multi-agent work. Does not replace the Risk classification or Forbidden list above — the Forbidden list always wins on conflict.

### 5.1 Source of truth — use existing files, do not create parallel ones

This repo already has every file a continuity protocol needs. Reuse them; do not invent `PROJECT_ANCHOR.md` / `DECISION_LOG.md` / `LESSONS_LOG.md` / `CURRENT_STATUS.md` / `DAILY_LOG.md` — a second SSOT next to an existing one is exactly how this repo got **P-07** (doc drift between sprints) and **P-08** (stale L1 after milestone close).

| Generic role | Read/write this file instead |
|---|---|
| Project anchor (current state, key config, open issues) | [`docs/prompts/ANCHOR_CURRENT.md`](docs/prompts/ANCHOR_CURRENT.md) |
| Decision log (append-only, confirmed values) | `STATE/DECISIONS.md` (per-repo local) — cross-repo decisions also recorded at the shared Kickoff Brief this project uses, if one is in play |
| Lessons log (root cause → fix) | [`docs/governance/LESSONS_LEARNED.md`](docs/governance/LESSONS_LEARNED.md) — append-only, never delete (P-11/F9) |
| Most recent phase/daily closeout | most recent `docs/governance/practice-evidence/*/RESULTS.md` or sprint report by date |
| Process changelog (versioned) | [`docs/governance/GOVERNANCE_CHANGELOG.md`](docs/governance/GOVERNANCE_CHANGELOG.md) |
| Current status snapshot | `STATE/PROGRESS.md` |
| Pending human-action queue (credential / merge / decision awaiting a human, status tracked live) | `STATE/HUMAN_REVIEW_QUEUE.md` |

If a mapped file is missing for the task at hand, say so in the first report rather than proceeding on assumption — do not silently create a same-purpose file under a different name.

### 5.2 Re-anchoring & Handoff Audit

Before touching any code in a new session, or when resuming work a different session/agent started, read `docs/prompts/ANCHOR_CURRENT.md`, the tail of `STATE/DECISIONS.md` and `STATE/PROGRESS.md`, and the top of `docs/governance/LESSONS_LEARNED.md`. Then state a short **Handoff Audit**: what you understand the current state to be, what you're about to do next, and any discrepancy between your understanding and those files. If a discrepancy exists, resolve it with tools or escalate — never proceed on a best guess.

Re-anchor at: session start; before each new task/sub-task; after any long tool-output-heavy operation; whenever an assumption contradicts `STATE/DECISIONS.md` or `ANCHOR_CURRENT.md`; at least once per phase on long tasks.

Never delete or silently overwrite a `STATE/DECISIONS.md` row to change it — append a new row that explicitly marks the prior one superseded, with reason and date (this repo already does this informally, e.g. "ĐÃ PHÂN XỬ → D-12"; make the superseded/active marking explicit from now on). If two sources conflict, stop and flag the conflict — do not silently pick one.

### 5.3 Human gate tiers — a second axis alongside Risk classification

Risk classification (§ACP-specific rules above) measures **blast radius** (which files, how central). This is a different axis: **can execution proceed without a human right now at all.**

| Tier | Meaning | Examples |
|---|---|---|
| **A — autonomous** | No human needed; proceed continuously | writing code, local builds, unit/integration tests, refactors, internal docs, non-destructive local ops |
| **B — needs human-supplied input** | Agent cannot legitimately generate this itself | credentials, API keys, SSH/VPS access, passwords, tokens, DNS/domain control, billing actions, third-party account access |
| **C — needs human approval** | High-risk/ambiguous/irreversible, even if the agent believes it knows the answer | destructive/irreversible action; requirement conflicting with `STATE/DECISIONS.md`; scope/architecture change beyond what was asked; cost/billing-affecting action; suspected security issue; **same error recurring after 3 fix attempts** (stop, do not try a 4th blind retry); any case that requires a business/product guess |

**Reconciliation with Risk classification:** `CRITICAL` always implies Tier C. Tier C can also fire on a `LOW`/`MEDIUM`-looking diff if a Tier C trigger fires anyway (e.g. a destructive git operation inside a docs-only change). Every item in the **Forbidden (absolute)** list above is Tier C regardless of self-assessment.

Tier B: never fabricate, guess, or silently reuse a credential-shaped value. If a placeholder is needed to keep developing, label it explicitly, e.g. `MOCK_SSH_KEY_DO_NOT_USE` — never present it as usable, and swap it for the real value before any real deploy/test against production.

**Stop-and-report format for Tier B/C** (use verbatim):

```
## HUMAN INPUT REQUIRED / ESCALATION
Type: [missing credential | ambiguous requirement | destructive action | loop detected | cost | security]
Exact ask: <precisely what value, decision, or approval is needed>
Why the agent cannot resolve this itself: <reason>
What has been verified/tried so far: <evidence>
Blocked tasks: <list>
Proposed options (if any): <A / B / C with tradeoffs, no default silently chosen>
```

### 5.4 Pre-execution forecast & post-execution report

Extends §4's "state plan with verify per step before executing step 1." Before writing code for a new task/sub-task, forecast in a few lines: expected outcome + affected files/modules, risk level and why, test plan (which checks in §5.5 apply), rollback plan. Larger tasks get more detail; do not skip even for small ones.

After finishing, report: actual result with evidence (`file:line`, real command output — never state "tests pass" without pasting the output), and classify variance as **MATCH** / **MINOR DEVIATION** / **MAJOR DEVIATION** / **FAILED**, with root cause of any deviation and what should change next time (feeds `docs/governance/LESSONS_LEARNED.md`).

### 5.5 Smoke test matrix — maps onto the existing ACP verify gate

| Generic check | Command in this repo |
|---|---|
| Lint / type check | `ruff check src/ tests/` · `mypy src/ai_control_plane/ --strict` |
| Build/compile | `pip install -e .` succeeds; API starts (`uvicorn ai_control_plane.api.server:app`) |
| Unit smoke | `pytest tests/ -v` |
| Regression smoke | same full suite — no previously-passing test may break |
| Integration smoke | `pytest tests/test_smoke.py -v -m smoke` (SMK-01..06c) |
| Config/schema touch | `pytest tests/test_shipped_config_parity.py -v -m shipped_config` |
| Secret/security scan | no credentials/tokens/PII in the diff — see `SECURITY.md` |

Paste the real command and real output for every applicable check in the post-execution report — a claimed result without attached output does not count.

### 5.6 Integration testing at task/PR/sprint boundaries

Run an integration check at each boundary this repo already has: sub-task→task (within a PR), task→PR (before opening), PR→sprint close (**P-05**: sprint DONE only after all sprint PRs are on `master`). At each boundary, state before/during/after: what this touches or could break, tests run with real output, residual risk carried forward.

### 5.7 Cross-agent review (independent reviewer pass)

For `HIGH`/`CRITICAL` work — and always for anything touching `policies.yml` or governance core — the review must come from someone/something other than the diff's author: a separate `/code-review` pass, a fresh session, or another approving reviewer. It checks specifically for: context drift from the original task/spec, discarding a still-valid `STATE/DECISIONS.md` entry in favor of an unverified new one, hallucinated file paths/APIs/config keys, and consistency with this repo's actual conventions (not "good practice in general"). This review re-checks tool output itself — it does not trust the executor's narrative.

### 5.8 Memory & lessons

Extends "Governance memory" above: search `docs/governance/LESSONS_LEARNED.md` by pattern/topic before starting any task resembling a past failure. After any failure, bug, or incorrect assumption, append a new entry (what happened, root cause, fix, how to avoid it next time). Never delete or archive entries (**P-11/F9**, unchanged).

### 5.9 Process versioning

Standing process/review rules for this repo do not change silently. `docs/governance/GOVERNANCE_CHANGELOG.md` is this repo's process changelog (MAJOR/MINOR/PATCH already defined there) — any change to the process itself needs a dated entry there and explicit human approval before taking effect.

This CLAUDE.md edit is itself such a process change, made under direct human instruction on 2026-07-08 (see Changelog line below). A matching `GOVERNANCE_CHANGELOG.md` / `GOVERNANCE_VERSION` bump is a **deliberate follow-up, not done here**: `GOVERNANCE_VERSION` is hardcoded in `src/ai_control_plane/core/governance_catalog.py:9` and served by `GET /governance/status` — bumping the changelog number without bumping that constant in the same change would itself be **P-07/P-08 drift** (docs claiming a version the running API doesn't report). Per §3 file-scope discipline, a `src/` touch reclassifies this from a docs-only change to `MEDIUM` — out of scope for this batch; do it as its own task with the code constant and changelog entry in the same PR.

### 5.10 Reporting cadence

Per-task: post-execution report in the PR body/commit message. Per-sprint: sprint report + `STATE/PROGRESS.md` update (existing **P-05/P-07** rules). Daily/weekly rollups: append to `STATE/PROGRESS.md`'s batch log, or for ops/soak workloads to a `docs/governance/PB9_SOAK_ITERATION_LOG.md`-style log — do not create new `DAILY_LOG.md`/`WEEKLY_LOG.md` files; that would be a second status SSOT.

### 5.11 Continuous execution & stop conditions

For Tier A work: forecast → execute → smoke test (§5.5) → post-execution report → cross-agent review if `HIGH`/`CRITICAL` (§5.7) → integration check at boundaries (§5.6) → update logs (§5.1) → re-anchor (§5.2) → next task, without pausing for human input inside that chain. The moment a task is Tier B/C, or a loop-detection/security/cost trigger fires: stop that thread, emit the §5.3 escalation block, and continue other unblocked Tier A work rather than halting the entire session. The **Forbidden (absolute)** list above is never eligible for the autonomous loop, regardless of tier self-assessment.

### 5.12 Anti-drift & anti-hallucination summary

- Treat your own unverified memory as untrustworthy — re-derive from files/tool output every session and after every long operation.
- Never fabricate credentials, test results, or file contents. Use explicitly labeled `MOCK_*` placeholders, or stop and ask.
- Never delete or overwrite a decision or lesson — supersede with a reasoned, dated entry.
- Adversarially self-review before declaring a task done; a separate pass catches what the executor missed on `HIGH`/`CRITICAL` work.
- Escalate rather than guess whenever a real secret, an irreversible action, a conflicting requirement, a cost threshold, a security concern, or a repeated failure (3 attempts) is involved.

### 5.13 Session close-out checklist

Extends §5.2 (which anchors the *start* of a session) with the mirror-image ritual for the *end* of one. Do this before ending a long or multi-step session — not just a final chat message, written to files per §5.1.

1. **Re-verify, don't recall.** `git fetch origin` then `git log <branch>..origin/master --oneline` — confirm you are not closing out against a baseline other sessions have already moved past (this repo runs multiple concurrent agent sessions on the same checkout; branch and working-tree state can change between your turns without you doing it). Re-read any file you're about to cite fresh — do not trust what it said earlier in this same conversation.
2. **Verify every "done" claim with a real command**, not a restated intention: test output, `git log`/`git show`/`git diff`, or a live API call. If you cannot re-verify something, write "CHƯA VERIFY LẠI" instead of asserting it's done.
3. **Route content to the file whose job it already is** (§5.1 table) — an anchor one-liner to `ANCHOR_CURRENT.md`, progress/evidence to `STATE/PROGRESS.md`, new open questions or decisions to `STATE/DECISIONS.md`, anything only a human can act on to `STATE/HUMAN_REVIEW_QUEUE.md`. Do not create a single combined close-out file — that recreates the exact `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` mistake this repo already made once (see its archived copy, `docs/governance/ACP_HANDOFF_FOR_NEW_CONVERSATION_2026-06-27.md`) and P-18.
4. **Never delete or silently overwrite another session's entry.** Correcting a stale claim means appending a new, dated entry that marks the old one superseded (per §5.2) — except a queue's own status column (e.g. `HUMAN_REVIEW_QUEUE.md`'s 🔴/🟡/🟢), which is explicitly designed to be updated in place as work closes, per that file's own header.
5. **If two sources conflict** (a STATE file vs. git reality, or one STATE file vs. another), record both explicitly and say so — do not silently pick one side or quietly drop the discrepancy.
6. **Report** (chat and/or PR body): which file(s) and section(s) you updated, the real evidence behind each claim, and an explicit split of what is *actually* closed this session (merged/committed/test-passed — not just planned or coded-but-unverified) vs. what remains open and where it now lives (`HUMAN_REVIEW_QUEUE.md` or `DECISIONS.md`).

A worked example of this checklist applied in practice is in `STATE/PROGRESS.md`, the `🔒 WINDOW-CLOSE` entries.

---

**Last updated:** 2026-07-26 @ added §5.13 Session close-out checklist + `STATE/HUMAN_REVIEW_QUEUE.md` row in the §5.1 table (same still-unapproved batch as the rest of §5 — see `STATE/HUMAN_REVIEW_QUEUE.md` item A.5 and `STATE/DECISIONS.md` open question #7). Previous: 2026-07-08 @ added §5 Autonomous execution & continuity protocol (human-directed integration of an external agent-protocol prompt, mapped onto this repo's existing SSOT files — no new parallel logs created)
