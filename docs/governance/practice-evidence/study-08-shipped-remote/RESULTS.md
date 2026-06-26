# Study 08 — Shipped config remote — Results

**Document ID:** ACP-GOV-PRACTICE-STUDY-08  
**Status:** **PASS**  
**Run date:** 2026-06-26  
**Operator:** root@ubuntu-vps (Profile B) + dmin@MSI (remote client)

---

## Verdict

| Overall | Closes G-06/G-07? | Blocks PB-12? |
|---------|-------------------|---------------|
| **PASS** | ✅ Yes | No |

---

## Test matrix

| ID | Test | Expected | Actual | Result |
|----|------|----------|--------|--------|
| 8-1 | `/health` rules count | 10 | **10** | ☑ |
| 8-2 | `agent4` loaded | present | **agent4** | ☑ |
| 8-3 | `datax-analytics` project | present | **datax-analytics** | ☑ |
| 8-4 | Remote soak | PASS | PASS @ 10:36:10Z | ☑ |

---

## Artifacts

- [x] `artifacts/remote-preflight-health-vps.json` — before Profile B (rules=8)
- [x] `artifacts/remote-preflight-gov-vps.json` — before Profile B
- [x] `artifacts/remote-profile-b-health.json` — after `study08_vps_preflight.sh`
- [x] `artifacts/remote-profile-b-soak.md` — client soak PASS

---

## Restore PB-9 staging (operator)

Study 08 stopped Docker/systemd fixture stack. To resume VPS 24/7 PB-9:

```bash
pkill -f "uvicorn ai_control_plane.api.server" || true
sudo systemctl restart acp-staging.service
# or: docker compose -f examples/minimal/docker-compose.yml up -d --build
```
