# ECC 48H — Post-verify deep audit

**Document ID:** ACP-GOV-ECC-POST-VERIFY-001  
**Status:** **PASS** (with documented gaps)  
**Operator:** MSI WSL (`dmin@MSI`)  
**Date:** 2026-06-30  
**Baseline:** `master` @ **`1dd8f31`** · catalog **v1.5.0** · **17** patterns · ECC 48H PR #146–#151 merged

**Parent:** [`ECC_48H_RESULTS.md`](../ECC_48H_RESULTS.md) · **Log:** [`artifacts/deep-audit-2026-06-30.log`](artifacts/deep-audit-2026-06-30.log)

---

## Verdict matrix

| Layer | Check | Result | Notes |
|-------|-------|--------|-------|
| L4 pytest | Full suite | **PASS** 177/177 | In-process; not Docker-only |
| L4 smoke | pass^8 | **PASS** 8/8 | WSL `.venv` |
| L4 shipped | `shipped_config` | **PASS** (in full suite) | Profile B parity |
| L4 MCP | `test_mcp_*` subset | **PASS** 13/13 | Policy integration + HTTP transport |
| L4 runtime | `verify_governance_status_runtime.sh` | **PASS** | **1.5.0 · 17 patterns** @ `minimal-acp-api-1` |
| L4 runtime | `verify_openapi_runtime.sh` | **PASS** | 3.1.0 · 13 paths |
| L5 memory | `verify_governance_memory.sh` | **PASS** | ML5 pack |
| L3 integrate | `examples/integrate/python/*` live | **PASS** | allow + deny + health + quota |
| L1 OpenAPI | `export_openapi.py` diff | **PASS** | Static `docs/openapi/openapi.json` in sync |
| ECC 48H | 5-phase artifacts on disk | **PASS** | A1–A9 per closeout doc |
| **GAP** | GHCR `demo` image catalog | **RESOLVED** @ PR #157 | Was **1.4.0** — auto-republish on `governance_catalog.py` push + `verify_ghcr_catalog.sh` |
| **GAP** | `SESSION_ANCHOR_TEMPLATE` | **RESOLVED** @ PR #161 | Was v1.3.3 / stale SHA — anchor @ `ad3d58a` |
| **GAP** | Port 8000 conflict | **RISK** | `acp-demo` (GHCR) vs `minimal-acp-api-1` — operator must `--down` before switch |

---

## Blind spots found (previous report understated)

### G-ECC-01 — GHCR demo image stale (HIGH for CONNECT path)

| Field | Detail |
|-------|--------|
| **Symptom** | `verify_governance_status_runtime.sh` returned **1.4.0** while repo @ **1.5.0** |
| **Root cause** | `acp-demo` container (`ghcr.io/dataxmind/ai-control-plane:demo`) bound :8000; image built pre–Phase 5 |
| **Trigger gap** | ~~tags only~~ | **Fixed:** `publish-ghcr.yml` triggers on `governance_catalog.py` / Dockerfile push to `master` |
| **Mitigation** | `docker stop acp-demo` + compose build OR `gh workflow run "Publish GHCR demo image"` |
| **Prevention** | `bash scripts/verify_ghcr_catalog.sh` before CONNECT-path verify |

### G-ECC-02 — Session anchor drift (P-14) — **RESOLVED** @ PR #161

Was: anchor cited v1.3.3 / 13 patterns. Now: `SESSION_ANCHOR_TEMPLATE.md` @ `ad3d58a` · v1.5.0 · 17 patterns.

### G-ECC-03 — Shell `curl` JSON escaping (operator trap)

Direct `curl -d '{...}'` from PowerShell/WSL wrappers can fail silently (405/invalid body). **Use:** integrate examples, `httpx`, or `agentctl` with venv active.

### G-ECC-04 — Not exercised this audit (explicit defer)

| Item | Why deferred |
|------|----------------|
| Study 09 MCP inventory | **Closed** @ `study-09-mcp-inventory/` |
| k6 / fleet load (P-15) | **Closed** @ `k6-policy-smoke/` PASS 10 VUs |
| Cross-host / Tailscale | Requires second machine |
| Kill switch live drill | Covered by SMK-04 + Study 05 runbook; not re-run live |
| `acp-up.sh --ghcr` end-to-end | Unblocked after GHCR republish @ PR #157 |
| AgentShield / ECC plugin | REJECT per 48H plan |

---

## Operator commands (repro)

```bash
git pull origin master   # expect 1dd8f31+
docker stop acp-demo 2>/dev/null || true
docker compose -f examples/minimal/docker-compose.yml up --build -d
export ACP_CONFIG_DIR=tests/fixtures/config
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/run_ecc_deep_audit.sh
```

---

## ECC 48H phase traceability

| Phase | Runtime evidence |
|-------|------------------|
| 1 SSOT | `DOC_LINKS.ecc_integration_analysis` in `/governance/status` |
| 2 Security | THREAT §6 + MCP matrix present; not re-audited prose |
| 3 Eval | `EVAL_METHODOLOGY.md` pass^k maps smoke 8/8 |
| 4 Agents | Integrative retrieval in `AGENTS.md`; session contract doc-only |
| 5 P-17 | Runtime `lessons_patterns` id **P-17** @ v1.5.0 |

---

**Last updated:** 2026-06-30 · Operator deep audit · PB-9 soak unchanged
