# ACP Data Flow & Trust Boundaries — 0.x

**Document ID:** ACP-GOV-DATAFLOW-001  
**Baseline:** `master` @ `e074c55` · Catalog v1.3.3  
**Related:** [`THREAT_MODEL.md`](THREAT_MODEL.md) · [`DATA_CLASSIFICATION.md`](../DATA_CLASSIFICATION.md) · [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

## Data Flow Diagram (ASCII)

```
[AI Agent]
    │ POST /policy/evaluate
    │ {agent_id, project_id, tool_name, role, args}
    ▼
[ACP Policy Engine] ──── reads ────► [Policy config YAML]
    │                                  (ACP_CONFIG_DIR — operator-defined; no PII by design)
    │ reads/writes (when ACP_REDIS_URL set)
    ▼
[Redis]
    │ {quota counts, action registry keys; optional when URL unset → in-memory}
    │
    │ writes (when telemetry / task persistence enabled)
    ▼
[ACP_DATA_DIR / structlog output]
    │ {timestamp, agent_id, decision, latency — policy audit path}
    │ No LLM prompts or conversation content on the policy hot path
    │
    ▼
[Operator / agentctl] ── GET /governance/status ── [Governance catalog (static SSOT)]
```

---

## Data Classification per Flow

| Data Element | Location | Contains PII? | Sensitivity | Retention |
|---|---|---|---|---|
| `agent_id` | Policy request, Redis (quota keys), logs | Depends on operator config | MEDIUM | Per-config |
| `role` | Policy request | No | LOW | Not persisted beyond request handling |
| `tool_name` (action) | Policy request, logs | No | LOW | Log retention |
| `project_id` / resource scope | Policy request, logs | Possibly (project naming) | MEDIUM | Log retention |
| `args` (context) | Policy request body | Operator-defined | VARIES | Not stored by default on hot path |
| Policy decision | Logs; Redis when quota/registry used | No | LOW | TTL + log retention |
| Quota count | Redis or in-memory `QuotaStore` | No | LOW | Rolling window |
| Governance state | `governance_catalog.py` | No | LOW | Static (versioned in git) |

---

## PII Handling Note (0.x)

ACP does not intentionally process PII. However:

- `agent_id` may be a human username if the operator configures it as such
- `project_id` or paths in `args` may contain URLs or identifiers with personal data
- `args` is operator-defined and may contain arbitrary data

**MCP layer:** Architecture and CHANGELOG reference `mcp/server_utils.py` with `redact_sensitive_data()` for MCP response redaction. At baseline `e074c55`, that module is **not yet present** under `src/ai_control_plane/mcp/` (only `git_server.py`, `server_factory.py`). Redaction rules are **not documented**; do not assume MCP output scrubbing until implemented and evidenced.

**Operator responsibility:** If `agent_id`, `args`, or logs contain personal data, you are responsible for log retention, deletion rights, and GDPR compliance. ACP 0.x does not provide right-to-erasure tooling for operator-collected fields.

---

## Trust Boundaries (reference: THREAT_MODEL.md §1)

| ID | Boundary | Trust level |
|----|----------|-------------|
| TB-1 | Agent → ACP Policy Engine | Authenticated (token) |
| TB-2 | ACP Policy Engine → Redis | Internal network; AUTH required when Redis used |
| TB-3 | Operator → ACP via `agentctl` / API | Admin token (separate from agent tokens) |
| TB-4 | ACP → Downstream resources | N/A — ACP advises; does not execute downstream actions |

---

## What ACP Does NOT Store

- LLM prompt/response content
- User conversation history
- Full tool call arguments beyond what operators pass in `args` for policy classification
- Financial or health data (by design — operator must not encode PHI in identifiers)

---

## Compliance Notes

- **GDPR:** If `agent_id` or logs contain personal data, ACP audit output is in scope. Operator must configure retention and erasure processes.
- **HIPAA:** ACP does not process PHI by design. Operator must ensure identifiers do not encode patient data.
- **SOC2:** Structlog policy-decision output supports logging controls when operators preserve and protect log files.

**Out of scope 0.x:** Multi-tenant isolation, production OpenTelemetry pipelines, automated PII scrubbing on all paths.

---

**Last updated:** 2026-06-29 · Catalog v1.3.3 · `master` @ `e074c55`
