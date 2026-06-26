# Study 08 — Shipped config remote — Runbook

**Document ID:** ACP-GOV-PRACTICE-STUDY-08-RUNBOOK  
**Prerequisite:** Study 07 PASS · VPS `100.94.21.33`  
**Profile:** **B** — shipped `config/` (unset fixture `ACP_CONFIG_DIR`)

---

## Topology

Same as Study 07 option B: API on `ubuntu-vps`, client on MSI Laptop via Tailscale.

```text
Laptop  ACP_API_URL=http://100.94.21.33:8000
   │
   └── Tailscale ──► ubuntu-vps :8000 (Profile B — rules 10)
```

---

## Phase 1 — VPS: stop fixture Docker

```bash
cd ~/AI-Control-Plane
docker compose -f examples/minimal/docker-compose.yml down
```

---

## Phase 2 — VPS: API with shipped config

**Helper script:** `scripts/study08_vps_preflight.sh` (git pull, stop Docker/systemd, uvicorn Profile B).

**Option A — uvicorn (recommended for Profile B)**

```bash
cd ~/AI-Control-Plane
source .venv/bin/activate
unset ACP_CONFIG_DIR   # use repo shipped config/
nohup uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000 \
  > /tmp/acp-study08-uvicorn.log 2>&1 &
```

**Option B — Docker** (requires compose override mounting `config/` — not in minimal image today; use Option A)

---

## Phase 3 — Verify Profile B on server

```bash
curl -sf http://127.0.0.1:8000/health | python3 -m json.tool
curl -sf http://127.0.0.1:8000/governance/status | python3 -c "
import sys,json; d=json.load(sys.stdin)
print('rules', d['policy_rules_count'])
print('agents', d.get('agents_loaded', 'see /health'))
"
```

**Expected:**

- `policy_rules_count`: **10**
- `agents_loaded`: includes **agent4**
- `projects_loaded`: includes **datax-analytics**

Save → `artifacts/remote-profile-b-health.json`

---

## Phase 4 — Remote client (Laptop)

```bash
export ACP_API_URL=http://100.94.21.33:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/soak_staging.sh --log /tmp/acp-study08-soak.log
```

**Expected soak:** `health=ok` with Profile B API (G-07 apex path).

Save log excerpt → `artifacts/remote-profile-b-soak.md`

---

## Phase 5 — Restore VPS staging (optional)

After evidence capture, restore PB-9 fixture stack:

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
# or: sudo systemctl restart acp-staging.service
```

---

## Governance mapping

| Gap | Step |
|-----|------|
| G-06 | Phase 3–4 health rules=10 remote |
| G-07 | Phase 4 soak with shipped config |
