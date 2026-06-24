# Claude Prompt — Milestone C+ (architect depth)

> **Status:** **APPROVED** 2026-06-24 — issues [#67](https://github.com/DataXMind/AI-Control-Plane/issues/67)–[#72](https://github.com/DataXMind/AI-Control-Plane/issues/72)  
> **Parent:** Issue umbrella #37 (closed boundary @ PR #63)  
> **Baseline:** [`ACP_FULL_AUDIT_RECONCILIATION.md`](../governance/ACP_FULL_AUDIT_RECONCILIATION.md)  
> **Does NOT replace:** Boundary MVP delivered in PR #63

---

## Context for Claude

PR #63 delivered **SAPAL boundary closure**:

- `SenseAdapter.collect()` — aggregates `TelemetryEvent` counts (no OTel)
- `AnalyzeAdapter` — threshold heuristic (no Argos)
- `PredictAdapter` — risk_level enum (no Darts)
- `ActAdapter` — skips on high risk (no `PolicyEngine.evaluate()`)
- `LearnAdapter` — human approval gate, empty proposals
- `FileTelemetryStore`, `/apex/*`, `agentctl apex`

The **original** architect spec (see `acp_full_audit_report.html` pane ⑤ + Cursor prompt 3) required OTel IsolationForest, Argos-pattern agents, Darts forecasting, policy-gated act, `TelemetryStore.replay()`, cyanheads CI.

**Your task:** Produce architecture decisions + acceptance criteria for **Milestone C+** without violating 8 invariants.

---

## Required outputs (Claude)

### 1. ADR: `TelemetryStore.replay(from_ts, event_type?)`

- Interface on `TelemetryStore` ABC
- Interaction with `FileTelemetryStore` + hash-chain integrity
- Whether replay is filter-only or includes unseal validation

### 2. ADR: `sense.py` + OTel pipeline

- IsolationForest vs simpler detector for PoC
- `scripts/run_otel_collector.sh` + `config/otel-collector.yaml.example` schema
- Optional `[apex]` extras in `pyproject.toml` — pin versions

### 3. ADR: `analyze.py` Argos-pattern

Define interfaces for:

- Detect → Repair → Review → Mutate
- Input/output schemas (Pydantic models in `core/models.py` if new types)
- Approval gate integration (`ApprovalGate` vs HTTP `/policy/approve`)
- Retry / fail-closed semantics

### 4. ADR: `predict.py` Darts adapter

- Forecast target: token usage? anomaly rate? queue depth?
- Training data source: telemetry replay window
- Fallback when insufficient history

### 5. ADR: `act.py` policy-gate (BLOCKER-5)

Resolve circular dependency:

- Option A: snapshot `PolicyEngine` rules at loop start
- Option B: separate evaluation context / service account identity
- Option C: act only emits *proposals*; human or TS bridge executes

**Recommend one option** with sequence diagram.

### 6. ADR: cyanheads MCP E2E in CI

- Job layout: mock TS server vs containerized cyanheads
- Minimum test: `git_status` → policy allow → forwarder response
- Env: `ACP_MCP_GIT_URL`

### 7. Issue breakdown template

For each ADR, provide GitHub issue title + acceptance criteria (testable) for Cursor.

---

## Constraints (invariants)

| ID | Constraint |
|----|------------|
| #1 | No OSS PolicyEngine replacement |
| #2 | New types → `core/models.py` only |
| #3 | No git logic in Python MCP |
| #4 | CLI remains HTTP-only |
| #5 | OSS adapters invoked **from** `apex/`, not reverse |
| #6 | New HTTP routes only in `api/server.py` |
| D5 | Fail-closed on policy errors |
| D8 | MVP stubs already removed — C+ extends, does not re-stub |

---

## Non-goals (C+)

- Public Beta legal docs
- Production 30-day soak (track separately)
- Branch protection API (GAP-BP-1)

---

## References for Claude

```
@ARCHITECTURE.md
@docs/DEVELOPMENT_PROTOCOL.md
@docs/governance/acp_full_audit_report.html
@docs/governance/ACP_FULL_AUDIT_RECONCILIATION.md
@src/ai_control_plane/apex/
@src/ai_control_plane/core/telemetry.py
@docs/prompts/CLAUDE_PROMPT_TAB7_TELEMETRY.md
```

---

## Deliverable format

1. Markdown ADR pack → `docs/governance/MILESTONE_C_PLUS_ADR.md` (Claude drafts, human approves)
2. Updated issue list (C+ labels: `milestone-c-plus`, `spec-gap`)
3. Go/No-Go checklist distinct from boundary CLOSED

**Do not patch code** — architect packet only.
