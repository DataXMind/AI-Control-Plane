# Client Integration Guide — CONNECT Door (Task 2)

**Document ID:** ACP-CLIENT-INTEGRATION-001  
**Audience:** App developers, agent builders, **client-of-client** integrators  
**You do NOT need:** `git clone`, fork, `ACP_CONFIG_DIR`, or governance docs  
**Operator path (Task 1):** [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md)

---

## 0. Which doc is for you?

| Tier | Doc | Who | Git required? |
|------|-----|-----|---------------|
| **T0** | [`QUICKSTART.md`](QUICKSTART.md) § CONNECT | First 5 min smoke | No |
| **T1** | **This file** | Wire policy into your app (any language) | No |
| **T2** | [`examples/integrate/`](../examples/integrate/README.md) | Runnable Python samples | Optional (copy scripts only) |
| **T3** | [`CONTRACT_TESTS.md`](CONTRACT_TESTS.md) + OpenAPI | Contract / codegen | No (use `/openapi.json`) |
| **Ops** | [`CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) | Who **hosts** ACP | No (vendor bundle) |

**Fork the repo?** Only if you plan to **contribute code/docs upstream** — see [`CONTRIBUTING.md`](../CONTRIBUTING.md). Integration does **not** require a fork.

**Procurement / competitive:** [`governance/PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md) §Feature comparison (OPA/Cedar/Casbin). Full map: [`END_USER_VALUE.md`](END_USER_VALUE.md).

---

## 1. Prerequisites (checklist)

Get these from whoever runs ACP (your platform team or vendor):

- [ ] **`ACP_API_URL`** — base URL, e.g. `http://acp.internal:8000` (no trailing slash)
- [ ] **`agent_id`** registered in operator's `agents.yml`
- [ ] **`project_id`** registered in operator's `projects.yml`
- [ ] **`role`** string matching operator config (e.g. `backend`)
- [ ] **Tool names** aligned with operator's `policies.yml` (e.g. `git_read`, `k8s_apply`)
- [ ] **Network path** from your app host to ACP (firewall / VPN / Tailscale)

Optional client env file: copy [`.env.client.example`](../.env.client.example) → export `ACP_API_URL`.

---

## 2. Step 1 — Verify connectivity (mandatory)

```bash
export ACP_API_URL=http://YOUR_ACP_HOST:8000   # replace YOUR_ACP_HOST

curl -sf "$ACP_API_URL/health" | python3 -m json.tool
```

**Pass criteria:**

| Field | Expected |
|-------|----------|
| `status` | `"ok"` |
| `config_loaded` | `true` |
| `policy_rules_count` | `> 0` |

**If this fails → stop.** Do not call tools (fail-closed). Fix network or contact the operator.

---

## 3. Step 2 — Prove allow + deny (mandatory)

```bash
# ALLOW — use agent/project the operator registered for you
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"YOUR_AGENT","project_id":"YOUR_PROJECT","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

# DENY — unknown agent (must fail closed)
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"unknown-agent","project_id":"YOUR_PROJECT","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

**Pass criteria:**

| Call | HTTP | Body |
|------|------|------|
| ALLOW | 200 | `"allowed": true` |
| DENY | 200 | `"allowed": false`, non-empty `"reason"` |

---

## 4. Integration pattern — one choke point

Implement **one function** (or middleware) in your codebase that every tool/action passes through **before** execution:

```text
your_app → acp_allow(...) → if OK → run_tool()
                         → if deny/timeout → abort (fail-closed)
