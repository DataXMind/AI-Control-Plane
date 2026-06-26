# Governance status v1.3 — Runtime verify (3-stream convergence)

**Document ID:** ACP-GOV-PRACTICE-GOV-STATUS-V13  
**Status:** **PARTIAL** — repo gate PASS; runtime script pending clean VPS re-run  
**Run date:** 2026-06-26  
**Prerequisite:** PR [#104](https://github.com/DataXMind/AI-Control-Plane/pull/104) merged → `master` @ `f50794b`  
**Related:** `lessons_patterns[]` P-01..P-12 + `practice_evidence.studies_completed: 8`

---

## Verdict

| Layer | Check | ubuntu-vps @ 2026-06-26 | Notes |
|-------|-------|---------------------------|-------|
| **L4 repo** | `ruff` + `mypy --strict` | ✅ PASS | Operator paste |
| **L4 repo** | `pytest` smoke 8/8 | ✅ (prior runs) | Not re-pasted this session |
| **L5** | `verify_governance_memory.sh` | ✅ PASS | Accidentally run via misnamed hand script (see below) |
| **Runtime** | `verify_governance_status_runtime.sh` | ⏸ **PENDING** | Script missing on VPS until `git pull`; hand `nano` copy was wrong file |

---

## Operator incident analysis (ubuntu-vps)

### What worked

```bash
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
ruff check src/ tests/ && mypy src/ai_control_plane/ --strict
# → All checks passed!
```

### Failure 1 — script not in tree

```text
bash: scripts/verify_governance_status_runtime.sh: No such file or directory
```

**Cause:** PR #104 not merged / `git pull` not run before operator session. File ships only on `master` ≥ `f50794b`.

**Fix:** `git pull origin master` — do **not** hand-create with `nano`.

### Failure 2 — wrong working directory

From `~/AI-Control-Plane/scripts/`:

```bash
bash scripts/verify_governance_status_runtime.sh   # WRONG — looks for scripts/scripts/
bash verify_governance_status_runtime.sh           # path OK only if cwd = scripts/
```

**Fix:** Always run from **repo root**:

```bash
cd ~/AI-Control-Plane
bash scripts/verify_governance_status_runtime.sh
```

### Failure 3 — hand-pasted script content (false PASS)

Operator created `scripts/verify_governance_status_runtime.sh` manually. Output showed:

```text
verify_governance_memory: all checks passed (ML5 pack)
```

That is **`verify_governance_memory.sh`** output — **not** runtime curl verify.

**Expected output** when correct:

```text
OK: governance/status runtime verify 1.3.0 12 patterns
```

**Fix:** Delete hand copy; `git checkout -- scripts/verify_governance_status_runtime.sh` after pull.

### Failure 4 — `ruff + mypy` (earlier session)

`ruff + mypy --strict` is invalid shell — `+` is not a command separator for ruff. Use:

```bash
ruff check src/ tests/ && mypy src/ai_control_plane/ --strict
```

---

## Canonical VPS procedure (post PR #104)

```bash
cd ~/AI-Control-Plane
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000

# Sanity
curl -sf "$ACP_API_URL/health" | python3 -m json.tool

# L4 repo gate
ruff check src/ tests/ && mypy src/ai_control_plane/ --strict
pytest tests/test_governance_status.py tests/test_cli_gov.py -q
pytest -m smoke -q
bash scripts/verify_governance_memory.sh

# Runtime gate (requires rebuilt Docker image from new src/)
bash scripts/verify_governance_status_runtime.sh
```

**Lesson (G-02):** `git pull` + `systemctl restart` triggers `docker compose up -d --build` — required for `governance_version: 1.3.0` and `lessons_patterns` in JSON.

---

## Test matrix (v1.3)

| ID | Assert | Expected |
|----|--------|----------|
| V13-1 | `governance_version` | `1.3.0` |
| V13-2 | `len(known_gaps)` | `7` |
| V13-3 | OPEN gaps | `G-05` only |
| V13-4 | `len(lessons_patterns)` | `≥ 12` |
| V13-5 | `practice_evidence.studies_completed` | `8` |
| V13-6 | `doc_links.risk_policy` | ends with `CURSOR_RISK_POLICY.md` |

---

## Artifacts

- [x] `artifacts/vps-operator-run-2026-06-26.md` — incident + partial PASS
- [ ] `artifacts/vps-runtime-v13-pass.md` — after clean re-run

---

**Operator:** Re-run canonical procedure after `git pull` @ `f50794b` and tick runtime row PASS.
