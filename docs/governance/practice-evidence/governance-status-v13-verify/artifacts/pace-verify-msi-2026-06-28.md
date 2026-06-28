# PACE verify — MSI WSL @ 2026-06-28

**Document ID:** ACP-GOV-PRACTICE-PACE-2026-06-28  
**Host:** MSI WSL `dmin@MSI` (`/mnt/d/Projects/ai-control-plane`)  
**Label:** WARM (operator soak host)  
**Baseline:** `master` @ `fa71bd5`  
**Stack:** Docker `minimal-acp-api-1` + soak loop PID 2408

## Procedure & output

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke          # 8/8 PASS
docker compose -f examples/minimal/docker-compose.yml up -d
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh # 1.3.3 · 13 patterns
bash scripts/verify_openapi_runtime.sh           # 3.1.0 · 13 paths
bash scripts/restart_soak_loop.sh                # --repo-log PB9_SOAK_ITERATION_LOG.md
```

```text
gates_remaining: 7 (catalog unchanged until flip bump)
```

## Verdict

**PASS** — smoke + runtime + soak OP-02 restored post PB-7 teardown.
