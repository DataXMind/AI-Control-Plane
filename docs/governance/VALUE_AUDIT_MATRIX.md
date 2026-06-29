# ACP Value Audit Matrix — 0.x

## Tier × Moat Cross-Reference

| Moat | Enterprise (Tier 1) | LLM Builder (Tier 2) | Gov-only (Tier 3) |
|---|---|---|---|
| Fail-closed policy | CS-06, SMK-04 | PB-7 quick start | — |
| Practice evidence corpus | Studies 01-08, dual-host | Studies 01-03 | Studies 04-07 |
| Governance catalog runtime | GET /governance/status | — | SESSION_ANCHOR |
| Agent-native ABAC | CS-04, shipped parity | PRODUCT_POSITIONING | — |
| 16 LESSONS encoded | P-01..P-16, PACE | CONTRIBUTING QS | P-01..P-16 |

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
| Gov-only | 16 LESSONS + PACE = rare ops asset | LESSONS_LEARNED, GOVERNANCE_CHANGELOG |

## Moat Strength @ 0.x

| Moat | Strength | Evidence | Timeline to strengthen |
|---|---|---|---|
| Practice evidence | Strong | 8 studies, dual-host, kill-switch | Study 09+ post-flip |
| Governance catalog runtime | Medium-Strong | GET /governance/status v1.4.0 | v1.5.x new gates |
| 16 LESSONS + 6-layer | Medium | P-01..P-16, PACE | Community additions |
| Agent-native ABAC | Medium | Shipped parity CI, CS-04 | Load test (P-15 closure) |
| SAPAL adaptive loop | Weak | Stub → Phase 0 v0.2.x | v0.3.x proposals |

**Last updated:** 2026-06-29 · master @ `cff686e` · catalog v1.4.0
