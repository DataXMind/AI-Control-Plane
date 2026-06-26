# G2-1 — Drill 5g kill switch (operator evidence)

**Gate:** G2-1 · **Gap:** G-01  
**Run date:** 2026-06-26  
**Host:** MSI WSL · **Config:** ephemeral `/tmp/acp-killswitch-config` (fixture copy; **not** committed)  
**Operator:** dmin@MSI

---

## Commands (per `RUNBOOK.md` §5g)

```bash
cd /mnt/d/Projects/ai-control-plane
. .venv/bin/activate
CFG=/tmp/acp-killswitch-config
rm -rf "$CFG" && mkdir -p "$CFG" && cp -r tests/fixtures/config/* "$CFG/"
python3 -c 'import yaml; from pathlib import Path; p=Path("/tmp/acp-killswitch-config/policies.yml"); d=yaml.safe_load(p.read_text()); d.setdefault("kill_switch",{})["active"]=True; d["kill_switch"]["reason"]="study-05-drill-5g-g2"; p.write_text(yaml.dump(d))'
export ACP_CONFIG_DIR="$CFG"
uvicorn ai_control_plane.api.server:app --host 127.0.0.1 --port 8765 &
# wait for /health
curl -s -X POST http://127.0.0.1:8765/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}'
curl -sf http://127.0.0.1:8765/health
```

---

## Policy evaluate (kill switch active)

```json
{
    "allowed": false,
    "reason": "kill_switch_active: study-05-drill-5g-g2",
    "requires_approval": false,
    "policy_id": "kill_switch",
    "latency_ms": 0.4
}
```

HTTP **200** · global deny · reason contains `kill_switch_active`.

---

## Health (API still up)

```json
{
    "status": "ok",
    "config_loaded": true,
    "policy_rules_count": 8
}
```

---

## Verdict

| Expected | Actual | Result |
|----------|--------|--------|
| `allowed: false` when `kill_switch.active=true` | `kill_switch_active: study-05-drill-5g-g2` | ✅ PASS |
| `/health` remains reachable | `status: ok` | ✅ PASS |

**Code coverage:** `tests/test_guardrails.py` (MB-S1-1) — this drill is **operator evidence** only.
