# PB-7 — Clean-machine fork verify (G3-1)

**Document ID:** ACP-GOV-PRACTICE-PB7-001  
**Status:** **PENDING** — runbook ready; operator clean-machine run required  
**Gate:** PB-7 · G3-1  
**Source:** [`OPEN_SOURCE_READINESS.md`](../../../OPEN_SOURCE_READINESS.md) · [`PUBLIC_BETA_GO_NO_GO.md`](../../PUBLIC_BETA_GO_NO_GO.md)

---

## Goal

Prove a **new operator** can clone the repo and reach a working API (**health + policy path**) in **≤ 15 minutes** using only README + `examples/minimal/` — no tribal knowledge.

**Acceptance:** Docker Path A PASS on clean machine OR documented blocker with fix.

---

## Quick start

| Doc | Purpose |
|-----|---------|
| [`RUNBOOK.md`](RUNBOOK.md) | Timed steps Path A (Docker) + Path B (native) |
| [`CHECKLIST.md`](CHECKLIST.md) | Operator sign-off |
| [`RESULTS.md`](RESULTS.md) | PASS/FAIL + elapsed time |

---

## What is "clean machine"?

| Qualifies | Does not qualify |
|-----------|------------------|
| Fresh VM / cloud instance | Dev laptop with existing `.venv` and cached images |
| New WSL distro never cloned ACP | MSI machine used for Studies 01–08 |
| CI runner first checkout | Warm Docker layer cache without noting it |

Record machine profile in `RESULTS.md` either way; label **CLEAN** vs **WARM** explicitly.

---

## Risk (PACE)

| Class | LOW — docs-only until operator run |
|-------|-------------------------------------|
| Blocks PB-9? | **No** — parallel G3 track |
| Blocks PB-12? | **Partial** — PB-7 must PASS before flip |
