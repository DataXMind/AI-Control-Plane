# Session anchor template (L5 — copy into every Cursor chat)

> **Use:** Paste this block as the **first message** (or pin) when starting a session.  
> **Policy:** [`AGENTS.md`](../../AGENTS.md) · [`CURSOR_RISK_POLICY.md`](../governance/CURSOR_RISK_POLICY.md) · Gold pattern: [`GP-01`](../governance/gold-patterns/GP-01-agent-session-memory.md)

---

## Canonical one-liner (paste at session start)

```text
AI Control Plane @ master 20e4fc3: Milestones A–C+ closed.
Public Beta IN_PROGRESS (PB-9 soak). Catalog v1.3.3 live.
Practice: PB-7 PASS · security@ PASS · tag v0.1.0-rc.1 @ c58b4cc · CHANGELOG/go-no-go merged (#119/#120).
Runtime catalog: 7 gates_remaining until maintainer bump @ PB-12 flip.
Critical path: PB-9 daily tick → Day 14 ~2026-07-06 → PB-12 ~2026-07-10.
PB-10 production soak deferred to GA (#78 post-flip). Trust verify_* scripts — not stale HTML.
```

---

## PB-12 operator gates — pinned checklist

> SSOT: [`TASK_AUDIT_REMAINING_2026-06-27.md`](../governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · [`PUBLIC_BETA_GO_NO_GO.md`](../governance/PUBLIC_BETA_GO_NO_GO.md) · **Claude full audit:** [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](../governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md) · `master` @ **`20e4fc3`**

**Chờ calendar / operator**

- [ ] **PB-9** daily tick — last **2026-06-28** · Day 14 review ~**2026-07-06**
- [x] **PB-7** CLEAN fork — **PASS** 2026-06-27
- [x] **security@** — live test **PASS** 2026-06-28
- [x] **OP-02 soak** — MSI repo log + VPS hourly PASS — [`vps-hourly-loop-verify-2026-06-28.md`](../governance/practice-evidence/pb-9-day14-review/artifacts/vps-hourly-loop-verify-2026-06-28.md)

**Practice done · catalog still lists until flip**

- [x] **PB-8** tag `v0.1.0-rc.1` @ `c58b4cc` (2026-06-28, pre–Day-14)
- [x] **CHANGELOG** `v0.1.0-rc.1` body — merged #120
- [x] **go/no-go** practice gates — merged #119

**Sau Day 14 PASS (~07-07–10)**

- [ ] Pre-flip: `export_openapi.py` (commit if diff) · smoke + verify
- [ ] **PB-12** human GO + operator signature (PB-10 defer recorded)
- [ ] **PB-10** / #78 — GA production soak **after** public flip

**Không claim**

- PB-7 trên MSI WARM (`dmin@MSI` @ `/mnt/d/Projects/…`) = PB-7 PASS
- PB-9 PASS / đóng #77 trước Day 14 (~07-06)
- `gates_remaining` = 0 trước maintainer catalog bump @ flip
- PB-10 blocks PB-12 @ 0.x beta (deferred GA — see go/no-go)
- CS-01/03/04 runtime drill
- Stale HTML: SHA `527eb5d`, "165 tests", gap Q1–Q3 open, PB-10 "needs confirm"

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/governance/status" | jq '.public_beta | {gates_remaining, gates_closed}'
```

---

## PACE verify (operator / pre-task)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke                   # 8/8
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh          # 1.3.3, 13 patterns
bash scripts/verify_openapi_runtime.sh                   # 3.1.0, 13 paths
```

---

## `gates_remaining` @ catalog v1.3.3 (runtime — not HTML)

| # | Gate | Practice @ 2026-06-28 | Blocks PB-12 @ 0.x? |
|---|------|------------------------|---------------------|
| 1 | PB-9 staging soak | 🔄 ticks through 28/06 | **Yes** — until Day 14 PASS |
| 2 | PB-7 clean fork | ✅ PASS | No (catalog until bump) |
| 3 | PB-8 rc tag | ✅ @ `c58b4cc` | No |
| 4 | PB-10 prod 30d | ❌ deferred GA | **No** |
| 5 | PB-6 OpenAPI publish | 🔄 static synced | Flip-day prominent link |
| 6 | security@ live | ✅ PASS | No |
| 7 | PB-12 human go/no-go | ⏳ ~07-10 | **Yes** |

---

## Drift — reject these claims

- `examples/docker-compose.yml` → `examples/minimal/docker-compose.yml`
- CI job `examples-smoke` → `examples-minimal-smoke`
- `"165 tests"` → ~**177** pytest @ master (use `pytest tests/ --collect-only -q`)
- `"PB-9 only gate"` → 7 `gates_remaining` in catalog
- `"HOÀN TẤT"` → engineering done; operator calendar open
- MSI WARM = PB-7 PASS
- `curl … > docs/openapi.json` → `python scripts/export_openapi.py` → `docs/openapi/openapi.json`
- PB-9 gap Scenario B/C default → calendar Day 14 **~07-06** (gap 06-22→25 documented)

---

## Claude / Cursor role this phase

- ✅ Day 14 template · go-no-go sync · CHANGELOG expand · CUR-04 VPS soak
- **Claude Projects:** [`CLAUDE_PROJECT_SETUP.md`](CLAUDE_PROJECT_SETUP.md) — Instructions · opener · knowledge list
- **Now:** PB-9 daily tick support · doc drift only (LOW)
- **~07-06:** Day 14 `RESULTS.md` when operator shares verdict
- **~07-10:** PB-12 narrative support — **human signature only**
- **DO NOT:** new feature code · close catalog gates · accelerate soak calendar · re-tag rc.1

---

## Anchor block (fill all fields)

```yaml
session_anchor:
  version: "1.0"
  date: "YYYY-MM-DD"
  baseline: "master @ <git-sha>"      # e.g. 20e4fc3
  risk: "LOW | MEDIUM | HIGH | CRITICAL"
  track: "feature | governance | ops | docs-only"
  gates_approved: []
  issue: "#NN or N/A"
  branch: "low/issue-short-desc or N/A"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md
    - docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md
    - ARCHITECTURE.md                # if non-trivial code
  durable_context:
    - docs/governance/PUBLIC_BETA_GO_NO_GO.md
    - docs/governance/PB9_STAGING_SOAK_LOG.md

file_allowlist:
  allowed:
    - path/to/file
  forbidden:
    - src/**                         # if docs-only

assumptions:
  - "Files I will touch: ..."
  - "If wrong, I will stop and ask: ..."

verify:
  - "ruff check src/ tests/"
  - "mypy src/ai_control_plane/ --strict"
  - "pytest tests/ -v"
  - "pytest tests/test_smoke.py -v -m smoke"

task: |
  One paragraph — goal, out of scope, done definition.

acceptance:
  - "[ ] ..."
```

---

## Example (governance docs-only)

```yaml
session_anchor:
  version: "1.0"
  date: "2026-06-28"
  baseline: "master @ 20e4fc3"
  risk: "LOW"
  track: "governance"
  gates_approved: ["docs-only — Karpathy track"]
  issue: "N/A"
  branch: "docs/example"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/governance/PUBLIC_BETA_GO_NO_GO.md
  durable_context:
    - docs/governance/L5_MATURITY_MODEL.md

file_allowlist:
  allowed:
    - docs/governance/**
    - docs/prompts/**
  forbidden:
    - src/**

assumptions:
  - "Docs-only; no API contract changes."

verify:
  - "git diff --name-only master | grep '^src/' → empty"
  - "pytest tests/test_smoke.py -v -m smoke"

task: |
  Update governance evidence or session anchor.

acceptance:
  - "[ ] Tier C artifact path updated"
```

---

## Runtime optional (operator)

```bash
export ACP_API_URL=http://localhost:8000
agentctl gov status --json | python3 -m json.tool
```

---

## Session close (Evolve)

- [ ] Issue/PR comment with outcome
- [ ] `LESSONS_LEARNED.md` if pitfall repeated (new P-xx row)
- [ ] `practice-evidence/` if operator ran hands-on steps
- [ ] Do **not** store sole copy of evidence in chat

**Last updated:** 2026-06-28 — VPS hourly verify · post #119/#120 · session anchor sync
