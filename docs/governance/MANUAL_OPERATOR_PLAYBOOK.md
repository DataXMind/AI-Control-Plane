# Manual Operator Playbook — Public Beta (no Agent required)

**Document ID:** ACP-GOV-MANUAL-OPERATOR-PLAYBOOK-001  
**Audience:** Operator · maintainer · org admin  
**Phase:** PB-9 staging soak → PB-12 flip → PB-10 GA (deferred)  
**Baseline:** `master` @ **`4210ad2`** · catalog **v1.5.0** · **17** patterns · pytest **181**  
**Reference date:** **2026-07-01** · PB-9 human tick cuối: **2026-07-01** · **Tier A pilot PASS** Mac Mini (PR [#176](https://github.com/DataXMind/AI-Control-Plane/pull/176) merged)  
**SSOT companions:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) · [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md)

> **Purpose:** Execute all remaining Public Beta operator work **without Cursor Agent** — shell, editor, GitHub UI, SSH VPS, optional Claude Project for drafting only.  
> **Agent framework (when using AI):** [`docs/prompts/AGENT_OPERATING_SYSTEM.md`](../prompts/AGENT_OPERATING_SYSTEM.md) · **This file = human-only track**

---

## Go-live verdict (operator summary @ 2026-06-30)

| Tier | Ready? | Action |
|------|--------|--------|
| **A — Pilot nội bộ** (policy + Docker + YAML riêng) | **Có — ngay** (PASS Mac Mini 2026-06-30) | [`PRODUCTION_DEPLOY.md`](../../examples/minimal/PRODUCTION_DEPLOY.md) + evidence [`mac-pilot-deploy-2026-06-30/RESULTS.md`](practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md) — **không thay** stack PB-9 fixture soak |
| **B — Public Beta (PB-12)** | **Chưa** — chờ Day 14 ~**07-06** + human GO ~**07-10** | M1 tick 07-01..05 → C1-01 → H1-02 |
| **C — Production GA (1.0.0)** | **Chưa** — PB-10 deferred, OIDC/k6/MCP PROPOSED | Post-flip #78 |

**Critical path thực sự block PB-12 @ 0.x:** chỉ **PB-9 (calendar)** + **PB-12 (human GO)**. Mọi thứ khác đã PASS practice hoặc deferred.

---

## 0. Classification (strict)

| Axis | Definition | Owner | Needs Cursor? |
|------|------------|-------|---------------|
| **M1 — Continuous manual** | Repeat daily / keep services alive | Operator | **No** |
| **C1 — Calendar** | Cannot accelerate by will | Operator + time | **No** |
| **H1 — Human gate** | Signature / decision / org permission | Maintainer / org admin | **No** |
| **D1 — Dependency** | Only after prior step PASS | Operator | **No** |

### Drift rules (mandatory)

- Practice PASS ≠ `gates_remaining` drops — **catalog bump @ flip** (maintainer `governance_catalog.py` PR).
- PB-9 Day 14 = **~2026-07-06** (soak start **2026-06-22**), **not** 07-10 unless new SEV-1/2 extends soak.
- **PB-10 does not block** 0.x beta — record defer in PB-12 narrative.
- **Three soak layers — do not conflate:**

| Layer | Path | Owner |
|-------|------|-------|
| Human daily | `docs/governance/PB9_STAGING_SOAK_LOG.md` | Operator tick (PR) |
| MSI machine | `docs/governance/PB9_SOAK_ITERATION_LOG.md` | `restart_soak_loop.sh --repo-log` |
| VPS machine | `practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log` | `acp-soak.service` |

**Runtime @ pre-flip:** `gates_blocking_pb12` = **PB-9, PB-12** · `gates_remaining` = **7** (unchanged until flip bump).

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
| Engineering | Milestones A–C+, smoke, OpenAPI | Done | CI green · **181** tests |
| OP-08 | CHANGELOG #120, go-no-go #119 | Done | merged |
| SOAK-01..03 | Ticks 06-29 reconcile, 06-30, RUNBOOK `.venv` | Operator/docs | PR [#169](https://github.com/DataXMind/AI-Control-Plane/pull/169)–[#171](https://github.com/DataXMind/AI-Control-Plane/pull/171) |
| PROD draft | Production compose + Day 14 draft | Docs | PR [#172](https://github.com/DataXMind/AI-Control-Plane/pull/172) |
| ADR/prep | OIDC, k6 fleet, MCP CI, ADR-001 — **PROPOSED only** | Docs | PR [#165](https://github.com/DataXMind/AI-Control-Plane/pull/165)–[#168](https://github.com/DataXMind/AI-Control-Plane/pull/168) — **no implementation** |

### 1.2 M1 — Continuous (daily → ~2026-07-06)

| # | Task | Owner | Trigger | Artifact | Blocks flip? |
|---|------|-------|---------|----------|--------------|
| M1-01 | Keep MSI Docker stack up (**PB-9 fixture**) | Operator | Daily | `docker compose -f examples/minimal/docker-compose.yml ps` healthy | Indirect |
| M1-02 | Keep MSI soak loop | Operator | Daily / after reboot | New lines in `PB9_SOAK_ITERATION_LOG.md` ~hourly | **Yes** |
| M1-03 | Keep VPS `acp-staging` + `acp-soak` | Operator | Daily | `vps-soak-iteration.log` + `/var/log/` | **Yes** |
| M1-04 | **Daily tick** human table | Operator | After 00:00 UTC when soak OK | `PB9_STAGING_SOAK_LOG.md` → **PR** | **Yes** |
| M1-05 | `git pull` MSI/VPS | Operator | After remote push | No soak restart if **docs-only** | No |
| M1-06 | Watch SEV-1/2 | Operator | On anomaly | Notes column; SEV-3 documented only | **Yes** if SEV-1/2 |

**Ticks remaining (UTC calendar):** **2026-07-02** through **2026-07-05** (+ review row **2026-07-06**).  
**Last human tick:** **2026-07-01** (Apex ☑ on MSI soak_iter).

**Known SEV-3 (documented, not blockers):**

- 2026-06-29: MSI ~13h Docker stop → restart 01:20Z
- 2026-06-29→30: iteration silence + manual rebuild during PR #163–168 verify — reconciled in soak log

**MSI iteration log @ 2026-06-30:** **21 PASS** / **0 ERROR** through `2026-06-29T11:26:07Z` — **re-count** on Day 14 after soak resumes post-restart.

### 1.3 C1 — Calendar (wait for date)

| # | Task | Owner | Target | Depends on | Artifact |
|---|------|-------|--------|------------|----------|
| C1-01 | Day 14 PB-9 review | Operator | **~2026-07-06** | ≥14 days from 2026-06-22 + clean soak | `practice-evidence/pb-9-day14-review/RESULTS.md` |
| C1-02 | Pre-flip refresh | Maintainer | **~2026-07-07** | C1-01 = PASS | `export_openapi.py`, smoke, verify, coverage ≥85% ([`COVERAGE_IMPROVEMENT_REPORT.md`](COVERAGE_IMPROVEMENT_REPORT.md)) |
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
| D1-05 | OIDC / k6 fleet / MCP E2E CI | Maintainer | PB-12 + pilot need | ADR-002, `K6_FLEET_TEST_PLAN.md`, MCP contract — **PROPOSED** |

### 1.6 Optional (not blocking PB-12)

| Task | When |
|------|------|
| Smoke 8/8 + `verify_*` on MSI | Before Day 14; after `src/` pull — **requires `.venv`** ([`RUNBOOK.md`](../RUNBOOK.md)) |
| **Pilot production stack** (Redis + host YAML) | Anytime — [`PRODUCTION_DEPLOY.md`](../../examples/minimal/PRODUCTION_DEPLOY.md) — **parallel** to PB-9 fixture soak |
| Witness PB-7 on third machine | Not required — CLEAN PASS exists |
| Re-test security@ | Not required — PASS 2026-06-28 |
| Complete Day 14 from draft | Start [`DAY14_REVIEW_DRAFT_2026-07-06.md`](practice-evidence/pb-9-day14-review/DAY14_REVIEW_DRAFT_2026-07-06.md) — not blank template |

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
- [x] Ticks 06-29 / 06-30 recorded (PR #169–#171)
- [ ] Set 3 calendar alarms: **2026-07-06** Day 14 · **2026-07-07** pre-flip · **2026-07-10** PB-12
- [ ] MSI: `python3 -m venv .venv && pip install -e ".[dev]"` (once)

#### A1 — Every day (2026-07-01 → 2026-07-05), ~15 min

**MSI (WSL):**

```bash
cd /mnt/d/Projects/ai-control-plane   # adjust clone path
docker compose -f examples/minimal/docker-compose.yml ps
tail -3 docs/governance/PB9_SOAK_ITERATION_LOG.md
# Expect: soak_iter health=ok … within last ~2h (gap 06-29→30 was SEV-3 manual restart)
```

If no new line in >2h:

```bash
bash scripts/restart_soak_loop.sh
```

After `src/` or `governance_catalog.py` change on pull:

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
```

**VPS (SSH, ~2 min):**

```bash
export ACP_REPO=/root/AI-Control-Plane
tail -3 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
sudo systemctl is-active acp-soak.service acp-staging.service
```

**Tick (editor):**

1. Open `docs/governance/PB9_STAGING_SOAK_LOG.md`
2. Insert row **between** previous day and `2026-07-06` if missing (do not edit 06-22..06-30 history)
3. Today (UTC): ☑ Health / Policy / Quota; ☑ Apex if soak shows `apex=ok`; SEV-1/2 = **0**
4. One-line Notes if event (SEV-3 → document in Notes, not SEV column)

**Commit via PR** ([`CONTRIBUTING.md`](../../CONTRIBUTING.md) — no direct push to `master`):

```bash
git checkout -b docs/pb9-tick-YYYY-MM-DD
git add docs/governance/PB9_STAGING_SOAK_LOG.md
# Add PB9_SOAK_ITERATION_LOG.md ONLY if soak --repo-log appended new lines since last commit
git commit -m "docs(pb-9): record daily tick YYYY-MM-DD"
git push -u origin docs/pb9-tick-YYYY-MM-DD
gh pr create --base master --head docs/pb9-tick-YYYY-MM-DD \
  --title "docs(pb-9): record daily tick YYYY-MM-DD" --body "Operator tick; smoke 8/8."
```

*Weekly batch:* still tick correct UTC dates in table; one PR with multiple days is OK if dates are accurate.

#### A2 — ~2026-07-06 (Day 14), ~2h

1. **Start from draft** (pre-filled through 06-30): copy [`DAY14_REVIEW_DRAFT_2026-07-06.md`](practice-evidence/pb-9-day14-review/DAY14_REVIEW_DRAFT_2026-07-06.md) → `RESULTS.md` — **not** blank template only
2. Re-count PASS/ERROR in `PB9_SOAK_ITERATION_LOG.md` (include lines after 06-30 restart)
3. SSH VPS — paste last ~20 lines of `vps-soak-iteration.log` into RESULTS
4. Run verify on MSI:

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke                    # expect 8/8
docker compose -f examples/minimal/docker-compose.yml up -d --build
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh        # expect 1.5.0 · 17 patterns
bash scripts/verify_openapi_runtime.sh
curl -sf "$ACP_API_URL/governance/status" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); pb=d['public_beta']; print(len(pb['gates_remaining']), pb.get('gates_blocking_pb12'))"
# expect: 7 ['PB-9', 'PB-12'] (approx — confirm from JSON)
```

5. Resolve **Apex ☐ on 06-30** — CONDITIONAL waiver in RESULTS if 07-01..05 Apex ☑ or last-known-good ≤48h documented
6. Verdict **PASS** / CONDITIONAL / FAIL — sign name + date
7. PR: `docs/pb9-day14-results` → merge
8. GitHub: close **#77** if PASS

#### A3 — ~2026-07-07 (pre-flip), ~30 min

```bash
git pull origin master
source .venv/bin/activate
python scripts/export_openapi.py
git diff docs/openapi/openapi.json   # commit only if changed
pytest tests/test_smoke.py -q -m smoke
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
pytest --collect-only -q | tail -3   # expect 181 collected
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
| 2 | `docker compose … up -d --build` if image stale | `sudo systemctl restart acp-staging` |
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
5. PR **same day** — human table + iteration log if new machine lines

**VPS after `git pull`:**

| Change type | Action |
|-------------|--------|
| `docs/` only | pull — **no** restart |
| `src/` or `examples/minimal/` (incl. `docker-compose.production.yml`) | `systemctl restart acp-staging` then `acp-soak` |
| `scripts/soak_staging.sh` | restart `acp-soak` |

See [`examples/minimal/systemd/README.md`](../../examples/minimal/systemd/README.md).

#### B2 — Every 3 days: PACE mini-audit (~20 min)

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
docker compose -f examples/minimal/docker-compose.yml up -d --build
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

Optional: save output to `~/acp-ops/pace-YYYY-MM-DD.txt` (local only).

#### B3 — Day 14 (~half day)

All of **A2**, plus:

- Full SEV table (include documented SEV-3 rows; confirm SEV-1/2 = 0)
- Compare MSI vs VPS iteration counts (timezone skew OK; ERROR pattern not OK)
- Paste `gates_remaining` = **7** from `curl …/governance/status`
- Two-person review if available: one reads, one signs

#### B4 — Pre-flip + PB-12

All of **A3 + A4**, plus:

- Full suite: `pytest tests/ -q` (**181** collected) on MSI before flip
- `gh release create v0.1.0-beta.1 …` if using CLI
- Post-flip: probe `gh api repos/DataXMind/AI-Control-Plane/branches/master/protection` — record PB-11 outcome

---

### Scheme C — Weekly sprint calendar (burst on milestones)

*Best for:* busy weekdays; soak runs 24/7 via systemd; **still must tick enough days in human table**.

#### C0 — Principles

- **Soak:** always 24/7 (VPS systemd + MSI loop) on **fixture** `docker-compose.yml`
- **Human tick:** minimum **3×/week** (Mon, Thu, Sun) — **daily tick recommended** for Day 14
- **Burst:** Sunday = verify + PR + backfill ticks if batching

#### C1 — Week of 2026-07-01 → 2026-07-03

| Day | Minimum work |
|-----|----------------|
| Tue 01, Thu 03 | 10 min: tail MSI + VPS logs → tick 1 day |
| Sun 05 Jul (or daily) | `git pull` both hosts · restart soak if needed · tick 01–05 · PR |

#### C2 — Week of 2026-07-04 → 2026-07-10

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

(Apex ☐ only if `/apex/trigger` not exercised — document in Notes.)

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

**Recommendation @ 2026-06-30:** **B** if Day 14 must be unquestionable (Apex gap + SEV-3 window); **A** if soak loop stable post-06-30 restart; **C** only if table stays complete through 07-05.

---

## 5. Critical notes (agent-independent)

1. **Tick ≠ machine log** — missing ticks weakens human evidence even if logs run.
2. **`git pull` docs-only** — no soak restart (verified VPS 2026-06-28; PR #163–168 docs wave).
3. **Never claim `gates_remaining` closed in chat** — maintainer edits catalog @ flip.
4. **PB-8 @ `c58b4cc`** — flip uses `v0.1.0-beta.1`; do not re-tag rc.1.
5. **Smoke requires `.venv`** on MSI — `source .venv/bin/activate` before pytest ([`RUNBOOK.md`](../RUNBOOK.md)).
6. **VPS log is gitignored** — paste excerpt into `RESULTS.md` for Day 14.
7. **Post-flip:** PB-10 (#78) is GA track — separate from 0.x beta ship.
8. **PB-9 soak ≠ production pilot** — fixture stack for evidence; `docker-compose.production.yml` is optional Tier A ([`PRODUCTION_DEPLOY.md`](../../examples/minimal/PRODUCTION_DEPLOY.md)).
9. **Stale Docker image** — `verify_governance_status_runtime.sh` may `KeyError: gates_blocking_pb12` until `docker compose … up --build`.
10. **SEV-3 ≠ SEV-1/2** — manual restart during verify is documented; does not extend calendar unless new SEV-1/2.

---

## 6. Printable desk checklist

```
□ Soak MSI running (tail PB9_SOAK_ITERATION_LOG.md)
□ Soak VPS running (tail vps-soak-iteration.log)
□ Tick PB9_STAGING_SOAK_LOG.md (UTC today) → PR   ← 07-01 done; next 07-02
□ SEV-1/2 = 0 (SEV-3 OK if documented)
□ 07-01..05: daily rows before Day 14
□ ~07-06: RESULTS.md from DAY14_REVIEW_DRAFT + close #77 if PASS
□ ~07-07: export_openapi + smoke 8/8 + verify 1.5.0·17 + 181 collect
□ ~07-10: PB-12 GO + public + v0.1.0-beta.1 + catalog bump
□ Post-flip: start PB-10 clock #78
```

---

## 7. Related documents

| Doc | Use |
|-----|-----|
| [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) | OP-01..11 register |
| [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) | Daily human table |
| [`DAY14_REVIEW_DRAFT_2026-07-06.md`](practice-evidence/pb-9-day14-review/DAY14_REVIEW_DRAFT_2026-07-06.md) | Day 14 pre-fill |
| [`PB9_DAY14_REVIEW_TEMPLATE.md`](PB9_DAY14_REVIEW_TEMPLATE.md) | Structure fallback |
| [`PRODUCTION_DEPLOY.md`](../../examples/minimal/PRODUCTION_DEPLOY.md) | Pilot Tier A (optional) |
| [`mac-pilot-deploy-2026-06-30/RESULTS.md`](practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md) | Tier A PASS evidence @ 2026-06-30 |
| [`CLAUDE_PROJECT_SETUP.md`](../prompts/CLAUDE_PROJECT_SETUP.md) | Optional drafting on claude.ai |
| [`TASK_AUDIT_REMAINING_2026-06-27.md`](practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) | Gate checklist (update @ Day 14) |

**Last updated:** 2026-07-01 · PB-9 tick 07-01 · baseline `4210ad2`
