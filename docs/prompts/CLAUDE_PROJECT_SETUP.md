# Claude Project — setup guide (ACP Public Beta)

**Document ID:** ACP-PROMPT-CLAUDE-PROJECT-SETUP-001  
**Audience:** Maintainer · operator · Claude Projects (claude.ai)  
**Phase:** PB-9 staging soak → PB-12 flip  
**Baseline:** `master` @ **`4210ad2`** · catalog **v1.5.0** · **17** patterns · pytest **181**  
**Companion:** [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) · [`CLAUDE_CODEX_PLAYBOOK.md`](CLAUDE_CODEX_PLAYBOOK.md) · [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) (Cursor)

> **Use:** One-time Project setup on claude.ai + paste **opener** at every new conversation.  
> **Refresh:** Re-upload knowledge files after significant `git pull` on `master`.

---

## 1. How Claude Projects work (read first)

| Component | Purpose | ACP implication |
|-----------|---------|-----------------|
| **Project Instructions** | Persistent behavior (role, rules, tone) | Keep **short** — behavior only, not long facts |
| **Project Knowledge** | Uploaded files Claude retrieves (RAG) | **Static snapshot** — not live GitHub; re-upload when repo changes |
| **Conversations** | Share Instructions + Knowledge | New chat **does not** inherit prior chat facts — use opener + knowledge |
| **vs Cursor** | Claude Project = advise · draft · audit | Does **not** run `git`, `pytest`, `curl`, commit, or flip gates |

**Design rule:** One Project = one job → **“ACP Public Beta — Governance & Operator Advisor”**.

---

## 2. Create the Project (once)

1. claude.ai → **Projects** → **New project**
2. Name: `ACP Public Beta — Governance Advisor`
3. Paste **§3 Project Instructions** into **Set project instructions**
4. Upload files from **§5 Knowledge file list** (rename with prefixes as in §5.1)
5. **Test retrieval:** ask *“List three HIGH findings from §14 second-pass audit in PROJECT_STATUS_FULL_TECHNICAL_REPORT.”*

---

## 3. Project Instructions (copy entire block)

Paste into **Project → Set project instructions**:

```xml
<role>
You are the governance and Public Beta operator advisor for AI Control Plane (DataXMind/AI-Control-Plane).
Phase: PB-9 staging soak → Day 14 review (~2026-07-06) → PB-12 human go/no-go (~2026-07-10).
You advise, draft docs, audit prompts, and prepare review materials. You do NOT execute git, pytest, curl, deploy, flip visibility, close catalog gates, or tick PB-9 dates without explicit operator confirmation.
</role>

<ssot_priority>
1. AGENT_OPERATING_SYSTEM.md (upload as 00_AOS.md)
2. ANCHOR_CURRENT.md
3. PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md
4. MANUAL_OPERATOR_PLAYBOOK.md + PUBLIC_BETA_GO_NO_GO.md
Runtime truth: governance_catalog.py → GET /governance/status (operator verifies on host).
Reject stale HTML snapshots (527eb5d, "165 tests", "177 tests" — use **181** @ `ANCHOR_CURRENT.md`).
</ssot_priority>

<current_state one_liner>
Milestones A–C+ CLOSED. Public Beta IN_PROGRESS. PB-9 tick through 2026-06-30; need 07-01..05.
gates_blocking_pb12: PB-9, PB-12. gates_remaining: 7 until flip bump.
Critical path: Day 14 ~2026-07-06 → pre-flip ~07-07 → PB-12 ~2026-07-10.
PB-10 deferred GA (#78). 181 pytest, smoke 8/8. Practice PASS ≠ catalog closed until H1-06.
</current_state>

<hard_rules>
- Practice PASS ≠ remove item from gates_remaining until catalog bump @ PB-12 flip.
- Do NOT claim PB-9 PASS before Day 14 calendar (~2026-07-06).
- Do NOT tick future PB-9 dates; operator says "đã tick ngày YYYY-MM-DD" only.
- MSI WARM dev machine ≠ PB-7 CLEAN PASS.
- PB-9 Day 14 = ~2026-07-06 from soak start 2026-06-22; reject Scenario B (07-10) unless new SEV-1/2.
- Do not propose new src/ features; Karpathy track = docs-only through PB-9 review.
- Paths: examples/minimal/docker-compose.yml; CI job examples-minimal-smoke; OpenAPI via scripts/export_openapi.py → docs/openapi/openapi.json.
- When uncertain, state what the operator must verify and which repo artifact path to update.
</hard_rules>

<output_style>
Structured markdown. Cite project knowledge filenames. Separate: Fact / Practice / Catalog / Calendar / Recommendation.
Flag drift explicitly. Vietnamese or English per user message.
</output_style>
```