```

**Language:** any HTTP client. Python samples in [`examples/integrate/`](../examples/integrate/README.md) are **reference only** — not a dependency.

### HTTP contract (SSOT)

| Method | Path | When |
|--------|------|------|
| `POST` | `/policy/evaluate` | Before every agent tool / sensitive action |
| `GET` | `/health` | Worker startup gate |
| `GET` | `/quota/{project_id}` | Before LLM / costly calls |
| `GET` | `/openapi.json` | Codegen / contract tests |

Frozen fields @ public beta: [`CONTRACT_TESTS.md`](CONTRACT_TESTS.md). Live Swagger: `$ACP_API_URL/docs`.

**Request body** (`POST /policy/evaluate`):

```json
{
  "agent_id": "string",
  "project_id": "string",
  "tool_name": "string",
  "role": "string",
  "args": {}
}
```

`role` may be omitted but operators often require it. `args` is optional (defaults `{}`).

**Response body** (200):

```json
{
  "allowed": true,
  "reason": "",
  "requires_approval": false,
  "policy_id": "...",
  "evaluation_path": "...",
  "latency_ms": 1.2
}
```

| Outcome | Semantics |
|---------|-----------|
| `allowed: true` | Proceed with action |
| `allowed: false` | Deny — read `reason` |
| HTTP error / timeout | **Deny** (fail-closed) |
| `/identity/verify` invalid JWT | HTTP **401** (not 200+deny) |

---

## 5. Language examples

### Python

Copy [`examples/integrate/python/before_tool_call.py`](../examples/integrate/python/before_tool_call.py) or inline:

```python
import os
import httpx

ACP = os.environ["ACP_API_URL"].rstrip("/")

def acp_allow(*, agent_id: str, project_id: str, tool_name: str, role: str) -> None:
    try:
        r = httpx.post(
            f"{ACP}/policy/evaluate",
            json={"agent_id": agent_id, "project_id": project_id,
                  "tool_name": tool_name, "role": role},
            timeout=2.0,
        )
        r.raise_for_status()
    except httpx.HTTPError as exc:
        raise PermissionError(f"ACP fail-closed: {exc}") from exc
    body = r.json()
    if not body.get("allowed"):
        raise PermissionError(body.get("reason") or "policy denied")
```

Run samples (requires `pip install httpx` only — no repo clone):

```bash
export ACP_API_URL=http://YOUR_ACP_HOST:8000
python before_tool_call.py   # after copying the script
```

### TypeScript

Designed primary consumer: TypeScript **PolicyClient** in agent gateways.

```typescript
const base = process.env.ACP_API_URL!.replace(/\/$/, "");

export async function acpAllow(req: {
  agent_id: string;
  project_id: string;
  tool_name: string;
  role: string;
}): Promise<void> {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), 2000);
  try {
    const res = await fetch(`${base}/policy/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
      signal: controller.signal,
    });
    if (!res.ok) throw new Error(`ACP HTTP ${res.status}`);
    const body = (await res.json()) as { allowed: boolean; reason?: string };
    if (!body.allowed) throw new Error(body.reason ?? "policy denied");
  } catch (e) {
    throw new Error(`ACP fail-closed: ${e}`);
  } finally {
    clearTimeout(t);
  }
}
```

Generate a typed client from `$ACP_API_URL/openapi.json` when you want OpenAPI codegen.

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Serialize)]
struct EvalRequest<'a> {
    agent_id: &'a str,
    project_id: &'a str,
    tool_name: &'a str,
    role: &'a str,
}

#[derive(Deserialize)]
struct EvalResponse {
    allowed: bool,
    reason: String,
}

pub async fn acp_allow(
    client: &Client,
    base: &str,
    req: EvalRequest<'_>,
) -> Result<(), String> {
    let url = format!("{}/policy/evaluate", base.trim_end_matches('/'));
    let resp = client
        .post(&url)
        .json(&req)
        .timeout(Duration::from_secs(2))
        .send()
        .await
        .map_err(|e| format!("ACP fail-closed: {e}"))?;
    if !resp.status().is_success() {
        return Err(format!("ACP fail-closed: HTTP {}", resp.status()));
    }
    let body: EvalResponse = resp
        .json()
        .await
        .map_err(|e| format!("ACP fail-closed: {e}"))?;
    if !body.allowed {
        return Err(if body.reason.is_empty() {
            "policy denied".into()
        } else {
            body.reason
        });
    }
    Ok(())
}
```

### Go

```go
package acp

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
)

