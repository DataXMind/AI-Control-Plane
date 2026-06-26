# PB-7 — Clean-machine fork — Runbook

**Document ID:** ACP-GOV-PRACTICE-PB7-RUNBOOK  
**Target:** ≤ **15 minutes** clone → `GET /health` OK + `POST /policy/evaluate` allow  
**Primary path:** Docker (matches PB-9 staging)  
**Secondary path:** Native venv (no Docker)

Start timer at **T0** when `git clone` begins.

---

## Prerequisites

| Item | Docker Path A | Native Path B |
|------|---------------|---------------|
| OS | Linux or WSL2 | Linux / WSL2 / macOS |
| Git | ✓ | ✓ |
| Docker + Compose v2 | ✓ | — |
| Python 3.11+ | — | ✓ |
| Network | GitHub clone + Docker Hub pull | GitHub clone + pip |

---

## Path A — Docker (recommended, ≤15 min)

### T0 — Clone

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
git log -1 --oneline   # record SHA in RESULTS.md
```

### T+2 — Start stack

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
```

**Expected:** Container `minimal-acp-api-1` (or similar) **healthy** within ~2–5 min first pull.

### T+5 — Health

```bash
curl -sf http://localhost:8000/health | python3 -m json.tool
```

**Expected:**

```json
{
  "status": "ok",
  "config_loaded": true,
  "policy_rules_count": 8,
  "agents_loaded": ["agent1", "agent2", "agent3"]
}
```

### T+7 — Policy allow (fail-closed path smoke)

```bash
curl -sf -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

**Expected:** `"allowed": true`

### T+8 — Deny path (optional but recommended)

```bash
curl -sf -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"unknown-agent","project_id":"rust-gateway","tool_name":"git_read"}' \
  | python3 -m json.tool
```

**Expected:** `"allowed": false` with non-empty `reason`

### T+10 — Governance UX (optional)

```bash
curl -sf http://localhost:8000/governance/status | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d['governance_version'], d['practice_evidence']['studies_completed'])"
```

**Expected @ master:** `1.3.1 8` (version may bump — record actual)

### T+15 — PASS criteria

| Check | Required |
|-------|----------|
| Elapsed ≤ 15 min | ✓ |
| `/health` 200 | ✓ |
| Policy allow 200 | ✓ |
| No manual edits to `src/` | ✓ |

### Cleanup

```bash
docker compose -f examples/minimal/docker-compose.yml down
```

---

## Path B — Native venv (no Docker)

### T0 — Clone (same as Path A)

### T+2 — Venv + install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### T+8 — Run API

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --host 127.0.0.1 --port 8000 &
sleep 3
```

### T+10 — Health + policy (same curls as Path A on port 8000)

### T+15 — PASS criteria (same)

```bash
pkill -f "uvicorn ai_control_plane.api.server" || true
```

---

## Failure triage

| Symptom | Fix |
|---------|-----|
| `docker: command not found` | Install Docker or use Path B |
| Port 8000 in use | `docker compose down` or change port in compose |
| `config_loaded: false` | Check `ACP_CONFIG_DIR` mount in compose |
| Build > 10 min on slow network | Note in RESULTS; may exceed 15 min — file as **BLOCKER** with network caveat |
| WSL2 localhost refused from Windows | Use WSL shell for curls (Study 04/06 lesson) |

---

## Evidence to capture

Save to `artifacts/`:

- `artifacts/timing.md` — T0, T+health, T+policy, total elapsed
- `artifacts/health.json` — curl output
- `artifacts/policy-allow.json` — curl output
- `artifacts/machine-profile.md` — OS, CLEAN/WARM, Docker version

Update [`RESULTS.md`](RESULTS.md) PASS/FAIL.
