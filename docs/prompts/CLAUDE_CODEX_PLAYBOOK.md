# Claude & Codex — playbook (Projects · Code CLI · Codex)

**Document ID:** ACP-PROMPT-CLAUDE-CODEX-001  
**Parent:** [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md)  
**Audience:** claude.ai Projects · Claude Code · OpenAI Codex · ChatGPT agent mode

---

## 1. Platform comparison (ACP-specific)

| | **Claude Project** | **Claude Code CLI** | **OpenAI Codex** |
|--|-------------------|---------------------|------------------|
| **Runs in repo** | No (uploaded snapshots) | Yes | Yes (cloud sandbox) |
| **Live git SHA** | No — re-upload knowledge | Yes — `git pull` | Yes |
| **pytest / docker** | No — outputs commands | Yes | Yes |
| **Best ACP role** | Advisor · draft · audit | Execute like Cursor | Small patches |
| **PB-9 / PB-12** | Never execute | Draft only; human signs | Never auto-flip |
| **Setup doc** | [`CLAUDE_PROJECT_SETUP.md`](CLAUDE_PROJECT_SETUP.md) | §2 below | §3 below |

**Shared rule:** All platforms obey [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) §3 anti-drift and §8 Forbidden.

---

## 2. Claude Code CLI

### 2.1 When to use

- Terminal-native workflow without Cursor UI  
- Same execution power as Cursor — **same guardrails**

### 2.2 Session open

```bash
cd AI-Control-Plane
git pull origin master
git log -1 --oneline
```

Paste into Claude Code system/context:

1. Contents of [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md)  
2. `Read AGENTS.md and docs/prompts/AGENT_OPERATING_SYSTEM.md before editing.`  
3. Your `task:` + `file_allowlist`

### 2.3 Execution contract

| Allowed | Forbidden |
|---------|-----------|
| Edit files in allowlist | `git push master` without human |
| Run `pytest`, `ruff`, `mypy` | Tick PB-9 dates without operator phrase |
| Create branch + commit when asked | Bump `GOVERNANCE_VERSION` without flip approval |
| Draft `RESULTS.md` from `DAY14_REVIEW_DRAFT` | Claim `gates_remaining=0` |

### 2.4 Verify before "done"

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
```

Human merges PR on GitHub — Claude Code does not replace maintainer review.

---

## 3. OpenAI Codex (ChatGPT / API agent)

### 3.1 Context loading

Codex has no `.cursor/rules`. **Explicitly attach or paste:**

- [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md)  
- [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) §1 mental model + §8 Forbidden  
- [`_TEMPLATE.md`](_TEMPLATE.md) for structured tasks  

### 3.2 Scope discipline

Codex excels at **focused diffs** (1–3 files). For repo-wide audit:

1. Ask for **read-only plan** first (Pause)  
2. Narrow `file_allowlist`  
3. Execute in second message  

Avoid: "refactor entire codebase" without anchor + risk class.

### 3.3 Verify handoff

Codex may not have your Docker daemon. End every code task with:

```text
Human must run:
  pytest tests/test_smoke.py -m smoke
  [task-specific commands from _TEMPLATE.md]
```

---

## 4. Claude Projects (claude.ai) — advisory mode

### 4.1 Role boundary

```text
Claude Project = Tier B advisor + Tier C draft writer
Claude Project ≠ operator ≠ maintainer ≠ CI
```

**Does:** Draft Day 14 `RESULTS.md`, audit prompts for drift, explain gate matrix, Vietnamese/English ops guidance.  
**Does not:** Execute git, close #77, flip public, edit soak log without operator confirmation.

### 4.2 One-time setup

Follow [`CLAUDE_PROJECT_SETUP.md`](CLAUDE_PROJECT_SETUP.md) — upload ≤12 knowledge files.

**Refresh knowledge when:**

- `governance_catalog.py` version changes  
- Post roadmap PR batch (update `ANCHOR_CURRENT` upload)  
- After PB-12 flip (major state change)

### 4.3 New conversation opener (copy first message)

```text
[ACP Public Beta — Claude session]

