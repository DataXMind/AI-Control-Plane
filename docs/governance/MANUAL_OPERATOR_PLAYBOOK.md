# Manual Operator Playbook — Public Beta (no Agent required)

**Document ID:** ACP-GOV-MANUAL-OPERATOR-PLAYBOOK-001  
**Audience:** Operator · maintainer · org admin  
**Phase:** PB-9 staging soak → PB-12 flip → PB-10 GA (deferred)  
**Baseline:** `master` @ **`5dc565b`** · catalog **v1.3.3**  
**SSOT companions:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md)

> **Purpose:** Execute all remaining Public Beta operator work **without Cursor Agent** — shell, editor, GitHub UI, SSH VPS, optional Claude Project for drafting only.

---

## 0. Classification (strict)

| Axis | Definition | Owner | Needs Cursor? |
|------|------------|-------|---------------|
| **M1 — Continuous manual** | Repeat daily / keep services alive | Operator | **No** |
| **C1 — Calendar** | Cannot accelerate by will | Operator + time | **No** |
| **H1 — Human gate** | Signature / decision / org permission | Maintainer / org admin | **No** |
| **D1 — Dependency** | Only after prior step PASS | Operator | **No** |

### Drift rules (mandatory)

- Practice PASS ≠ `gates_remaining` drops — **catalog bump @ flip** (maintainer).
- PB-9 Day 14 = **~2026-07-06** (soak start **2026-06-22**), **not** 07-10 unless new SEV-1/2.
- **PB-10 does not block** 0.x beta — record defer in PB-12 narrative.
- **Three soak layers — do not conflate:**

| Layer | Path | Owner |
|-------|------|-------|
| Human daily | `docs/governance/PB9_STAGING_SOAK_LOG.md` | Operator tick |
| MSI machine | `docs/governance/PB9_SOAK_ITERATION_LOG.md` | `restart_soak_loop.sh --repo-log` |
| VPS machine | `practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log` | `acp-soak.service` |

**True blockers for PB-12 @ 0.x:** **PB-9 (calendar)** + **PB-12 (human GO)** only.

---

## 1. Master checklist

### 1.1 Done — do not redo

| ID | Task | Owner | Evidence |
|----|------|-------|----------|
| PB-1..4 | Legal | Maintainer | LICENSE, SECURITY, CONTRIBUTING, CoC |
| PB-5 | `examples/minimal` | CI | `examples-minimal-smoke` |
| PB-7 | CLEAN fork ≤15 min | Operator | [`pb-7-clean-machine-fork/RESULTS.md`](practice-evidence/pb-7-clean-machine-fork/RESULTS.md) |
| PB-8 | Tag `v0.1.0-rc.1` | Human | `c58b4cc` — **do not re-tag** |
| OP-06 | security@ live | Operator | [`security-email-live-test/RESULTS.md`](practice-evidence/security-email-live-test/RESULTS.md) |
| OP-03 | Gap 06-22→25 | Done | `PB9_STAGING_SOAK_LOG.md` § clock |
| OP-05 | PB-7 waiver | Cancelled | OP-04 PASS |
| Engineering | #116–#118, smoke, OpenAPI | Done | CI green |
| OP-08 | CHANGELOG #120, go-no-go #119 | Done | merged |

### 1.2 M1 — Continuous (daily → ~2026-07-06)

| # | Task | Owner | Trigger | Artifact | Blocks flip? |
|---|------|-------|---------|----------|--------------|
| M1-01 | Keep MSI Docker stack up | Operator | Daily | `docker compose … ps` healthy | Indirect |
| M1-02 | Keep MSI soak loop | Operator | Daily / after reboot | New lines in `PB9_SOAK_ITERATION_LOG.md` ~hourly | **Yes** |
| M1-03 | Keep VPS `acp-staging` + `acp-soak` | Operator | Daily | `vps-soak-iteration.log` + `/var/log/` | **Yes** |
| M1-04 | **Daily tick** human table | Operator | After 00:00 UTC when soak OK | `PB9_STAGING_SOAK_LOG.md` | **Yes** |
| M1-05 | `git pull` MSI/VPS | Operator | After remote push | No soak restart if **docs-only** | No |
| M1-06 | Watch SEV-1/2 | Operator | On anomaly | Notes column in daily table | **Yes** if SEV-1/2 |

**Ticks remaining (UTC calendar):** **2026-06-29** through **2026-07-05** (+ review row **2026-07-06**).  
**Last tick recorded @ playbook write:** **2026-06-28**.