type EvalRequest struct {
	AgentID   string `json:"agent_id"`
	ProjectID string `json:"project_id"`
	ToolName  string `json:"tool_name"`
	Role      string `json:"role"`
}

type EvalResponse struct {
	Allowed bool   `json:"allowed"`
	Reason  string `json:"reason"`
}

func Allow(ctx context.Context, base string, req EvalRequest) error {
	body, _ := json.Marshal(req)
	url := strings.TrimRight(base, "/") + "/policy/evaluate"
	httpReq, _ := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	httpReq.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 2 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		return fmt.Errorf("ACP fail-closed: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("ACP fail-closed: HTTP %d", resp.StatusCode)
	}
	var out EvalResponse
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		return fmt.Errorf("ACP fail-closed: %w", err)
	}
	if !out.Allowed {
		if out.Reason != "" {
			return fmt.Errorf("%s", out.Reason)
		}
		return fmt.Errorf("policy denied")
	}
	return nil
}
```

---

## 6. Optional patterns

| Pattern | API | Sample |
|---------|-----|--------|
| Startup health gate | `GET /health` | [`startup_health_gate.py`](../examples/integrate/python/startup_health_gate.py) |
| Quota before LLM | `GET /quota/{project_id}` | [`quota_check.py`](../examples/integrate/python/quota_check.py) |
| Human approval | `requires_approval: true` in evaluate response | Operator workflow + Study 02 |

---

## 7. Client rules (do / don't)

| Do | Don't |
|----|-------|
| Set **`ACP_API_URL`** on app/worker hosts | Set `ACP_CONFIG_DIR` on client machines |
| Deny on timeout / 5xx / connection error | Default-allow when ACP is down |
| Map each bot/worker to a registered `agent_id` | Hardcode policy rules in app code |
| Use OpenAPI as contract SSOT | Depend on copying Python into non-Python repos |
| Ask operator to restart API after config change | Expect policy to change without API restart |

---

## 8. Handoff checklist (integrator sign-off)

- [ ] Step 1 health check passes
- [ ] Step 2 allow + deny smoke passes with **your** agent/project IDs
- [ ] Single choke-point function wired before all tools
- [ ] Fail-closed tested (stop ACP → app denies / worker exits)
- [ ] `requires_approval` flow documented if used
- [ ] 0.x disclaimer acknowledged — API may change until `1.0.0`

---

## 9. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `connection refused` | Wrong `ACP_API_URL`, firewall, or ACP not running — ask operator |
| `allowed: false` for known agent | `agent_id` / `role` / `tool_name` mismatch — ask operator to check YAML |
| Works on laptop, fails in CI | CI cannot reach private ACP — VPN or test double |
| Empty curl JSON | API still starting — retry or operator runs `verify-pilot.sh` |

Advanced networking (WSL portproxy, Tailscale): [`RUNBOOK.md`](RUNBOOK.md).

---

## 11. Operator rollback & incidents (integrator handoff)

Policy rollback and SEV-1 response are **operator-owned**. Integrators: on incident, **stop calling tools** (fail-closed) and contact the operator.

| Scenario | SSOT |
|----------|------|
| PB-9 Day 14 FAIL / soak extension | [`governance/ROLLBACK_PROTOCOL.md`](governance/ROLLBACK_PROTOCOL.md) Scenario 1 |
| SEV-1 after public flip | Same doc — Scenario 2 (hotfix branch, security advisory) |
| Network / connectivity | [`RUNBOOK.md`](RUNBOOK.md) |

Operators changing YAML: see [`CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) § **Evaluate before apply** (staging matrix before production restart).

---

## 12. What next?

| Goal | Doc |
|------|-----|
| Host ACP for your team | [`CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) |
| 5-minute overview | [`QUICKSTART.md`](QUICKSTART.md) |
| Contribute upstream | [`CONTRIBUTING.md`](../CONTRIBUTING.md) |

---

**Last updated:** 2026-07-02 · baseline `44a5fef` · competitive + END_USER_VALUE cross-links
