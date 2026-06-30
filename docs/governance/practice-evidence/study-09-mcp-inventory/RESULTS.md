# Study 09 — MCP inventory (P-17 practice evidence)

**Document ID:** ACP-GOV-PRACTICE-STUDY-09-001  
**Status:** **PASS** (inventory audit — not live MCP E2E)  
**Date:** 2026-06-30  
**Baseline:** `master` @ `25cfee0` · catalog **v1.5.0** · P-17 encoded

**Parent:** [`MCP_INTEGRATION_CONTRACT.md`](../../MCP_INTEGRATION_CONTRACT.md) · [`ECC_ACP_INTEGRATION_ANALYSIS.md`](../../ECC_ACP_INTEGRATION_ANALYSIS.md)

---

## Verdict

| Overall | Blocks PB-12? |
|---------|---------------|
| **PASS** — connector inventory documented; default target **0–1** MCP | **No** |

---

## Shipped MCP surface (repo inventory)

| # | Component | Path | Role | Default active? |
|---|-----------|------|------|-----------------|
| 1 | Git MCP facade | `src/ai_control_plane/mcp/git_server.py` | Policy-gated git tool forwarder | Optional (operator enables) |
| 2 | MCP server factory | `src/ai_control_plane/mcp/server_factory.py` | HTTP transport bootstrap | Optional |
| 3 | Tool name resolver | `src/ai_control_plane/core/tool_names.py` | MCP tool → policy action map | Always (library) |

**External adapter (not vendored):** cyanheads git-mcp-server via `ACP_MCP_GIT_URL` — **experimental**, not CI E2E.

---

## Connector decision matrix (operator harness)

| Integration | Classification | Rationale |
|-------------|----------------|-----------|
| `POST /policy/evaluate` | **Primary** | Universal; stateless; no context tax |
| `agentctl` / `gh` / `pytest` | **CLI/skill** | One-shot; no persistent MCP session |
| Git MCP (cyanheads) | **Optional MCP (0–1)** | Stateful git session; beats CLI when interactive |
| ECC / AgentShield plugins | **REJECT** | Not imported per ECC 48H plan |

---

## Test matrix

| ID | Check | Expected | Actual | Result |
|----|-------|----------|--------|--------|
| S09-1 | Shipped MCP modules | ≤3 in `mcp/` package | 3 files | ✅ |
| S09-2 | Default connector target | 0–1 documented | MCP_INTEGRATION_CONTRACT § matrix | ✅ |
| S09-3 | Policy path primary | HTTP evaluate documented | QUICKSTART + integrate examples | ✅ |
| S09-4 | P-17 lesson encoded | P-17 in catalog | `lessons_patterns` includes P-17 | ✅ |
| S09-5 | CI MCP subset | tests pass | `test_mcp_*` in deep audit | ✅ |

---

## Artifacts

- [x] [`artifacts/mcp-inventory.json`](artifacts/mcp-inventory.json)

---

## Honest scope

This study is an **inventory + decision-matrix audit**, not a second-machine MCP soak. Live cyanheads E2E remains **MC-8 debt** (labeled `[mcp-unverified]`).