### 1.3 C1 — Calendar (wait for date)

| # | Task | Owner | Target | Depends on | Artifact |
|---|------|-------|--------|------------|----------|
| C1-01 | Day 14 PB-9 review | Operator | **~2026-07-06** | ≥14 days from 2026-06-22 + clean soak | `practice-evidence/pb-9-day14-review/RESULTS.md` |
| C1-02 | Pre-flip refresh | Maintainer | **~2026-07-07** | C1-01 = PASS | `export_openapi.py`, smoke, verify |
| C1-03 | PB-12 flip window | Human | **~2026-07-10** | C1-01 PASS + C1-02 OK | GitHub public + release |

### 1.4 H1 — Human gates (cannot delegate to agent)

| # | Task | Owner | When | Why not automatable |
|---|------|-------|------|---------------------|
| H1-01 | Day 14 **verdict** PASS/FAIL/CONDITIONAL | Operator sign-off | ~2026-07-06 | Operational accountability |
| H1-02 | PB-12 **GO / NO-GO** + signature | Maintainer | ~2026-07-10 | Product decision |
| H1-03 | Record **PB-10 defer** in PB-12 record | Maintainer | @ PB-12 | 0.x vs GA policy |
| H1-04 | GitHub **public visibility** | Org admin | @ PB-12 GO | Org permission |
| H1-05 | Release **`v0.1.0-beta.1`** | Maintainer | @ PB-12 | Human approve |
| H1-06 | Catalog **`gates_remaining` bump** | Maintainer | @ flip | Edit `governance_catalog.py` + PR |
| H1-07 | PB-11 branch protection API | Org | Post-public or Team plan | GitHub plan |

### 1.5 D1 — Post-flip / deferred

| # | Task | Owner | Depends on | Issue |
|---|------|-------|------------|-------|
| D1-01 | PB-10 production soak 30d | Operator | PB-12 GO | [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78) |
| D1-02 | Close #77 | Operator | Day 14 PASS | [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) |
| D1-03 | OpenAPI publish prominence in README | Maintainer | Flip | PB-6 |
| D1-04 | GA `1.0.0` / PyPI | Future | PB-10 PASS | Phase 3 |

### 1.6 Optional (not blocking)

| Task | When |
|------|------|
| Smoke 8/8 + `verify_*` on MSI | Before Day 14; after `src/` pull |
| Witness PB-7 on third machine | Not required — CLEAN PASS exists |
| Re-test security@ | Not required — PASS 2026-06-28 |
| Claude Project draft RESULTS.md | Draft only — you paste & commit |

---

## 2. Dependency graph

```text
[M1 soak + daily tick] ──(until 07-06)──► [C1-01 Day 14 PASS] ──H1-01 sign──┐
                                                                              ▼
                                                                    [C1-02 pre-flip verify]
                                                                              ▼
                                                                    [H1-02 PB-12 GO] ──► [H1-04 public]
                                                                              │              │
                                                                              ▼              ▼
                                                                    [H1-06 catalog bump]  [D1-01 PB-10 #78]
```

**No branch requires Cursor Agent.**

---

## 3. Three deployment schemes (100% manual)

**Tools (no Cursor):** VS Code / vim · git · docker · SSH VPS · `gh` CLI (optional) · phone calendar · Claude Project (draft only, optional).

---

### Scheme A — Minimal daily ritual (~15 min/day)

*Best for:* one operator, stable soak loops, batch git commits acceptable.

#### A0 — One-time setup

- [x] MSI: `restart_soak_loop.sh` running
- [x] VPS: `acp-soak.service` enabled
- [ ] Set 3 calendar alarms: **2026-07-06** Day 14 · **2026-07-07** pre-flip · **2026-07-10** PB-12

#### A1 — Every day (2026-06-29 → 2026-07-05), ~15 min

**MSI (WSL):**

```bash
cd /mnt/d/Projects/ai-control-plane   # adjust clone path
docker compose -f examples/minimal/docker-compose.yml ps
tail -3 docs/governance/PB9_SOAK_ITERATION_LOG.md
# Expect: soak_iter health=ok … within last ~1h
```

If no new line in >2h:

```bash
bash scripts/restart_soak_loop.sh
```

**VPS (SSH, ~2 min):**

```bash
export ACP_REPO=/root/AI-Control-Plane
tail -3 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
sudo systemctl is-active acp-soak.service acp-staging.service
```

