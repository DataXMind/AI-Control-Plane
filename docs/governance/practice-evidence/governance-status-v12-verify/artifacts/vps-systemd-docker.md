# VPS verify — ubuntu-vps + systemd staging

**Run date:** 2026-06-26  
**Host:** `ubuntu-vps` (`<VPS_TAILSCALE_IP>` Tailscale)  
**Repo:** `/root/AI-Control-Plane` @ `8b30ad4`  
**API:** `http://127.0.0.1:8000` → Docker via `acp-staging.service`

---

## Commands

```bash
cd ~/AI-Control-Plane
git pull origin master
sudo systemctl restart acp-staging.service
sleep 15
curl -sf http://127.0.0.1:8000/governance/status | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(d['governance_version'], len(d['known_gaps']), d['practice_evidence']['overall_verdict'])
"
```

---

## Output

```text
1.2 7 PASS
```

---

## git pull scope

Fast-forward `acccf4b..8b30ad4` — includes PR #98 (Gate B, systemd) + PR #99 (`governance_catalog` v1.2).

---

## Prior failure (documented)

Before `git pull` + `systemctl restart acp-staging`: same `KeyError: 'known_gaps'` as local — stale Docker image.
