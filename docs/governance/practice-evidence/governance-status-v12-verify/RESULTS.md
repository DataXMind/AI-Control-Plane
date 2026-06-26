# Governance status v1.2 — Dual-host Docker verify

**Document ID:** ACP-GOV-PRACTICE-GOV-STATUS-V12  
**Status:** **PASS**  
**Run date:** 2026-06-26  
**Prerequisite:** PR [#99](https://github.com/DataXMind/AI-Control-Plane/pull/99) merged → `master` @ `8b30ad4`  
**Related:** Claude review P0 (Phương án A) — `known_gaps[]` + `practice_evidence` on `GET /governance/status`

---

## Verdict

| Host | Stack | `governance_version` | `known_gaps` | `practice_evidence.verdict` | Result |
|------|-------|----------------------|--------------|----------------------------|--------|
| **MSI Laptop (WSL)** | Docker `minimal-acp-api-1` | **1.2** | **7** | **PASS** | ✅ |
| **ubuntu-vps** | Docker + `acp-staging.service` | **1.2** | **7** | **PASS** | ✅ |

---

## Test case

| ID | Step | Expected | Evidence |
|----|------|----------|----------|
| V12-1 | `git pull origin master` @ `8b30ad4` | Includes `governance_catalog` v1.2 | Both hosts |
| V12-2 | `docker compose ... up -d --build` (local) or `systemctl restart acp-staging` (VPS) | Image rebuild copies new `src/` | Build log layer `[5/7] COPY src` |
| V12-3 | `curl /governance/status` | JSON includes `known_gaps`, `practice_evidence` | Artifacts below |
| V12-4 | One-liner assert | Prints `1.2 7 PASS` | Operator paste |

**Lesson (G-02 related):** `git pull` alone does **not** update running API — Docker image must rebuild. Initial `KeyError: 'known_gaps'` before rebuild = stale container (documented in operator notes).

---

## Operator command (canonical)

```bash
curl -sf http://127.0.0.1:8000/governance/status | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(d['governance_version'], len(d['known_gaps']), d['practice_evidence']['overall_verdict'])
"
```

---

## Governance mapping

| Item | Evidence |
|------|----------|
| Stream 3 runtime UX | `GET /governance/status` self-describing |
| Stream 1 practice gaps | `known_gaps` G-01..G-07 in JSON |
| Profile C Docker | PB-9 + VPS 24/7 staging parity |
| CS-02 catalog | `doc_links` includes `practice_audit` |

---

## Artifacts

- [x] `artifacts/local-msi-docker.md`
- [x] `artifacts/vps-systemd-docker.md`

---

## Operator notes

1. Local: `docker compose -f examples/minimal/docker-compose.yml up -d --build` after every merge touching `src/`.
2. VPS: `git pull` + `sudo systemctl restart acp-staging.service`.
3. Soak scripts unchanged — no restart required for `nohup soak_staging.sh`.
