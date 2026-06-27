# Governance status v1.3 — Runtime verify (3-stream convergence)

**Document ID:** ACP-GOV-PRACTICE-GOV-STATUS-V13  
**Status:** **PASS** (latest: **v1.3.3** @ `863b611`)  
**Run date:** 2026-06-27 (local + VPS)  
**Prerequisite:** PR [#115](https://github.com/DataXMind/AI-Control-Plane/pull/115) → `master` @ `863b611` (catalog v1.3.3)  
**Related:** `lessons_patterns[]` P-01..**P-13** + `practice_evidence.studies_completed: 8`

---

## Verdict

| Layer | Check | ubuntu-vps @ 2026-06-26 | Notes |
|-------|-------|---------------------------|-------|
| **L4 repo** | `ruff` + `mypy --strict` | ✅ PASS | Prior operator + CI |
| **L4 repo** | `pytest` smoke 8/8 | ✅ | CI on #109 |
| **L5** | `verify_governance_memory.sh` | ✅ PASS | |
| **Runtime v1.3.0** | `verify_governance_status_runtime.sh` | ✅ **PASS** | `1.3.0` · `12 patterns` @ `a43524a` |
| **Runtime v1.3.2** | `verify_governance_status_runtime.sh` | ✅ **PASS** | `1.3.2` · `13 patterns` @ `68ae48e` |
| **Runtime v1.3.3** | `verify_governance_status_runtime.sh` | ✅ **PASS** | `1.3.3` · `13 patterns` @ `863b611` |

| Host | Stack | `governance_version` | `lessons_patterns` | Result |
|------|-------|----------------------|--------------------|--------|
| **WSL local** | Docker `minimal-acp-api-1` | **1.3.3** | **13** | ✅ |
| **ubuntu-vps** | Docker + `acp-staging.service` | **1.3.3** | **13** | ✅ |

---

## Operator incident analysis (resolved)

Earlier session issues (documented for ML5):

1. Script missing — PR #104 not pulled  
2. Wrong cwd (`scripts/` subdir)  
3. Hand `nano` pasted `verify_governance_memory.sh` content (false PASS)  
4. `git pull` blocked by untracked hand file → fixed with `rm` then pull  
5. `ruff + mypy` invalid syntax → use `ruff check ... && mypy ...`

**Resolution (v1.3.0):** `rm -f scripts/verify_governance_status_runtime.sh` → `git pull` @ `a43524a` → `systemctl restart` → runtime script **PASS**.

**Resolution (v1.3.2):** Clean `git pull` `dbf3079..68ae48e` → `systemctl restart` → `OK: … 1.3.2 13 patterns` (no incident).

**Resolution (v1.3.3):** `git pull` @ `863b611` → `systemctl restart` → `OK: … 1.3.3 13 patterns` (no incident).

---

## Canonical VPS procedure

```bash
cd ~/AI-Control-Plane
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
```

Expected (@ master ≥ `863b611`):

```text
OK: governance/status runtime verify 1.3.3 13 patterns
```

**Lesson (G-02):** `git pull` + `systemctl restart` rebuilds Docker image — required after merges touching `src/`.

---

## Test matrix

### v1.3.0 (@ `a43524a`)

| ID | Assert | Expected | VPS |
|----|--------|----------|-----|
| V13-1 | `governance_version` | `1.3.0` | ✅ |
| V13-2 | `len(known_gaps)` | `7` | ✅ |
| V13-3 | OPEN gaps | `G-05` only | ✅ |
| V13-4 | `len(lessons_patterns)` | `≥ 12` | ✅ (12) |
| V13-5 | `practice_evidence.studies_completed` | `8` | ✅ |
| V13-6 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ |

### v1.3.2 (@ `68ae48e`)

| ID | Assert | Expected | VPS |
|----|--------|----------|-----|
| V132-1 | `governance_version` | `1.3.2` | ✅ |
| V132-2 | `len(known_gaps)` | `7` | ✅ |
| V132-3 | OPEN gaps | `G-05` only | ✅ |
| V132-4 | `len(lessons_patterns)` | `≥ 13` | ✅ (13, P-13) |
| V132-5 | `practice_evidence.studies_completed` | `8` | ✅ |
| V132-6 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ |

### v1.3.3 (@ `863b611`)

| ID | Assert | Expected | Local | VPS |
|----|--------|----------|-------|-----|
| V133-1 | `governance_version` | `1.3.3` | ✅ | ✅ |
| V133-2 | `len(known_gaps)` | `7` | ✅ | ✅ |
| V133-3 | OPEN gaps | `G-05` only | ✅ | ✅ |
| V133-4 | `len(lessons_patterns)` | `≥ 13` | ✅ (13) | ✅ (13) |
| V133-5 | `len(gates_remaining)` | `≥ 5` | ✅ (7) | ✅ |
| V133-6 | `len(gates_closed)` | `≥ 3` | ✅ (4) | ✅ |
| V133-7 | `practice_evidence.studies_completed` | `8` | ✅ | ✅ |
| V133-8 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ | ✅ |

---

## Artifacts

- [x] `artifacts/vps-operator-run-2026-06-26.md` — incident trail (v1.3.0 attempt)
- [x] `artifacts/vps-runtime-v13-pass.md` — PASS @ `a43524a` (`1.3.0` · 12 patterns)
- [x] `artifacts/vps-runtime-v132-pass.md` — PASS @ `68ae48e` (`1.3.2` · 13 patterns)
- [x] `artifacts/local-runtime-v133-pass.md` — PASS @ `863b611` (local Docker)
- [x] `artifacts/vps-runtime-v133-pass.md` — PASS @ `863b611` (`1.3.3` · 13 patterns)
- [x] `artifacts/TASK_AUDIT_REMAINING_2026-06-26.md` — open vs closed task audit
- [x] `artifacts/TASK_AUDIT_REMAINING_2026-06-27.md` — gates_remaining sync

---

**Last updated:** 2026-06-27 — runtime PASS local + ubuntu-vps @ v1.3.3