---

## 4. First message — new conversation opener

Paste as the **first message** in every new Project conversation (even with Instructions set):

```text
[ACP Public Beta — session start]

Baseline: master @ 4210ad2 · catalog v1.5.0 · 17 patterns · pytest 181 · smoke 8/8.

Đọc AGENT_OPERATING_SYSTEM.md và ANCHOR_CURRENT.md trong project knowledge trước khi trả lời.

Xác nhận ngắn (bullet):
1) Critical path và gate THỰC SỰ block PB-12 @ 0.x beta
2) Practice PASS vs gates_remaining — một câu
3) Operator HÔM NAY vs CHỜ calendar (tick 07-01..05, Day 14 ~07-06)
4) Ba drift claim cần reject (SHA cũ, test count cũ, PB-10 blocks beta)

Sau đó hỏi focus: PB-9 tick draft, Day 14 RESULTS, PB-12 memo, hay audit prompt?

Hard rules: không đóng gates_remaining · không tick ngày tương lai · không code src/ mới · không execute git/pytest.
```

**After opener:** state intent in one line, e.g. *“Focus: draft Day 14 RESULTS from soak logs”* or *“Audit this prompt for drift.”*

---

## 5. Knowledge file list

Upload from repo paths below. Prefer **≤12 files** focused; remove stale uploads when refreshing.

### 5.1 Recommended upload set (12 files)

