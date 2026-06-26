# VPS operator run — governance verify 2026-06-26

**Host:** `ubuntu-vps` (`root@~/AI-Control-Plane`)  
**Context:** Post Study 08 restore; pre-PR #104 on VPS at first attempt

## Commands run (chronological)

| Step | Command | Result |
|------|---------|--------|
| 1 | `sudo systemctl restart acp-staging.service` | OK (no output) |
| 2 | `export ACP_API_URL=http://127.0.0.1:8000` | OK |
| 3 | `ruff check src/ tests/ && mypy src/ai_control_plane/ --strict` | ✅ All checks passed |
| 4 | `bash scripts/verify_governance_status_runtime.sh` | ❌ No such file (PR #104 not pulled) |
| 5 | `nano scripts/verify_governance_status_runtime.sh` + `chmod +x` | ⚠️ Wrong content pasted |
| 6 | `bash verify_governance_status_runtime.sh` (from `scripts/`) | ✅ `OK: governance/status runtime verify 1.3.0 12 patterns` |

## Misleading output (not runtime verify)

```text
verify_governance_memory: all checks passed (ML5 pack)
```

## Correct next run (from repo root @ master ≥ cf1f90a)

```bash
cd ~/AI-Control-Plane
rm -f scripts/verify_governance_status_runtime.sh   # required if hand-created via nano (untracked blocks git pull)
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
```

Expected:

```text
OK: governance/status runtime verify 1.3.0 12 patterns
```
