# Study 02 — Profile B (shipped config) — PENDING

**Profile:** B — `unset ACP_CONFIG_DIR` → `config/`  
**Expected deltas vs Study 01:**

| Field | Study 01 (A) | Study 02 (B) |
|-------|--------------|--------------|
| `policy_rules_count` | 8 | **10** |
| `agents_loaded` | agent1–3 | agent1–**4** |
| `projects_loaded` | rust-gateway | rust-gateway + **datax-analytics** |

Run after Study 01 PASS: stop T1 uvicorn, then follow Profile B commands in `GOVERNANCE_UX_RUNTIME.md` / practice guide.

Evidence files will be added under this folder after operator run.