**Tick (editor):**

1. Open `docs/governance/PB9_STAGING_SOAK_LOG.md`
2. Today’s row (UTC): ☑ all four columns if soak OK; SEV = 0
3. One-line Notes if event occurred

**Commit (choose one):**

- *Daily:* `git add docs/governance/PB9_STAGING_SOAK_LOG.md docs/governance/PB9_SOAK_ITERATION_LOG.md && git commit -m "ops: PB-9 tick YYYY-MM-DD" && git push origin master`
- *Weekly batch:* tick each day on time; push Sunday — **dates in table must still be correct**

#### A2 — ~2026-07-06 (Day 14), ~2h

1. Copy [`PB9_DAY14_REVIEW_TEMPLATE.md`](PB9_DAY14_REVIEW_TEMPLATE.md) → `docs/governance/practice-evidence/pb-9-day14-review/RESULTS.md`
2. Count PASS/ERROR in `PB9_SOAK_ITERATION_LOG.md`
3. SSH VPS — paste last ~20 lines of `vps-soak-iteration.log` into RESULTS
4. Run verify on MSI:

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

5. Select verdict **PASS** / CONDITIONAL / FAIL — sign name + date in RESULTS
6. `git add` · `commit` · `push`
7. GitHub: close **#77** if PASS

#### A3 — ~2026-07-07 (pre-flip), ~30 min

