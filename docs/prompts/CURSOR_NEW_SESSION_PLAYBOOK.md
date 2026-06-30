# Cursor — New session & new account playbook

**Document ID:** ACP-PROMPT-CURSOR-NEW-SESSION-001  
**Parent:** [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md)  
**Audience:** New Cursor subscriber · new machine · fork maintainer

---

## 1. What Cursor auto-loads (Tier A)

| Source | Loaded when | Content |
|--------|-------------|---------|
| [`.cursorrules`](../../.cursorrules) | Every chat | L0–L5 Karpathy stack |
| [`.cursor/rules/*.mdc`](../../.cursor/rules/) | By glob / `alwaysApply` | Scoped: `core-critical`, `governance-docs`, `acp-l5-memory` |
| User rules (Cursor Settings) | Every chat | Your org preferences — **add ACP rules below** |
| [`AGENTS.md`](../../AGENTS.md) | When @ or agent reads | Entry point — point agents to AOS |

**Cursor does NOT auto-load:** `ANCHOR_CURRENT.md`, soak logs, or live `git sha` — **you paste anchor**.

---

## 2. One-time setup (new account / new machine)

### 2.1 Clone + Python env

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2.2 Docker (PACE / verify)

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
```

### 2.3 Cursor user rules (recommended paste)

Add in **Cursor → Settings → Rules**:

```text
AI Control Plane repo:
- Start every task with anchor from docs/prompts/ANCHOR_CURRENT.md
- Read docs/prompts/AGENT_OPERATING_SYSTEM.md for governance/soak/multi-PR work
- PACE: Plan risk + allowlist before Act; smoke 8/8 before PR
- Never tick PB9_STAGING_SOAK_LOG without operator message "đã tick ngày YYYY-MM-DD"
- Never push master without explicit human request; PR-only per CONTRIBUTING.md
- source .venv/bin/activate before pytest on WSL
```

### 2.4 Pin files in workspace (optional)

Pin: `ANCHOR_CURRENT.md`, `AGENTS.md`, `MANUAL_OPERATOR_PLAYBOOK.md`.

---

## 3. Every new chat (mandatory open)

### Step 1 — Pull + SHA

```bash
git checkout master && git pull
git log -1 --oneline
```

Update mental baseline; if you merged roadmap batch, refresh [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md).

### Step 2 — Paste anchor (first message)

Copy full block from [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md). Append:

```yaml
task: |
  [Your goal — one paragraph]
risk: LOW|MEDIUM|HIGH
track: docs-only|feature|governance|ops
file_allowlist:
  allowed: [...]
  forbidden: [src/**]   # if docs-only
```

### Step 3 — @ files (Tier B)

| Task type | @ mention |
|-----------|-----------|
| Code in `core/` | `ARCHITECTURE.md`, `CURSOR_RISK_POLICY.md` |
| Governance | `GOVERNANCE_DRIFT_RECONCILIATION.md`, task-specific plan |
| PB-9 support | `MANUAL_OPERATOR_PLAYBOOK.md`, `PB9_STAGING_SOAK_LOG.md` |
| New prompt | `_TEMPLATE.md`, `AGENT_OPERATING_SYSTEM.md` |

### Step 4 — Let scoped rules apply

Editing `docs/governance/**` → `governance-docs.mdc` activates.  
Editing `src/ai_control_plane/core/**` → `core-critical.mdc` activates.

---

## 4. Execution patterns

### Docs-only PR (most common @ Public Beta)

```text
TRACK: docs-only · risk LOW
Branch: docs/short-desc
Forbidden: src/**, .github/workflows/** (unless approved), GOVERNANCE_VERSION bump
Verify: pytest tests/test_smoke.py -m smoke
1 task = 1 branch = 1 PR
```

### Code PR

Follow [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) + [`CONTRIBUTING.md`](../../CONTRIBUTING.md):

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
```

### Iterative retrieval (≤3 rounds)

Per [`AGENTS.md`](../../AGENTS.md): SemanticSearch/Grep → read hits → refine. Round 4 blocked → Pause + state gap in anchor.

---

## 5. Session close (Evolve)

- [ ] PR created with verify checklist in body  
- [ ] No soak state stored only in chat  
- [ ] If pitfall repeated → `LESSONS_LEARNED.md` row (maintainer PR)  
- [ ] If baseline moved significantly → update `ANCHOR_CURRENT.md` in separate docs PR  

---

## 6. Cursor-specific anti-patterns

| Don't | Do instead |
|-------|------------|
| Start coding without anchor | Paste `ANCHOR_CURRENT` first |
| Trust summarized prior chat | Re-read Tier C files |
| `pytest` without `.venv` on WSL | `source .venv/bin/activate` |
| One PR mixing soak tick + feature code | Split branches |
| Agent merges without CI watch | `gh pr checks --watch` then human merge |

---

## 7. When NOT to use Cursor Agent

Use **human + [`MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md)** only:

- PB-9 daily tick ritual  
- Day 14 sign-off  
- PB-12 public visibility + release  
- Production pilot deploy decisions  

Cursor may **draft** text; operator **commits** via PR.

**Last updated:** 2026-06-30
