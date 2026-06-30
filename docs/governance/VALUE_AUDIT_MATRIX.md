# ACP Value Audit Matrix — 0.x

## Tier × Moat Cross-Reference

| Moat | Enterprise (Tier 1) | LLM Builder (Tier 2) | Gov-only (Tier 3) |
|---|---|---|---|
| Fail-closed policy | CS-06, SMK-04 | PB-7 quick start | — |
| Practice evidence corpus | Studies 01-08, dual-host, ecc-48h-post-verify | Studies 01-03 | Studies 04-07 |
| Governance catalog runtime | GET /governance/status · gate_details | — | SESSION_ANCHOR |
| Agent-native ABAC | CS-04, shipped parity | PRODUCT_POSITIONING | — |
| 17 LESSONS encoded | P-01..P-17, PACE | CONTRIBUTING QS | P-01..P-17 |

## Case Study → Tier Map

| CS | Title | Primary Tier | Secondary |
|---|---|---|---|
| CS-01 | Monolithic PR risk | Gov-only | Enterprise |
| CS-02 | Scope creep doc PRs | Gov-only | All |
| CS-03 | GitHub auto-close failure | Gov-only | — |
| CS-04 | Silent ABAC assumption | Enterprise | LLM Builder |
| CS-05 | Staging soak gate | Enterprise | LLM Builder |
| CS-06 | Fail-closed policy path | Enterprise | LLM Builder |

## Why Care at Public Flip (per tier)

| Tier | Primary reason | Trust artifact |
|---|---|---|
| Enterprise | Audit-ready trust surface | THREAT_MODEL + 8 studies + SAPAL_LEGAL |
| LLM Builder | ≤15 min fork, MIT, 0.x disclaimer | PB-7, README Quick Start |
| Gov-only | 17 LESSONS + PACE = rare ops asset | LESSONS_LEARNED, GOVERNANCE_CHANGELOG |

## Moat Strength @ 0.x

| Moat | Strength | Evidence | Timeline to strengthen |
|---|---|---|---|
| Practice evidence | Strong | 8 studies, dual-host, kill-switch, ecc-48h-post-verify | Study 09+ post-flip |
| Governance catalog runtime | Medium-Strong | v1.5.0 · 17 patterns · gate_details / gates_blocking_pb12 | GHCR sync on tag publish |
| 17 LESSONS + 6-layer | Medium-Strong | P-01..P-17, PACE, ECC 48H | Community additions |
| Agent-native ABAC | Medium | Shipped parity CI, CS-04 | k6 load closure (P-15) |
| SAPAL adaptive loop | Weak | MVP in apex/ — demote in pitch until v0.3.x | v0.3.x proposals |

## Runtime gate clarity (P-14 @ v1.5.0)

| Field | Operator meaning |
|-------|------------------|
| `gates_remaining` | Catalog list until maintainer bump @ PB-12 flip (may include practice-PASS gates) |
| `gates_blocking_pb12` | **Truthful blockers** — typically `PB-9`, `PB-12` |
| `gate_details[].practice_status` | PASS / OPEN / DEFERRED with `evidence` path |

**SSOT:** `curl $ACP_API_URL/governance/status | jq '.public_beta'`

**Last updated:** 2026-06-30 · master @ `77c4cc8` · catalog v1.5.0
