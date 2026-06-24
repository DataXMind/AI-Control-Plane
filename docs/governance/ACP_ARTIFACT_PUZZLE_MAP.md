# ACP — Artifact Puzzle Map (Claude arch → execution)

**Document ID:** ACP-GOV-PUZZLE-001  
**Created:** 2026-06-24  
**Purpose:** Giải thích cách các mảnh ghép (HTML artifacts, markdown governance, Claude prompts, GitHub issues, Cursor execution) khớp với nhau.

---

## 1. Thứ bậc sự thật (DEVELOPMENT_PROTOCOL §3)

```text
ARCHITECTURE.md + 8 invariants
    ↓
Claude consolidated architecture (HTML) — decision matrix V1∪V2
    ↓
DEVELOPMENT_PROTOCOL.md — PACE, 9-step, smoke gate
    ↓
GitHub issues (acceptance criteria)
    ↓
docs/prompts/CLAUDE_PROMPT_*.md — task packets cho Cursor
    ↓
Code on master (actual behavior)
```

**Quy tắc audit nghiêm khắc:** Khi HTML artifact / issue title / Claude prompt **mâu thuẫn code**, code + `ARCHITECTURE.md` post-merge thắng — artifact cũ phải được đánh dấu **stale** hoặc reconciliation.

---

## 2. Lớp artifact và vai trò

| Lớp | File(s) | Owner | Output |
|-----|---------|-------|--------|
| **Architecture V3** | `ai_control_plane_consolidated_architecture.html` | Claude | 8 invariants, module tree, milestone A/B/C boundaries |
| **Workflow** | `cursor_workflow_prompt_system.html`, `cursor_workflow_continued.html` | Claude | Build order Milestone A; apex stubs |
| **Phase 2 audit** | `phase2_adjusted_prompts.html`, `PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md` | Claude + Cursor | P0 fixes, Path B merge, 38-item DoD |
| **Reconcile** | `cursor_claude_reconcile_analysis.html` | Claude | GAP-* IDs, 88% match narrative |
| **Telemetry / smoke** | `tab7_telemetry_spec_and_smoke_audit.html`, `CLAUDE_PROMPT_TAB7_TELEMETRY.md` | Claude | Hash-chain spec, SMK matrix |
| **Tool naming** | `CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md` | Claude | P0-2b Option A decision |
| **Full audit (snapshot)** | `acp_full_audit_report.html` | Claude | Baseline `fc296d4` — **STALE** after PR #63/#64 |
| **Reconciliation (live)** | `ACP_FULL_AUDIT_RECONCILIATION.md` | Cursor | master @ `a285539` truth |
| **Sprint plans** | `MILESTONE_B_BACKLOG.md`, `MILESTONE_C_SPRINT_PLAN.md` | Agent + human | Execution tracking |
| **Claude next** | `docs/prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md` | Claude (planned) | C+ depth: OTel, Argos, Darts, cyanheads CI |

---

## 3. Claude prompts — map tới execution

### Phase 1 (đã thực hiện)

| Prompt | Issue | Delivered | PR / commit |
|--------|-------|-----------|-------------|
| `CLAUDE_PROMPT_TAB7_TELEMETRY.md` | #23 | `TelemetryWriter`, hash-chain, `InMemoryTelemetryStore` | Milestone A |
| `CLAUDE_PROMPT_SMOKE_AUDIT.md` | #25 | SMK-01..06c (8 tests), `scripts/smoke_acp.sh` | Milestone A/B |
| `CLAUDE_PROMPT_CONFIG_TOOL_NAMING.md` | #8 | `core/tool_names.py`, Option A adapter | PR #48 |

### `acp_full_audit_report.html` — 3 Cursor prompts (baseline `fc296d4`)

| Prompt | Intent @ snapshot | Execution status @ `a285539` |
|--------|-------------------|------------------------------|
| **Cursor 1** — Close #8, #35, #45; label #37 | Issue hygiene pre-MC | ✅ Done (bulk close + PR #64: #37, #3, #13, #53–#62) |
| **Cursor 2** — HIGH doc drift (API surface, stores, PHASE1 §4.2) | Docs sync pre-MC | ⚠️ **Partial** — stores/execution updated PR #64; API surface table + PHASE1 §4.2 **still stale** |
| **Cursor 3** — MED drift + MC sub-issues (OTel, Argos, Darts) | Architect-grade Milestone C | ⚠️ **Scope adjusted** — MC #52–#62 created but implemented as **MVP SAPAL** (PR #63), not OTel/Argos/Darts |

### Claude Prompt 3 (trong HTML) vs thực tế MC issues

| HTML đề xuất | Issue thực tế | Code PR #63 |
|--------------|---------------|-------------|
| MC-1: OTel IsolationForest | #53 SenseAdapter.collect | Heuristic aggregate telemetry — **không OTel** |
| MC-2: Argos Detect→Repair→Review→Mutate | #54 AnalyzeAdapter | Threshold `anomaly_event_threshold` — **không Argos** |
| MC-3: Darts forecasting | #55 PredictAdapter | `risk_level` heuristic — **không Darts** |
| MC-4: PolicyEngine-gated act | #56 ActAdapter | Skip high risk — **không gọi PolicyEngine** |
| MC-5: Learn + human approval | #57 LearnAdapter | `proposals: []` — đúng human gate, chưa adaptation logic |
| MC-0: replay API + otel + cyanheads CI | Không tạo MC-0 | `FileTelemetryStore` yes; `replay()` **no**; otel script stub; cyanheads CI **no** |

**Kết luận puzzle:** Issue map MC-1..11 **đúng tên module**, nhưng **acceptance criteria trong HTML Prompt 3** (Claude architect vision) **không được implement** — chỉ boundary milestone "no NotImplementedError + wiring".

---

## 4. Pipeline PACE ↔ artifacts

```mermaid
flowchart TB
  subgraph claude [Claude layer]
    A1[consolidated_architecture.html]
    A2[audit HTML + GAP IDs]
    A3[CLAUDE_PROMPT packets]
  end
  subgraph human [Human]
    H[Approve scope / merge PR]
  end
  subgraph cursor [Cursor layer]
    C1[9-step + gates]
    C2[PR diff]
    C3[governance markdown sync]
  end
  subgraph github [GitHub]
    I[issues + CI]
    M[master]
  end
  A1 --> A2 --> A3 --> H
  H --> C1 --> C2 --> I
  C2 --> M
  C3 --> M
  M --> A2
```

**Deviation đã chấp nhận:** Path B monolithic PRs (#48, #63) thay Rule 1 "1 task = 1 PR" — documented in `PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md` (W1 waived).

---

## 5. Khi nào dùng artifact nào

| Câu hỏi | Đọc |
|---------|-----|
| Invariant có bị vi phạm không? | `ARCHITECTURE.md` + code |
| Milestone A/B/C đã xong chưa? | `MILESTONE_*_SPRINT_PLAN.md`, `ACP_FULL_AUDIT_RECONCILIATION.md` |
| Claude vision apex đầy đủ? | `acp_full_audit_report.html` pane ⑤ + `CLAUDE_PROMPT_MILESTONE_C_PLUS.md` |
| Cursor task tiếp theo? | `ACP_CURSOR_PROMPT_PACKET_POST_MC.md` |
| Smoke / protocol gates? | `DEVELOPMENT_PROTOCOL.md` §5.5 |

---

**Supersedes:** Nothing. Complements `acp_full_audit_report.html` (historical snapshot only).
