# MCP Integration Contract — ACP 0.x

**Document ID:** ACP-GOV-MCP-CONTRACT-001  
**Baseline:** `master` @ `635ed8c` · Catalog v1.3.3  
**Related:** [`DATA_FLOW.md`](DATA_FLOW.md) · [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`mcp/git_server.py`](../../src/ai_control_plane/mcp/git_server.py)

---

## Status

- **Integration path:** MCP (Model Context Protocol) via **cyanheads** adapter (`SubprocessGitForwarder` → cyanheads git-mcp-server)
- **CI status:** **NOT CI-tested** in 0.x (known limitation — see [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md))
- **Stability:** **EXPERIMENTAL** in 0.x beta

---

## MCP Version Compatibility

| ACP Version | MCP Spec Version | Adapter | CI Tested |
|---|---|---|---|
| 0.x beta | [operator to fill — pin version] | cyanheads | ❌ No |
| 0.2.x (planned) | TBD | TBD | Target: Yes |

**Operator action:** Before deploying ACP with MCP integration, pin the MCP spec version. If the MCP spec updates, test manually before upgrading.

---

## Contract: What ACP Expects from MCP Layer

ACP treats MCP as an **event source** that emits agent action intents.

The MCP adapter **must** provide:

1. **`agent_id`** — stable identifier for the calling agent
2. **`action`** — string matching the ACP policy rule namespace (mapped from MCP `tool_name` via `resolve_policy_tool_name()`)
3. **`resource`** — target of the action (optional but recommended)
4. **`role`** — agent's declared role (must match ABAC config)

ACP does **not**:

- Validate MCP message schema (adapter responsibility)
- Retry failed MCP connections (operator-managed)
- Buffer MCP events during ACP restart

---

## Known Regression Risk

Because MCP integration is **not CI-tested** in 0.x:

- MCP-related issues after release should be labeled **`[mcp-unverified]`**
- Maintainers cannot guarantee MCP behavior is regression-free in patch releases
- Community MCP bug reports must include **MCP spec version** + **cyanheads version**

---

## Roadmap to CI Coverage

- **Target:** v0.2.x
- **Approach:** Contract test with mock MCP adapter (not cyanheads E2E)
- **Issue:** [to be created post-flip]

---

## Finding from Architecture Review

Architecture artifacts and CHANGELOG reference `mcp/server_utils.py` with `redact_sensitive_data()` for MCP response redaction. At baseline `635ed8c`, that module is **not present** under `src/ai_control_plane/mcp/` (shipped: `git_server.py`, `server_factory.py` only). Redaction rules are **not yet documented**. See [`DATA_FLOW.md`](DATA_FLOW.md) § PII Handling Note.

---

**Last updated:** 2026-06-29 · Catalog v1.3.3 · `master` @ `635ed8c`
