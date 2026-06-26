# G2-2 — Drill 5e-r stale Docker image (operator evidence)

**Gate:** G2-2 · **Gap:** G-02  
**Run date:** 2026-06-26  
**Host:** MSI WSL · Docker `minimal-acp-api-1`  
**Change:** `GOVERNANCE_VERSION` `1.2` → `1.2.1` in `governance_catalog.py`

---

## Procedure

1. Original Study 05e: rebuild **without** src edit → version unchanged (partial).
2. 05e-r: bump catalog version + `docker compose up -d --build`.
3. Assert `/governance/status` reflects new version.

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -sf http://localhost:8000/governance/status | python3 -m json.tool | head -5
```

---

## Result

```json
"governance_version": "1.2.1"
```

`known_gaps` G-02 status: **CLOSED** in catalog.

---

## Verdict

| Expected | Actual | Result |
|----------|--------|--------|
| Version changes after src bump + rebuild | `1.2.1` | ✅ PASS |
| Teaches rebuild-after-merge | See also `governance-status-v12-verify` | ✅ |