```bash
git pull origin master
python scripts/export_openapi.py
git diff docs/openapi/openapi.json   # commit only if changed
pytest tests/test_smoke.py -q -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

**Do not** re-tag `v0.1.0-rc.1` (@ `c58b4cc`).

#### A4 — ~2026-07-10 (PB-12), ~1h — human only

1. Read [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) — confirm checklist
2. Write in RESULTS or issue: *"PB-10 deferred GA; 0.x ships without 30-day production soak"*
3. **Maintainer signs GO**
4. GitHub → Settings → Change visibility → **Public**
5. Releases → **`v0.1.0-beta.1`** from existing rc.1 — 0.x disclaimer in notes
6. Maintainer: update `src/ai_control_plane/core/governance_catalog.py` — move practice-PASS gates to `gates_closed`, update `public_beta.phase` → PR → merge
7. Open / track **#78** (PB-10) post-flip

---

### Scheme B — Dual-host high discipline (MSI + VPS parity)

*Best for:* strong Day 14 evidence; daily SSH; periodic verify.

#### B0 — Weekly startup (Sunday, ~45 min)

| Step | MSI | VPS |
|------|-----|-----|
| 1 | `git pull` | `cd $ACP_REPO && git pull` |
| 2 | `docker compose … up -d` | `sudo systemctl restart acp-staging` |
| 3 | `bash scripts/restart_soak_loop.sh` | `sudo systemctl restart acp-soak` |
| 4 | `pgrep -af soak_staging` | `systemctl status acp-soak` |
| 5 | Smoke 8/8 if `src/` changed | `verify_governance_status_runtime.sh` |

Record in Sunday Notes row in `PB9_STAGING_SOAK_LOG.md`.

#### B1 — Every day (~25 min)

**Morning (UTC):**

1. MSI + VPS: tail machine logs — same pattern `health=ok policy_allowed=True`
2. `curl -sf $ACP_API_URL/health` on both hosts
3. On FAIL: `docker logs` / `journalctl -u acp-soak` — fix before tick

**Evening:**

4. Tick `PB9_STAGING_SOAK_LOG.md`
5. Commit **same day** — include MSI iteration log in repo

**VPS after `git pull`:**

| Change type | Action |
|-------------|--------|
| `docs/` only | pull — **no** restart |
| `src/` or `examples/minimal/` | `systemctl restart acp-staging` then `acp-soak` |
| `scripts/soak_staging.sh` | restart `acp-soak` |

See [`examples/minimal/systemd/README.md`](../../examples/minimal/systemd/README.md).

#### B2 — Every 3 days: PACE mini-audit (~20 min)

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

Optional: save output to `~/acp-ops/pace-YYYY-MM-DD.txt` (local only).

#### B3 — Day 14 (~half day)

All of **A2**, plus:

- Full SEV table in RESULTS
- Compare MSI vs VPS iteration counts (timezone skew OK; ERROR pattern not OK)
- Paste `curl …/governance/status` → `len(gates_remaining)` = **7**
- Two-person review if available: one reads, one signs

#### B4 — Pre-flip + PB-12

All of **A3 + A4**, plus:

- Full suite: `pytest tests/ -q` (177) on MSI before flip
- `gh release create v0.1.0-beta.1 …` if using CLI
- Post-flip: probe `gh api repos/DataXMind/AI-Control-Plane/branches/master/protection` — record PB-11 outcome

---

### Scheme C — Weekly sprint calendar (burst on milestones)

*Best for:* busy weekdays; soak runs 24/7 via systemd; **still must tick enough days in human table**.

#### C0 — Principles

- **Soak:** always 24/7 (VPS systemd + MSI nohup loop)
- **Human tick:** minimum **3×/week** (Mon, Thu, Sun) — **daily tick recommended** for Day 14
- **Burst:** Sunday = verify + git push + backfill ticks if batching

#### C1 — Week 1 (2026-06-29 → 2026-07-03)

| Day | Minimum work |
|-----|----------------|
| Mon, Wed, Fri | 10 min: tail MSI + VPS logs → tick 1 day |
| Sun | `git pull` both hosts · restart soak if needed · backfill missing ticks · push |

#### C2 — Week 2 (2026-07-04 → 2026-07-10)

| Day | Work |
|-----|------|
| 04–05 Jul | Tick + keep soak |
| **06 Jul** | **Day 14 burst** — full A2/B3 |
| **07 Jul** | Pre-flip A3 — **only if Day 14 PASS** |
| 08–09 Jul | Draft PB-12 memo (editor / Claude Project) — PB-10 defer text |
| **10 Jul** | PB-12 burst A4 — public + release + catalog PR |

#### C3 — Quick tick template

```markdown
| YYYY-MM-DD | ☑ | ☑ | ☑ | ☑ | 0 | MSI+VPS hourly OK; SEV=0 |
```

#### C4 — If Day 14 FAIL

1. FAIL verdict in RESULTS — document extension days
2. **No** flip · **no** public
3. Fix root cause → extend soak → repeat calendar

---

## 4. Scheme comparison

| Criterion | A — Minimal | B — Dual-host | C — Weekly sprint |
|-----------|-------------|---------------|-------------------|
| Time/day | ~15 min | ~25–45 min | 10 min × 3 + Sun burst |
| Day 14 evidence | OK if logs steady | Strongest | Risk gaps if ticks skipped |
| Cursor dependency | 0 | 0 | 0 |
| Best for | 1 ops-savvy operator | Strict audit / 2 hosts | Busy schedule + systemd |

**Recommendation:** **B** for unquestionable Day 14; **A** if soak stable since 2026-06-28; **C** only if daily table stays complete.

---

## 5. Critical notes (agent-independent)

1. **Tick ≠ machine log** — missing ticks weakens human evidence even if logs run.
2. **`git pull` docs-only** — no soak restart (verified VPS 2026-06-28).
3. **Never claim `gates_remaining` closed in chat** — maintainer edits catalog @ flip.
4. **PB-8 @ `c58b4cc`** — flip uses `v0.1.0-beta.1`; do not re-tag rc.1.
5. **Smoke requires `.venv`** on MSI — `source .venv/bin/activate` before pytest.
6. **VPS log is gitignored** — paste excerpt into `RESULTS.md` for Day 14.
7. **Post-flip:** PB-10 (#78) is GA track — separate from 0.x beta ship.

---

## 6. Printable desk checklist

```
□ Soak MSI running (tail PB9_SOAK_ITERATION_LOG.md)
□ Soak VPS running (tail vps-soak-iteration.log)
□ Tick PB9_STAGING_SOAK_LOG.md (UTC today)
□ SEV-1/2 = 0
□ ~2026-07-06: RESULTS.md Day 14 + close #77 if PASS
□ ~2026-07-07: export_openapi + smoke 8/8 + verify_*
□ ~2026-07-10: PB-12 GO + public + v0.1.0-beta.1 + catalog bump
□ Post-flip: start PB-10 clock #78
```

---

## 7. Related documents

- [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) — OP-01..11 register
- [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) — daily human table
- [`PB9_DAY14_REVIEW_TEMPLATE.md`](PB9_DAY14_REVIEW_TEMPLATE.md) — Day 14 structure
- [`CLAUDE_PROJECT_SETUP.md`](../prompts/CLAUDE_PROJECT_SETUP.md) — optional drafting on claude.ai
- [`practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) — gate checklist

**Last updated:** 2026-06-28 · playbook author: operator audit wave
