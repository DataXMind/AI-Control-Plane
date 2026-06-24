# Milestone C+ — Architecture Decision Record (ADR pack)

**Document ID:** ACP-GOV-MC-PLUS-ADR-001  
**Version:** 1.0  
**Status:** DRAFT — pending human architect approve before Cursor execution  
**Baseline:** `master` @ post PR #65 (`a0ae399`)  
**Parent:** [`CLAUDE_PROMPT_MILESTONE_C_PLUS.md`](../prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md)  
**Supersedes:** Architect vision in `acp_full_audit_report.html` pane ⑤ (not delivered in PR #63 boundary)

---

## Executive summary

PR #63 closed **Milestone C boundary** (SAPAL wiring + file telemetry). **Milestone C+** adds architect depth without violating 8 invariants:

| ADR | Decision (recommended) |
|-----|------------------------|
| ADR-1 | Add `TelemetryStore.replay()` — filter + chain verify |
| ADR-2 | Phase C+ sense: Z-score on replay window first; OTel IF optional phase 2 |
| ADR-3 | Argos as 4-stage **protocol** with Pydantic envelopes; Review → ApprovalGate |
| ADR-4 | Darts forecast **token burn rate**; fallback to rolling mean |
| ADR-5 | **Option C** — act emits proposals only; execution via existing HTTP/MCP |
| ADR-6 | CI: `respx` mock cyanheads HTTP first; container job deferred |
| ADR-7 | Six GitHub issues (C+-1..C+-6) — implement only after per-issue approve |

---

## ADR-1: `TelemetryStore.replay()`

### Context

`sense.py` and `learn.py` need time-ordered subsets. Today: `list_events()` only.

### Decision

Add to `TelemetryStore` ABC:

```python
def replay(
    self,
    *,
    from_ts: datetime | None = None,
    to_ts: datetime | None = None,
    event_type: str | None = None,
    project_id: str | None = None,
) -> list[TelemetryEvent]:
    """Return filtered events in append order; verify chain before return."""
```

### Rules

- **Filter-only** on stored sealed events — no unseal/rehash.
- Call `verify_chain()` first; if false → raise `ControlPlaneError` (fail-closed).
- `InMemoryTelemetryStore` + `FileTelemetryStore` share filter logic in module helper.
- No new HTTP route in C+ v1 — apex uses injected store from `AppState`.

### Acceptance criteria

- [ ] `tests/test_telemetry.py` + `test_telemetry_persistence.py` cover replay filters
- [ ] Tampered chain → replay raises
- [ ] mypy strict on new signature

---

## ADR-2: `sense.py` + OTel pipeline

### Context

HTML spec: OTel IsolationForest. MVP used event counts.

### Decision — phased

**Phase C+-2a (PoC):** `SenseAdapter` uses `store.replay()` + simple Z-score on `payload` numeric fields (e.g. token counts if present). No new ML deps.

**Phase C+-2b (optional):** `[apex]` extras:

```toml
[project.optional-dependencies]
apex = ["scikit-learn>=1.4", "opentelemetry-api>=1.24"]
```

- `scripts/run_otel_collector.sh` — already stub; add `config/otel-collector.yaml.example` (OTLP gRPC → logging exporter for dev).
- IsolationForest on feature vector `[event_count_1h, error_rate, unique_agents]` — **only when `[apex]` installed**.

### Acceptance criteria

- [ ] Z-score path works without `[apex]` extra
- [ ] `otel-collector.yaml.example` documented in README
- [ ] sklearn path skipped gracefully with structlog warning if extra missing

---

## ADR-3: `analyze.py` Argos-pattern

### Context

Detect → Repair → Review → Mutate requires clear contracts.

### Decision

New models in `core/models.py`:

```python
class AnalyzeFinding(BaseModel): ...      # Detect output
class RepairProposal(BaseModel): ...    # Repair output
class ReviewDecision(BaseModel): ...    # Review output (approved: bool)
class MutateResult(BaseModel): ...      # Mutate output (applied: bool)
```

Pipeline in `AnalyzeAdapter.analyze(sense_output) -> dict`:

1. **Detect** — classify anomalies from sense features
2. **Repair** — propose config-safe remediations (no direct YAML write)
3. **Review** — if `requires_approval`: call `ApprovalGate` (in-process when loop runs in API worker) OR return `requires_approval=True` for HTTP path
4. **Mutate** — only if Review approved; still **no auto YAML** — emit proposal dict for Learn/human

### Fail-closed

- Any stage exception → return `{"status": "failed", "stage": "detect|repair|review|mutate"}`  
- Review deny → no Mutate

### Acceptance criteria

- [ ] 4-stage unit tests with mocked ApprovalGate
- [ ] No filesystem writes in analyze/
- [ ] Invariant #1 preserved

---

## ADR-4: `predict.py` Darts adapter

### Context

Forecast what SAPAL should optimize.

### Decision

- **Target:** project-level **token burn rate** (events/hour with `event_type=TOOL_CALL` and numeric payload).
- **Training window:** `replay(from_ts=now-7d)` minimum 24 points; else fallback.
- **Fallback:** rolling 24h mean — no Darts import required.
- **Library:** `darts>=0.27` in `[apex]` optional extra only.

### Acceptance criteria

- [ ] Fallback path tested without darts installed
- [ ] With darts + synthetic series → forecast dict returned
- [ ] predict never calls external network

---

## ADR-5: `act.py` policy-gate (BLOCKER-5)

### Options evaluated

| Option | Pros | Cons |
|--------|------|------|
| A — snapshot PolicyEngine rules | Deterministic loop | Stale if YAML changes mid-loop |
| B — service account identity | Real-time policy | New identity type; scope creep |
| **C — proposals only** | No circular exec; uses existing bridge | Human/TS step required |

### Decision: **Option C**

`ActAdapter.execute()` returns:

```python
{
  "executed": False,
  "proposals": [{"tool_name": "...", "args": {...}, "policy_eval_required": True}],
  "status": "proposal_only",
}
```

Actual tool execution:

- TypeScript PolicyClient + MCP (existing path), OR
- Future `POST /apex/execute` (C++ scope — **not in C+ v1**)

### Sequence (mermaid)

```mermaid
sequenceDiagram
  participant Loop as SapalLoop
  participant Act as ActAdapter
  participant API as api/server
  participant MCP as mcp/git_server
  Loop->>Act: execute(prediction)
  Act-->>Loop: proposals (no side effects)
  Note over Loop: Operator or TS bridge evaluates policy + executes
  MCP->>API: POST /policy/evaluate
  API-->>MCP: allowed/deny
```

### Acceptance criteria

- [ ] act never imports `core.policies` from cli path
- [ ] High-risk predictions still emit proposals but `policy_eval_required=True`
- [ ] Document in ARCHITECTURE §apex

---

## ADR-6: cyanheads MCP E2E in CI

### Context

Production claim needs Python facade → HTTP forwarder → response.

### Decision — phased

**Phase C+-6a:** Extend `tests/test_mcp_http_transport.py`:

- `respx` mock `ACP_MCP_GIT_URL` cyanheads JSON-RPC
- Full path: `tools/call` → policy allow → forwarder HTTP → result

**Phase C+-6b (deferred):** Docker job with cyanheads image — Public Beta prep.

### CI env

```yaml
env:
  ACP_CONFIG_DIR: tests/fixtures/config
  ACP_MCP_GIT_URL: http://127.0.0.1:9xxx  # respx mock
```

### Acceptance criteria

- [ ] New test in CI Full suite job
- [ ] No live git binary in Python tests
- [ ] Invariant #3 preserved

---

## ADR-7: GitHub issue breakdown (C+-1..C+-6)

Create **only after human approves this ADR pack**. Label: `milestone-c-plus`, `spec-gap`.

| ID | Title | Acceptance (summary) |
|----|-------|----------------------|
| **C+-1** | TelemetryStore.replay() API | ADR-1 tests green |
| **C+-2** | Sense Z-score + otel-collector.example | ADR-2a + yaml example |
| **C+-3** | Analyze Argos 4-stage protocol | ADR-3 models + tests |
| **C+-4** | Predict Darts token burn + fallback | ADR-4 optional extra |
| **C+-5** | Act proposal-only policy path | ADR-5 Option C |
| **C+-6** | cyanheads MCP E2E CI (respx) | ADR-6a test |

---

## Go/No-Go — Milestone C+ start

| Gate | Required |
|------|----------|
| Milestone C boundary CLOSED | ✅ PR #63 |
| This ADR approved by human | ⏸ |
| Doc drift HIGH items fixed | ✅ PR #66 (this branch) |
| #9, #39 remain tracked as B+ | ✅ separate from C+ |
| Each C+-issue approved before code | ⏸ |

**Verdict:** **NO-GO for code** until ADR human sign-off. **GO for issue creation** after sign-off.

---

## Sign-off

| Role | Name | Date | Approve |
|------|------|------|---------|
| Architect (Claude packet) | Cursor draft | 2026-06-24 | ☐ |
| Human maintainer | | | ☐ |

---

**Last updated:** 2026-06-24
