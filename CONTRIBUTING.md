# Contributing to AI Control Plane

## Quick Start for Contributors (5 minutes)

New to ACP? Start here before reading the full governance docs.

**Evaluate or integrate (not contributing)?** [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — two doors, 5 minutes.  
**Fork vs clone map:** [`docs/DEVELOPER_SCENARIOS.md`](docs/DEVELOPER_SCENARIOS.md) — advanced / operator paths.

### Your First Contribution Path

1. **Bug fix or docs:** Follow this guide completely.
2. **New feature:** Read AGENTS.md and CURSOR_RISK_POLICY.md first, then return here.
3. **Security issue:** Do NOT open a public issue. Email security@dataxmind.com — see SECURITY.md.

### Minimum Viable Setup

```bash
git clone https://github.com/DataXMind/AI-Control-Plane
cd AI-Control-Plane
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke  # should be 8/8 PASS
bash scripts/verify_governance_memory.sh
```

**Operator / staging (API running on :8000):**

```bash
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_ghcr_catalog.sh   # SKIP if no GHCR image pulled
```

### The One Rule

**Every PR must pass smoke gate (8/8) before review.**
Smoke fail → fix first → then request review. Reviewers will not merge failing PRs.

### What You Can Do Without Reading All Docs

- Fix typos in docs/ → open PR directly
- Add examples in examples/ → open PR, describe what you tested
- Report bugs → use GitHub Issue templates (bug_report template)

### What Requires Reading Governance Docs First

- Changes to src/ai_control_plane/ → read AGENTS.md
- Changes to policy behavior → read CURSOR_RISK_POLICY.md §ABAC
- New CI gates → discuss in issue first

### AI-Assisted Contributions (Cursor / Claude Code)

If using AI coding assistants, paste session anchor at start:
See [`docs/prompts/ANCHOR_CURRENT.md`](docs/prompts/ANCHOR_CURRENT.md) (living snapshot) or [`SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md) for full YAML.

**Operator / pilot deploy:** [`examples/minimal/PRODUCTION_DEPLOY.md`](examples/minimal/PRODUCTION_DEPLOY.md) · [`MANUAL_OPERATOR_PLAYBOOK.md`](docs/governance/MANUAL_OPERATOR_PLAYBOOK.md)

---

Thank you for contributing. This project is a **governance control plane** — changes that weaken fail-closed behavior or bypass invariants will be rejected.

**Process SSOT:** [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) (PACE) · [docs/governance/CURSOR_RISK_POLICY.md](docs/governance/CURSOR_RISK_POLICY.md) (L2 risk)

---

## Before you start

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) — **8 hard invariants** are non-negotiable.
2. Read [AGENTS.md](AGENTS.md) — agent entry, session anchor, memory tiers (ML5).
3. Read [CLAUDE.md](CLAUDE.md) — L0 behavioral constitution (Karpathy 4).
4. Read [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) — PACE workflow, 9-step executor path, **smoke gate §5.5**.
5. Read [docs/governance/CURSOR_RISK_POLICY.md](docs/governance/CURSOR_RISK_POLICY.md) — classify task risk (L2) **before** coding.
6. Open sessions with [`docs/prompts/ANCHOR_CURRENT.md`](docs/prompts/ANCHOR_CURRENT.md) or [`SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md).
7. Harness vs policy boundary: [docs/governance/ECC_ACP_INTEGRATION_ANALYSIS.md](docs/governance/ECC_ACP_INTEGRATION_ANALYSIS.md) (48H SSOT — no ECC plugin import).
8. Open or link a GitHub issue (`bug`, `spec-gap`, `debt`, `quality`) — **questions** → [GitHub Discussions](https://github.com/DataXMind/AI-Control-Plane/discussions).

---

## Development setup

```bash
git clone https://github.com/DataXMind/AI-Control-Plane
cd AI-Control-Plane
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
export ACP_CONFIG_DIR=tests/fixtures/config
```

---

## New task workflow (PACE + L2)

| Step | Action |
|------|--------|
| **P**lan | Classify risk LOW / MEDIUM / HIGH / CRITICAL ([CURSOR_RISK_POLICY](docs/governance/CURSOR_RISK_POLICY.md)); list files, assumptions, verify command |
| **A**ct | Branch per naming below; respect file allowlists per risk level |
| **C**heck | Gates below (+ `shipped_config` for HIGH+) |
| **E**volve | PR body; individual `Closes #N`; update docs if contracts change |

**Docs-only (LOW):** `*.md`, `docs/**` only — no `src/` without reclassifying to MEDIUM.

---

## Branch naming

```
low/docs-fix-typo
low/governance-p13-killswitch-v132
medium/add-cli-status-filter
high/core-policies-abac-role-weight
```

Pattern: `{risk}/{short-desc}` — never commit directly to `master`.

---

## Required gates (every PR)

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -q
pytest -m smoke -q
bash scripts/verify_governance_memory.sh
```

**HIGH / CRITICAL** (when touching API contracts or shipped config):

```bash
pytest -m shipped_config -q
```

CI must pass **Smoke gate** and **Full suite**.

Optional local hook: `pre-commit run --all-files`

---

## PR checklist

Copy into PR body:

- [ ] Risk level identified (LOW / MEDIUM / HIGH / CRITICAL)
- [ ] Files touched listed; assumptions stated explicitly
- [ ] Verify gate passed: `ruff` + `mypy --strict` + `pytest` + smoke (+ `shipped_config` if HIGH+)
- [ ] Each issue listed individually (`Closes #N` — **not** ranges)
- [ ] No new types outside `core/models.py` (Invariant #2)
- [ ] No OSS policy engines imported into `core/` (Invariant #1)
- [ ] `ARCHITECTURE.md` updated if HTTP or config loading changed
- [ ] `bash scripts/verify_governance_memory.sh` passed (governance / L5 docs)

Template: [`.github/pull_request_template.md`](.github/pull_request_template.md)

---

## 8 invariants (never violate)

1. **`core/policies.py`** — custom `PolicyEngine` only; no OSS replacement.
2. **`core/models.py`** — all data contracts here only.
3. **`mcp/git_server.py`** — facade only (no Git logic in Python).
4. **`cli/`** — HTTP calls only (no direct `core/` policy imports).
5. **`apex/`** — SAPAL loop; OSS tools called **from** `apex/`.
6. **`api/`** — sole cross-language bridge to TypeScript.
7. **`core/quota.py`** — `QuotaStore` ABC, swappable backend.
8. **`config/`** — shipped defaults; runtime override via `ACP_CONFIG_DIR`.

---

## Design principles (fork-friendly)

### `/health` vs `/governance/status`

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness/readiness — k8s, CI, load balancers (`status`, `policy_rules_count`) |
| `GET /governance/status` | Human/agent governance checklist — milestones, case studies, lessons (L5) |

Do not bloat `/health` with governance metadata. Forks should keep this separation.

### First check after deployment

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
curl -sf "$ACP_API_URL/governance/status" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['governance_version'], len(d['lessons_patterns']), 'patterns')"
bash scripts/verify_governance_status_runtime.sh
```

Operator runbook: [docs/RUNBOOK.md](docs/RUNBOOK.md)

---

## Running tests

```bash
pytest tests/ -v                      # full suite
pytest -m smoke -v                    # smoke gate (8 tests)
pytest -m shipped_config -v             # shipped config parity (HIGH+)
pytest tests/test_api_contract_snapshot.py -v   # API contract snapshots
```

---

## 6-layer governance (Karpathy)

| Layer | Doc |
|-------|-----|
| L0 | [CLAUDE.md](CLAUDE.md) |
| L1 | [ARCHITECTURE.md](ARCHITECTURE.md) |
| L2 | [docs/governance/CURSOR_RISK_POLICY.md](docs/governance/CURSOR_RISK_POLICY.md) |
| L3 | [.cursorrules](.cursorrules) · this file |
| L4 | CI gates · [docs/CONTRACT_TESTS.md](docs/CONTRACT_TESTS.md) |
| L5 | [docs/governance/LESSONS_LEARNED.md](docs/governance/LESSONS_LEARNED.md) · [AGENTS.md](AGENTS.md) |

---

## PR rules

- Target `master` via pull request only (no direct pushes).
- State **risk level** per [CURSOR_RISK_POLICY.md](docs/governance/CURSOR_RISK_POLICY.md).
- Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- Link issues with individual `Closes #N` (not ranges).
- Update `ARCHITECTURE.md` when HTTP contracts or config loading change.

---

## Questions?

- **How-to / design questions:** [GitHub Discussions](https://github.com/DataXMind/AI-Control-Plane/discussions)
- **Bugs and spec gaps:** [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues)
- **Security:** [SECURITY.md](SECURITY.md) — private report path only

---

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
