# Governance status v1.3 — Runtime verify (3-stream convergence)

**Document ID:** ACP-GOV-PRACTICE-GOV-STATUS-V13  
**Status:** **PASS**  
**Run date:** 2026-06-26  
**Prerequisite:** PR [#104](https://github.com/DataXMind/AI-Control-Plane/pull/104) + docs [#105](https://github.com/DataXMind/AI-Control-Plane/pull/105) → `master` @ `a43524a`  
**Related:** `lessons_patterns[]` P-01..P-12 + `practice_evidence.studies_completed: 8`

---

## Verdict

| Layer | Check | ubuntu-vps @ 2026-06-26 | Notes |
|-------|-------|---------------------------|-------|
| **L4 repo** | `ruff` + `mypy --strict` | ✅ PASS | Operator paste |
| **L4 repo** | `pytest` smoke 8/8 | ✅ (prior CI + operator) | |
| **L5** | `verify_governance_memory.sh` | ✅ PASS | |
| **Runtime** | `verify_governance_status_runtime.sh` | ✅ **PASS** | `1.3.0` · `12 patterns` |

| Host | Stack | `governance_version` | `lessons_patterns` | Result |
|------|-------|----------------------|--------------------|--------|
| **ubuntu-vps** | Docker + `acp-staging.service` | **1.3.0** | **12** | ✅ |

---

## Operator incident analysis (resolved)

Earlier session issues (documented for ML5):

1. Script missing — PR #104 not pulled  
2. Wrong cwd (`scripts/` subdir)  
3. Hand `nano` pasted `verify_governance_memory.sh` content (false PASS)  
4. `git pull` blocked by untracked hand file → fixed with `rm` then pull  
5. `ruff + mypy` invalid syntax → use `ruff check ... && mypy ...`

**Resolution:** `rm -f scripts/verify_governance_status_runtime.sh` → `git pull` @ `a43524a` → `systemctl restart` → runtime script **PASS**.

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

Expected:

```text
OK: governance/status runtime verify 1.3.0 12 patterns
```

**Lesson (G-02):** `git pull` + `systemctl restart` rebuilds Docker image — required after merges touching `src/`.

---

## Test matrix (v1.3)

| ID | Assert | Expected | VPS |
|----|--------|----------|-----|
| V13-1 | `governance_version` | `1.3.0` | ✅ |
| V13-2 | `len(known_gaps)` | `7` | ✅ |
| V13-3 | OPEN gaps | `G-05` only | ✅ |
| V13-4 | `len(lessons_patterns)` | `≥ 12` | ✅ (12) |
| V13-5 | `practice_evidence.studies_completed` | `8` | ✅ |
| V13-6 | `doc_links.risk_policy` | `CURSOR_RISK_POLICY.md` | ✅ |

---

## Artifacts

- [x] `artifacts/vps-operator-run-2026-06-26.md` — incident trail
- [x] `artifacts/vps-runtime-v13-pass.md` — clean PASS @ `a43524a`

---

**Last updated:** 2026-06-26 — runtime PASS ubuntu-vps
