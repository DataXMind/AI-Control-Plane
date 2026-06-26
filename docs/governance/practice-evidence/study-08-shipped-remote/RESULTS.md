# Study 08 — Shipped config remote — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-08  
**Status:** **PARTIAL** — client soak PASS; VPS Profile B pending SSH operator  
**Run date:** 2026-06-26  
**Operator:** dmin@MSI (client) · VPS SSH blocked (publickey)

---

## Verdict

| Overall | Closes G-06/G-07? | Blocks PB-12? |
|---------|-------------------|---------------|
| **PARTIAL** | G-07 path only | No |

---

## Test matrix

| ID | Test | Expected | Actual | Result |
|----|------|----------|--------|--------|
| 8-1 | `/health` rules count | 10 | **8** (fixture Profile A on VPS) | ☐ |
| 8-2 | `agent4` loaded | present | **absent** (agent1–3) | ☐ |
| 8-3 | `datax-analytics` project | present | **rust-gateway** only | ☐ |
| 8-4 | Remote soak | PASS | PASS @ 09:33Z | ☑ |

---

## Artifacts

- [x] `artifacts/remote-preflight-health-vps.json` — VPS state before Profile B switch
- [x] `artifacts/remote-preflight-gov-vps.json` — `governance_version: 1.2` (needs `git pull` + Profile B)
- [x] `artifacts/remote-profile-b-soak.md` — client soak PASS
- [ ] `artifacts/remote-profile-b-health.json` — after `scripts/study08_vps_preflight.sh`

---

## Operator unblock (VPS)

```bash
ssh ubuntu-vps   # or root@100.94.21.33
cd ~/AI-Control-Plane && git pull origin master
bash scripts/study08_vps_preflight.sh
# Laptop: export ACP_API_URL=http://100.94.21.33:8000 && bash scripts/soak_staging.sh
# Restore: sudo systemctl restart acp-staging.service
```
