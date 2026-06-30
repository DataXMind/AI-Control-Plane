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

## Connector decision matrix (48H — aligned with industry MCP minimalism)

**SSOT context:** [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md) · external reference [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) MCP connector policy.

ACP **policy enforcement** sits **below** the harness MCP surface. Use this matrix when adding integrations:

| Prefer | When | ACP 0.x example |
|--------|------|-----------------|
| **HTTP `/policy/evaluate`** | Every tool call decision | `examples/integrate/python/before_tool_call.py` |
| **CLI / skill wrapper** | Stateless one-shot (create PR, run smoke) | `gh`, `agentctl`, `pytest` — not a persistent MCP server |
| **MCP connector** | Stateful, session-bound, universal across operators | Git via cyanheads adapter (**experimental**) |

**Default connector count target (operator harness):** **0–1** optional MCP servers beyond built-in harness tools. Each default connector taxes every session's context window.

**PR bar for new default MCP in ACP docs:** Must satisfy **both**:

1. **Universal** — applies to most coding-agent operators on any harness.  
2. **MCP beats CLI** — needs interactive session state, streaming, or auth handshake — not a single request/response.

If only one criterion holds → document as **skill/CLI**, not MCP.

**ACP does not ship** a general-purpose MCP catalog. Shipped path: policy API + optional git MCP facade.

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

> **STATUS: PROPOSED — implementation sau PB-12 flip (~2026-07-10), không kích hoạt trước**

**Prerequisite:** Pin the **MCP spec version** (and cyanheads git-mcp-server release) in this contract **before** authoring any E2E test. The placeholder in [MCP Version Compatibility](#mcp-version-compatibility) must be replaced with a concrete semver; E2E assertions depend on that pin.

**Target:** v0.2.x post-flip (one focused PR — **not** a 48H item).

**Approach options (choose one at implementation time):**

| Option | Summary |
|--------|---------|
| **(A) Docker service in CI** | Spin cyanheads git-mcp-server as a workflow service container; contract test exercises `SubprocessGitForwarder` against a real MCP process |
| **(B) Waiver continues** | Keep **`[mcp-unverified]`** label on MCP-related issues/PRs; no CI job; manual operator verification only |

**Effort:** ~1 PR after PB-12 flip (mock-adapter contract test **or** docker-service E2E — not both in the first pass).

**Explicit constraint (this document only):** No new `.github/workflows/` job is added as part of the roadmap clarification PR. Implementation PR is a separate maintainer-approved branch.

**Activation:** Open implementation task only when **(1)** PB-12 flip is complete **and** **(2)** maintainers approve a dedicated MCP CI branch.

---

## Finding from Architecture Review

Architecture artifacts and CHANGELOG reference `mcp/server_utils.py` with `redact_sensitive_data()` for MCP response redaction. At baseline `635ed8c`, that module is **not present** under `src/ai_control_plane/mcp/` (shipped: `git_server.py`, `server_factory.py` only). Redaction rules are **not yet documented**. See [`DATA_FLOW.md`](DATA_FLOW.md) § PII Handling Note.

---

**Last updated:** 2026-06-30 · Catalog v1.5.0
