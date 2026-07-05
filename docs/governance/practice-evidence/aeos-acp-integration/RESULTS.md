# AEOS × ACP Guardrails — Integration evidence (ACP repo view)

**Document ID:** ACP-PRACTICE-AEOS-ACP-001  
**Status:** **AEOS PHASE 2 SMOKE PASS** (MSI WSL client → VPS ACP, 2026-07-05)  
**ACP baseline:** VPS production pilot · Tailscale `100.94.21.33:8000` · `policy_rules_count: 10`  
**AEOS baseline:** `main` @ `9be7e2a` (duydp/aeos — merge PR #4)  
**AEOS SSOT (detail):** [`duydp/aeos`](https://github.com/duydp/aeos) → `docs/governance/practice-evidence/aeos-acp-integration/RESULTS.md`

---

## 1. Scope sign-off

| Product | Integration | Verdict |
|---------|-------------|---------|
| **Hybrid AI Gateway** × ACP | Tool policy + `/acp/status` | **CONNECT CLOSED** — [`hybrid-gateway-acp-integration/RESULTS.md`](../hybrid-gateway-acp-integration/RESULTS.md) |
| **AEOS** × ACP | `POST /sessions` → `session.create` evaluate | **PHASE 2 PASS** — this doc |
| **SACP** (Sovereign AI Control Plane) | LLM gateway routing | **OPEN** — operator reports issues; evidence pending; **≠ ACP** |

---

## 2. Three-product map (no conflation)

| Name | Repo | Role | This evidence |
|------|------|------|---------------|
| **ACP** | AI-Control-Plane | Agent tool policy `POST /policy/evaluate` | Host on VPS |
| **AEOS** | aeos | Session orchestrator + bridge client | Client on MSI |
| **SACP** | Hybrid-AI-Gateway (gateway README naming) | LLM chat routing/compliance | **Not verified here** |

See [`HYBRID_AI_GATEWAY.md`](../../integrations/HYBRID_AI_GATEWAY.md) §0.

---

## 3. ACP host environments

### 3.1 VPS production pilot (operator-verified)

| Field | Value |
|-------|-------|
| Tailscale URL | `http://100.94.21.33:8000` |
| VPS localhost | `http://127.0.0.1:8000` |
| `policy_rules_count` | **10** |
| Config | `/opt/acp/production-config` → container `/etc/acp/config` |
| Compose | `examples/minimal/docker-compose.yml` + `docker-compose.production.yml` + `/opt/acp/.env.production` |
| Agents | `agent1`–`agent4` |
| Projects | `datax-analytics`, `rust-gateway` |
| AEOS action | `session.create` allowed for `agent2`/`backend`/`rust-gateway` |

### 3.2 MSI localhost (reference — not AEOS smoke path)

| Field | Value |
|-------|-------|
| URL | `http://127.0.0.1:8000` |
| Container | `minimal-acp-api-1` |
| Profile | Fixture (8 rules) if production overlay not applied |
| Note | AEOS Phase 2 smoke used **VPS** ACP, not local Docker |

---

## 4. AEOS client configuration (verified)

| Variable | Value |
|----------|-------|
| `ACP_ENABLED` | `true` (server terminal only) |
| `ACP_API_URL` | `http://100.94.21.33:8000` |
| `ACP_AGENT_ID` | `agent2` |
| `ACP_ROLE` | `backend` |
| `ACP_PROJECT_ID` | `rust-gateway` (temporary) |
| AEOS API (dev) | `http://127.0.0.1:8002` (`API_PORT=8002`) |

---

## 5. Verification matrix

| # | Check | Result | Date |
|---|-------|--------|------|
| 1 | VPS `/health` 10 rules | PASS | 2026-07-05 |
| 2 | VPS evaluate `session.create` → allow | PASS | 2026-07-05 |
| 3 | AEOS `POST /sessions` with bridge | PASS — HTTP 201 | 2026-07-05 |
| 4 | AEOS GitHub CI | **OPEN** — runs #15–#21 fail; local gate green @ `9be7e2a` |

Artifacts (sanitized): AEOS repo `docs/governance/practice-evidence/aeos-acp-integration/artifacts/`

---

## 6. Drift — reject outdated claims

| Claim | Verdict |
|-------|---------|
| AEOS Phase 2 not implemented | **REJECT** — @ `8918c1b` |
| ACP PASS implies SACP PASS | **REJECT** |
| AEOS dev on `:8000` with local ACP Docker | **REJECT** — use `:8002` |
| `policy_rules_count: 8` on VPS = production | **REJECT** — fixture mis-deploy |
| GitHub CI green for aeos | **REJECT** until workflow passes |

---

## 7. Open items

| ID | Item |
|----|------|
| O-01 | AEOS GitHub CI fix (deferred) |
| O-02 | Register `aeos` project on VPS `production-config` |
| O-03 | SACP evidence pack (operator to supply) |

---

## 8. Sign-off

| Role | Verdict | Date |
|------|---------|------|
| Operator | AEOS × ACP Phase 2 **SMOKE PASS** | 2026-07-05 |
