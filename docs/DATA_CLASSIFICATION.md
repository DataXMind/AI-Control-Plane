# Data Classification

**Document ID:** ACP-DATA-CLASS-001  
**Layer:** L1 — Project context  
**Related:** `config/policies.yml` (Restrict-PII), [`ARCHITECTURE.md`](../ARCHITECTURE.md) ABAC

---

## Sensitivity levels

| Level | Definition | Examples in ACP |
|-------|------------|-----------------|
| **PUBLIC** | Safe in shipped `config/` and docs | Project ids, tool names, policy rule ids |
| **INTERNAL** | Runtime config; not in public examples | Agent registry entries, quota limits |
| **SENSITIVE** | PII or credentials; never commit | JWT secrets, production `ACP_CONFIG_DIR` |
| **RESTRICTED** | Policy-gated data paths | `data_class: pii` / `data_category: PII` in ABAC |

---

## PII and ABAC

Policy rule **Restrict-PII** (`config/policies.yml`):

- Denies when `data_class: pii` for roles outside privileged `role_not_in` list (e.g. `reviewer` exempt).
- Evaluation context keys: `data_class`, `data_category` (loader normalizes to policy engine).

**Test fixtures:** Use synthetic values only in `tests/fixtures/config/`. No real user emails, tokens, or cluster credentials.

---

## Telemetry fields

| Field | Classification | Notes |
|-------|----------------|-------|
| `agent_id`, `project_id`, `tool_name` | INTERNAL | Logged via structlog; hash-chain in `TelemetryEvent` |
| `payload` / free-form metadata | SENSITIVE if user content | Do not log raw prompts with secrets |
| JWT / API keys | RESTRICTED | Env vars only (`ACP_JWKS_URL`, never in YAML) |

---

## Handling rules

1. Shipped `config/*.yml` — **no production secrets** (Public Beta gate PB-12).
2. Fork operators override via `ACP_CONFIG_DIR`; do not commit private paths.
3. ABAC changes touching PII rules = **CRITICAL** risk per [`CURSOR_RISK_POLICY.md`](governance/CURSOR_RISK_POLICY.md).

**Last updated:** 2026-06-22