| Upload name (prefix) | Repo path |
|----------------------|-----------|
| `00_AOS_AGENT_OPERATING_SYSTEM.md` | [`docs/prompts/AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) |
| `01_ANCHOR_CURRENT.md` | [`docs/prompts/ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) |
| `02_SSOT_PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md` | [`docs/governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](../governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md) |
| `03_MANUAL_OPERATOR_PLAYBOOK.md` | [`docs/governance/MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md) |
| `03_OPERATOR_PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` | [`docs/governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) |
| `04_OPERATOR_PUBLIC_BETA_GO_NO_GO.md` | [`docs/governance/PUBLIC_BETA_GO_NO_GO.md`](../governance/PUBLIC_BETA_GO_NO_GO.md) |
| `05_OPERATOR_TASK_AUDIT_REMAINING_2026-06-27.md` | [`docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md`](../governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) |
| `08_RECON_HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md` | [`docs/governance/HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md`](../governance/HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md) |
| `09_RECON_ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md` | [`docs/governance/ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](../governance/ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md) |
| `10_REF_MANUAL_OPERATOR_PLAYBOOK.md` | [`docs/governance/MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md) |
| `11_PB9_PB9_STAGING_SOAK_LOG.md` | [`docs/governance/PB9_STAGING_SOAK_LOG.md`](../governance/PB9_STAGING_SOAK_LOG.md) |
| `12_PB9_PB9_DAY14_REVIEW_TEMPLATE.md` | [`docs/governance/PB9_DAY14_REVIEW_TEMPLATE.md`](../governance/PB9_DAY14_REVIEW_TEMPLATE.md) |

### 5.2 Tier optional (add when needed)

| Repo path | When |
|-----------|------|
| [`docs/governance/PROJECT_STATUS_AUDIT_FOR_CLAUDE.md`](../governance/PROJECT_STATUS_AUDIT_FOR_CLAUDE.md) | Shorter companion to full report |
| [`docs/governance/PB9_SOAK_ITERATION_LOG.md`](../governance/PB9_SOAK_ITERATION_LOG.md) | MSI machine log snapshot — refresh often |
| [`docs/governance/OPEN_SOURCE_READINESS.md`](../governance/OPEN_SOURCE_READINESS.md) | Phase 0→3 visibility |

### 5.3 Do not upload as SSOT

| Avoid | Why |
|-------|-----|
| [`ACP_HANDOFF_FOR_NEW_CONVERSATION_2026-06-27.md`](../governance/ACP_HANDOFF_FOR_NEW_CONVERSATION_2026-06-27.md) (archived, Claude UI export) | Stale @ `527eb5d` — use [`HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md`](../governance/HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md) |
| `docs/governance/*.html` | Stale counts/SHAs — use `*_RECONCILIATION.md` instead |
| Entire `src/`, `tests/`, `.github/` | Too large; retrieval noise |
| `CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md` alone | Partially stale — prefer FULL report + TASK_AUDIT |

---

## 6. Step-by-step per conversation

1. Paste **§4 opener**
2. State **one task** (tick rules · Day 14 prep · PB-12 draft · drift audit)
3. Paste **new evidence** if any (log excerpt, *"đã tick ngày …"*)
4. Ask for output with **repo file paths** to update (Claude drafts; Cursor/operator commits)
5. Close with: *“3-bullet summary + human-only actions”*

### Milestone map

| When | Claude Project | Operator / Cursor |
|------|----------------|-------------------|
| Daily | Tick rules Q&A; soak evidence layers | OP-01 tick · OP-02 soak |
| ~2026-07-06 | Draft `pb-9-day14-review/RESULTS.md` | Verdict · close #77 if PASS |
| ~2026-07-07 | Pre-flip checklist narrative | `export_openapi.py` · smoke 8/8 · `verify_*` |
| ~2026-07-10 | PB-12 GO memo (PB-10 defer text) | **Human signature** · public flip |

---

## 7. Refresh policy

After `git pull` on `master` when any of these change:

- `PROJECT_STATUS_FULL_TECHNICAL_REPORT_*`
- `SESSION_ANCHOR_TEMPLATE.md`
- `PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` · `PUBLIC_BETA_GO_NO_GO.md`
- `TASK_AUDIT_REMAINING_*` · `PB9_STAGING_SOAK_LOG.md`

**Actions:**

1. Re-upload replaced files to Project knowledge (delete old versions)
2. Update **§3** `<current_state>` and **§4** baseline SHA if commit moved
3. First message in next chat: *“Knowledge refreshed @ SHA …”*

---

## 8. Drift guard (reject in Claude Project)

| Stale claim | Correct SSOT |
|-------------|--------------|
| `ac5f017` / `527eb5d` / `8a4e7fa` as current baseline | **[`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md)** (`4210ad2` @ 2026-07-01) |
| `"165 tests"` / `"156 tests"` / `"177 tests"` | **181** pytest (`pytest --collect-only -q`) |
| `"PB-9 only gate remaining"` | **7** `gates_remaining` |
| MSI WARM = PB-7 PASS | PB-7 needs **CLEAN** machine `RESULTS.md` |
| PB-10 blocks PB-12 @ 0.x beta | **Deferred GA** — #78 post-flip |
| `examples/docker-compose.yml` | `examples/minimal/docker-compose.yml` |
| `curl > docs/openapi.json` | `python scripts/export_openapi.py` |
| Day 14 default = 2026-07-10 | **~2026-07-06** (soak start 2026-06-22) |
| HTML `acp_status_audit_analysis.html` as live state | Use reconciliation + FULL report |
| `ACP_HANDOFF_FOR_NEW_CONVERSATION_2026-06-27.md` (archived, UI @ `527eb5d`) | [`HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md`](../governance/HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md) |

---

## 9. Three soak evidence layers (do not conflate)

| Layer | Path | Owner |
|-------|------|-------|
| Human daily | `docs/governance/PB9_STAGING_SOAK_LOG.md` | Operator tick |
| MSI machine | `docs/governance/PB9_SOAK_ITERATION_LOG.md` | `restart_soak_loop.sh --repo-log` |
| VPS machine | `practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log` | `acp-soak.service` |

---

## 10. Related documents

- [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](../governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md)
- [`HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md`](../governance/HANDOFF_UI_DRIFT_RECONCILIATION_2026-06-28.md)
- [`MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md)
- [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md)
- [`GP-01`](../governance/gold-patterns/GP-01-agent-session-memory.md) — session memory pattern

**Last updated:** 2026-06-28 @ `20e4fc3`
