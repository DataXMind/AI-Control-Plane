# Gold Patterns — AI Control Plane

**Purpose:** Reusable, **public-ready** governance patterns extracted from ACP operator experience.  
**Audience:** Maintainers forking ACP or adopting fail-closed agent governance in other repos.

| ID | Title | Layer | Status |
|----|-------|-------|--------|
| [**GP-01**](GP-01-agent-session-memory.md) | Agent session memory (3-tier + anchor) | L5 | **Stable** — reference implementation on ACP |

---

## How to use

1. Read the pattern doc end-to-end.
2. Copy the **file tree** and **session anchor** block into your repo.
3. Run the pattern's verify script equivalent in CI.
4. Cite pattern ID in PR body: `Gold pattern: GP-01`.

---

## Contributing patterns

New gold patterns require:

- Problem / when-not-to-use
- Copy-paste file tree
- Verify commands
- Mapping to 6-layer (L0–L5)
- LOW-risk docs PR or linked issue

---

**Last updated:** 2026-06-25