Baseline: master @ bbc65cf · catalog v1.5.0 · 17 patterns · pytest 181 · smoke 8/8.

Đọc trong project knowledge (theo thứ tự):
1) AGENT_OPERATING_SYSTEM.md hoặc PROJECT_STATUS_FULL_TECHNICAL_REPORT
2) ANCHOR_CURRENT / SESSION_ANCHOR_TEMPLATE
3) MANUAL_OPERATOR_PLAYBOOK (nếu câu hỏi về operator)

Xác nhận ngắn:
1) Critical path và gate THỰC SỰ block PB-12 @ 0.x
2) Practice PASS vs gates_remaining — một câu
3) Việc operator làm HÔM NAY vs CHỜ calendar
4) Ba drift claim cần reject (SHA cũ, 165 tests, PB-10 blocks beta)

Sau đó hỏi tôi focus gì: PB-9 tick draft, Day 14 RESULTS, PB-12 memo, hay audit prompt?

Hard rules: không tick ngày tương lai · không đóng gates trong chat · không code src/ mới qua Public Beta soak.
```

### 4.4 Output format (ask Claude to follow)

```markdown
## Fact (Tier C path)
## Practice status
## Catalog status (pre-flip)
## Calendar
## Recommendation
## Human must verify (commands)
```

---

## 5. Claude ↔ Cursor handoff

| Step | Owner | Artifact |
|------|-------|----------|
| Architecture / plan | Claude Project or Claude | `docs/prompts/CLAUDE_PROMPT_*.md` from `_TEMPLATE.md` |
| Execute + PR | Cursor / Claude Code / Codex | Branch + CI green |
| Operator calendar | Human | `MANUAL_OPERATOR_PLAYBOOK.md` |
| Drift fix | Cursor docs PR | `GOVERNANCE_DRIFT_RECONCILIATION.md` |

**Packet handoff example:**

```text
Cursor: Implement docs/prompts/CLAUDE_PROMPT_X.md exactly.
Anchor: ANCHOR_CURRENT.md
Risk: LOW · docs-only · smoke 8/8
```

---

## 6. Task packet creation (Claude drafts → Cursor executes)

Use [`_TEMPLATE.md`](_TEMPLATE.md):

1. **Risk** + **allowlist**  
2. **Assumptions** (3 bullets)  
3. **Verify** block — always include smoke  
4. **Acceptance** checkboxes  

Save as `docs/prompts/CLAUDE_PROMPT_<TOPIC>.md` — durable Tier C for repeat tasks.

---

## 7. Anti-drift for non-Cursor agents

| Stale claim | Correct @ 2026-06-30 |
|-------------|----------------------|
| `5dc565b`, `ad3d58a`, `527eb5d` as current | `bbc65cf` — use `ANCHOR_CURRENT` |
| catalog v1.3.3 | **v1.5.0** · **17** patterns |
| 165 / 177 tests | **181** pytest |
| PB-9 tick through 28/06 | Through **30/06**; missing **07-01..05** |
| PB-10 blocks PB-12 | **Deferred** — record @ H1-03 |
| `examples/docker-compose.yml` | `examples/minimal/docker-compose.yml` |

---

## 8. Knowledge upload list (Claude Project refresh)

Minimum set (copy from repo):

| Priority | File |
|----------|------|
| P0 | `docs/prompts/AGENT_OPERATING_SYSTEM.md` |
| P0 | `docs/prompts/ANCHOR_CURRENT.md` |
| P0 | `docs/governance/MANUAL_OPERATOR_PLAYBOOK.md` |
| P1 | `docs/governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md` |
| P1 | `docs/governance/PUBLIC_BETA_GO_NO_GO.md` |
| P1 | `docs/governance/practice-evidence/pb-9-day14-review/DAY14_REVIEW_DRAFT_2026-07-06.md` |
| P2 | `ARCHITECTURE.md` (first 120 lines + invariants) |
| P2 | `docs/governance/GOVERNANCE_DRIFT_RECONCILIATION.md` §1 |

**Last updated:** 2026-06-30
