# Study 07 — Cross-network — Results (template)

**Document ID:** ACP-GOV-PRACTICE-STUDY-07  
**Status:** PENDING  
**Topology:** Ubuntu API + Windows client (mạng ngoài, Tailscale only)

| ID | Test | Expected | Actual | Result |
|----|------|----------|--------|--------|
| 7-0 | Tailnet + negative LAN | Laptop ngoài không reach LAN IP | | ☐ |
| 7-1 | curl health via TS | 200, rules 8 | | ☐ |
| 7-2 | agentctl gov status | rules match Ubuntu | | ☐ |
| 7-3 | policy evaluate | allowed true | | ☐ |
| 7-4 | agentctl assign | task_id + Ubuntu TS client IP in log | | ☐ |
| 7-5 | soak_staging.sh remote | soak_iter ok | optional | ☐ |

## Ubuntu API

| Key | Value |
|-----|--------|
| Host | |
| LAN IP | |
| Tailscale IP | |
| Config | `ACP_CONFIG_DIR=tests/fixtures/config` |

## Windows client (external network)

| Key | Value |
|-----|--------|
| Network | hotspot / external Wi-Fi |
| Tailscale IP | |
| ACP_API_URL | `http://<ubuntu-ts>:8000` |
| LAN ping Ubuntu | fail (required) |
