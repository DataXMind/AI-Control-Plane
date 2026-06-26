# PB-7 — Warm dry-run (MSI WSL) — partial

**Date:** 2026-06-26  
**Label:** **WARM** — not a PB-7 PASS (dev machine, pre-existing stack)  
**Purpose:** Validate runbook curl commands only

## Result

Dry-run curls failed — local Docker API not reachable at authoring time (`curl` exit 22). Operator must run full Path A on **CLEAN** machine per [`RUNBOOK.md`](../RUNBOOK.md).

## Does not substitute PB-7

Per [`GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md`](../../../GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md): real fork on clean machine required.
