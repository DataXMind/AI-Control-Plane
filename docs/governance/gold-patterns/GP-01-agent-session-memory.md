# GP-01 — Agent session memory (3-tier + anchor)

**Pattern ID:** GP-01  
**Version:** 1.0  
**Layer:** L5 — Governance & Memory  
**Maturity target:** ML5  
**Reference implementation:** [AI-Control-Plane](https://github.com/DataXMind/AI-Control-Plane) — `AGENTS.md`, `.cursor/rules/`, `SESSION_ANCHOR_TEMPLATE.md`

---

## Problem

Coding agents **forget** prior sessions. Long chats get **summarized** and lose SHAs, approval gates, and operator evidence. Teams over-trust chat and under-document.

## When to use

- Multi-session features (sprints, soak calendars, governance tracks)
- Multiple agents (Cursor + Claude + CI bots) on one repo
- Fail-closed or regulated codebases where **audit trail** matters

## When not to use

- Single-file scripts with one-shot edits
- Repos without any agent policy (start at ML1 flat `.cursorrules` first)

---

## Solution — three memory tiers

| Tier | Storage | Lifetime | Owner |
|------|---------|----------|-------|
| **A — Auto** | `.cursorrules`, `.cursor/rules/*.mdc`, editor user rules | Every session | Maintainers |
| **B — Session** | Session anchor YAML in chat + `@` files | One task/PR | Agent + human |
| **C — Durable** | `LESSONS_LEARNED.md`, `docs/evidence/`, soak logs | Months/years | Human operator |

**Principle:** If it must survive a new chat, it belongs in **Tier C**.

---

## Minimal file tree (copy into your repo)

```text
AGENTS.md                          # Single entry for all agents
.cursorrules                       # L0–L5 stack (or start L0-only)
.cursor/rules/
  memory-always.mdc                # alwaysApply: true — anchor + SSOT
  your-domain.mdc                  # globs: src/** — scoped rules
docs/
  prompts/SESSION_ANCHOR_TEMPLATE.md
  governance/LESSONS_LEARNED.md    # failure → rule loop
scripts/verify_agent_memory.sh     # CI gate (exit non-zero if missing)
```

---

## Session anchor (copy every session)

```yaml
session_anchor:
  version: "1.0"
  date: "YYYY-MM-DD"
  baseline: "main @ <sha>"
  risk: "LOW | MEDIUM | HIGH | CRITICAL"
  gates_approved: []
  branch: "feature/..."

file_allowlist:
  allowed: ["docs/**"]
  forbidden: ["src/**"]

assumptions:
  - "Files I will touch: ..."
verify:
  - "your-test-command"
task: |
  Goal in one paragraph.
```

Full template: ACP [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](../../../prompts/SESSION_ANCHOR_TEMPLATE.md) · living snapshot [`ANCHOR_CURRENT.md`](../../../prompts/ANCHOR_CURRENT.md) · framework [`AGENT_OPERATING_SYSTEM.md`](../../../prompts/AGENT_OPERATING_SYSTEM.md).

---

## Scoped rule example (`.cursor/rules/memory-always.mdc`)

```markdown
---
description: Require session anchor; SSOT over chat
alwaysApply: true
---

# Memory

1. Open session with SESSION_ANCHOR_TEMPLATE.md filled.
2. SSOT: ARCHITECTURE / code > written evidence > chat.
3. Sprint close: update LESSONS_LEARNED.md for repeated pitfalls.
```

---

## SSOT hierarchy (recommended)

```text
code + ARCHITECTURE
  > operator RESULTS / run logs
  > governance runtime API (optional)
  > design HTML/PDF archives (historical)
```

---

## Verify (adopter CI snippet)

```bash
#!/usr/bin/env bash
set -euo pipefail
test -f AGENTS.md
test -f docs/prompts/SESSION_ANCHOR_TEMPLATE.md
count=$(find .cursor/rules -name '*.mdc' 2>/dev/null | wc -l)
test "$count" -ge 1
echo "GP-01 memory pack OK ($count rules)"
```

ACP ships: `scripts/verify_governance_memory.sh` + `tests/test_governance_memory.py`.

---

## Optional — runtime governance UX

ACP exposes `GET /governance/status` with layers, case studies, and `doc_links`. Adopters can start with **static markdown only** (GP-01) and add runtime later.

---

## Adoption checklist

- [ ] `AGENTS.md` links to anchor template and lessons file
- [ ] At least one `alwaysApply` rule enforces anchor
- [ ] CI runs verify script on every PR
- [ ] Evolve step requires LESSONS update on repeated failures
- [ ] Operators log hands-on evidence in files, not chat

---

## ACP case studies tied to GP-01

| Lesson | Why GP-01 helps |
|--------|-----------------|
| P-11 HTML artifact drift | Tier C reconciliation docs; chat cannot be SSOT |
| PB-9 soak | `PB9_STAGING_SOAK_LOG.md` Tier C — Studies ≠ calendar |
| CS-01/03/04 weak | Anchor lists gates; durable audit defines what is proven |

---

## License & attribution

Copy freely into MIT/Apache projects. Attribution: *"Based on GP-01 Agent Session Memory, AI Control Plane."*

---

**Last updated:** 2026-06-25
