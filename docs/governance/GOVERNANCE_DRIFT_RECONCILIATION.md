# Governance drift reconciliation — HTML artifacts vs master @ Studies 01–07

**Document ID:** ACP-GOV-DRIFT-RECON-001  
**Reconcile date:** 2026-06-25  
**Baseline code:** `master` post PR #89 (`30ace00`)  
**HTML sources (Claude pre–Gov UX / pre–Studies):**
- `karpathy_acp_artifacts_fixed.html` — CURSOR_RISK_POLICY, CLAUDE.md, deploy packet, 14-item checklist
- `lessons_learned_md.html` — LESSONS_LEARNED P-01..P-07

**Live SSOT after operator work:**
- [`GOVERNANCE_UX_RUNTIME.md`](GOVERNANCE_UX_RUNTIME.md) — CS-01..06 runtime catalog
- [`practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md)

**Post-G0 closure:** PR [#90](https://github.com/DataXMind/AI-Control-Plane/pull/90) merged 2026-06-25 (`c6e8cc1`). §1 table below is the **pre-G0 snapshot** (why reconciliation was opened). Current drift severity → see **§1.1**.

---

## 1. Executive verdict (pre-G0 snapshot @ open)

> **Do not use this table for go/no-go after #90.** Use §1.1.


| Area | HTML artifact state | Master @ 2026-06-25 | Drift severity |
|------|---------------------|----------------------|----------------|
| 6-layer `.cursorrules` | Deploy checklist item | ✅ Deployed (R1) | **Low** — needs L1/L5 refresh |
| `CURSOR_RISK_POLICY.md` | Full L2 (F1–F10, PR template) | Condensed L2 (F1–F7) | **Medium** — missing F8–F10, PR template |
| `LESSONS_LEARNED.md` | P-01..P-07 rich registry | Patterns 1–7 different mapping | **High** — P-05/P-06 missing; numbering diverged |
| `CLAUDE.md` | Root L0 constitution | **Not in repo** | **High** — R1-B never merged |
| Deploy checklist | 14 items, pytest **156** | Partially done | **High** — counts stale |
| Gov UX runtime | Not in HTML | ✅ PR #86 | **N/A** — new capability |
| Practice Studies 01–07 | Not in HTML | ✅ PASS + audit pack | **N/A** — new evidence layer |
| PB-9 soak | Not in HTML | 🔄 calendar IN PROGRESS | **Info** — separate clock |

**Rule for Claude:** When HTML artifact conflicts with `practice-evidence/` or `GOVERNANCE_UX_RUNTIME.md`, **live operator evidence + code** win. Mark HTML tabs as **historical design** unless reconciled here.

### 1.1 Post-G0 closure @ PR #90 (`c6e8cc1`)

| Area | Status after #90 | Residual |
|------|------------------|----------|
| 6-layer `.cursorrules` | ✅ L1/L5 refreshed | None |
| `CURSOR_RISK_POLICY.md` | ✅ Ops #7–11, PR template, waiver | Labeling uses numbers not “F8” — cosmetic |
| `LESSONS_LEARNED.md` | ✅ P-01..P-12 | Quarterly review calendar open (G1-3) |
| `CLAUDE.md` | ✅ Root file | Link from CONTRIBUTING optional (G1) |
| Deploy checklist pytest 156 | ✅ Reconciled → 165 in CURSOR_RISK | HTML still 156 — historical |
| Gov UX + Studies 01–07 | ✅ | CS-01/03/04 weak — see pre-approval audit §7 |
| PB-9 soak | 🔄 | **Ops gap** — daily log unchecked |
| ML5 memory pack | ✅ | `AGENTS.md`, `.cursor/rules/`, GP-01, CI `governance-memory` |

**Next audit:** [`GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md`](GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md)

### 1.2 Post-G1 wave @ `638250c` (PR #91–#96)

| Area | Status | Notes |
|------|--------|-------|
| L0 `CLAUDE.md` | ✅ Full Karpathy prompt | #95 |
| L2 `CURSOR_RISK_POLICY.md` | ✅ F1–F11, §1–§5 full | #94 |
| L5 `LESSONS_LEARNED.md` | ✅ P-01..P-12 enriched | #96 |
| ML5 pack | ✅ | #91 — `AGENTS.md`, `.cursor/rules/`, GP-01 |
| `cli/gov.py` coverage | ✅ 100% | #93 `test_cli_gov.py` |
| pytest baseline | **176** (SMK **8/8**) | Not 156 — HTML historical |
| Meta-drift (Karpathy §3.3) | ✅ Refreshed | This reconcile + Karpathy plan |
| PB-9 soak log | 🔄 | Operator — daily tick still required |
| G1-4 addendum | ✅ | `GOV_6LAYER_AUDIT_PASS.md` post-studies section |

### 1.4 Post-ECC 48H @ `1dd8f31` (catalog v1.5.0 · PR #146–#151)

| Area | Status | Residual |
|------|--------|----------|
| ECC 48H docs track | ✅ PASS | Study 09 / AgentShield deferred |
| Runtime v1.5.0 / 17 patterns | ✅ @ compose local | [`ecc-48h-post-verify/RESULTS.md`](practice-evidence/ecc-48h-post-verify/RESULTS.md) |
| GHCR `demo` image | ✅ coupling @ PR #157 | Auto-republish on `governance_catalog.py` push; `verify_ghcr_catalog.sh` |
| `SESSION_ANCHOR_TEMPLATE` | ✅ Reconciled | Was v1.3.3 — P-14 |
| Historical HTML / handoff @ v1.3.3 | 📁 Historical | Do not use for go/no-go |
| PB-9 soak | 🔄 | Operator calendar unchanged |

---

## 2. Timeline (context anti-drift)

```text
[HTML artifacts]     Karpathy 6-layer proposal + deploy packet (pytest 156 era)
        ↓
[R1–R3 governance]   .cursorrules 6-layer, CURSOR_RISK (condensed), LESSONS (7 patterns)
        ↓
[PR #86]             GET /governance/status, agentctl gov, CS-01..06 catalog
        ↓
[Studies 01–07]      Operator hands-on: Profile A/B/C, ops, multi-host, Tailscale
        ↓
[PR #89]             PRACTICE_STUDIES_AUDIT_01-07.md
        ↓
[This doc]           Reconcile HTML ↔ master; plan Phase G1–G4
```

---

## 3. LESSONS_LEARNED.md — pattern mapping

| HTML ID | Repo before reconcile | Status | Action |
|---------|----------------------|--------|--------|
| P-01 Monolithic PR | Pattern 1 | ✅ Same intent | Merge rich format |
| P-02 Doc scope creep | Pattern 2 | ✅ Same | Merge |
| P-03 GitHub ranges | Pattern 3 | ✅ Same | Merge |
| P-04 Silent ABAC | Pattern 4 | ✅ Same | Merge |
| P-05 Step 7 timing | **Missing** | ❌ Gap | **Add** |
| P-06 SAPAL scope reduction | **Missing** | ❌ Gap | **Add** |
| P-07 Doc drift | Partial (Pattern 5 overlap) | ⚠️ Split | P-07 = sprint doc sync; P-08 = stale `.cursorrules` |
| — Kill switch HTTP 200+deny | Claude HTML → "P-08" | Info | **P-13** @ G2-1 (P-08 already taken — F9) |
| — Stale `.cursorrules` | Pattern 5 | ✅ Keep as P-08 |
| — Pilot no branch | Pattern 6 | ✅ Keep as P-09 |
| — Gov UX runtime | Pattern 7 | ✅ **RULE ENCODED** → P-10 |
| — HTML artifact stale | **New** | ⚠️ | **P-11** (this reconciliation) |
| — WSL portproxy / multi-host | **New** from Study 06 | Info | **P-12** ops note |

Full merged registry: [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md).

---

## 4. `.cursorrules` drift analysis

| Topic | HTML / deploy packet | Current `.cursorrules` | Fix |
|-------|---------------------|------------------------|-----|
| `CURSOR_RISK` path | `docs/CURSOR_RISK_POLICY.md` | `docs/governance/CURSOR_RISK_POLICY.md` | ✅ Repo path correct — HTML wrong |
| Forbidden ops | F1–F10 | F1–F6 only | Add F7–F10 (see CURSOR_RISK) |
| Milestone L1 | N/A | A/B/C/C+ CLOSED, PB IN PROGRESS | ✅ Correct |
| Gov UX / practice | Not present | Missing | Add L1 pointers |
| pytest baseline | 156 | Not stated in rules | L4 in CURSOR_RISK = 165 |
| `CLAUDE.md` pointer | Expected at root | Missing | Add after R1-B |
| Last updated | Deploy era | 2026-06-22 | → 2026-06-25 |

**Why `.cursorrules` diverged from HTML deploy packet:** Deploy packet was a **one-shot Cursor prompt**; repo received **condensed** R1 merge (`low/gov-karpathy-rearch-import`) without full HTML §4–§5 (PR template, waivers) or `CLAUDE.md`. Subsequent work (Gov UX #86, Studies 01–07) updated **downstream** docs but not L0/L5 pointers.

---

## 5. CURSOR_RISK_POLICY.md drift

| HTML section | In repo? | Notes |
|--------------|----------|-------|
| §1 Risk levels (full prose) | Partial table | Repo shorter — OK if F-rules complete |
| §2 Forbidden F1–F10 | F1–F7 only | **Add F8–F10** |
| §3 PR size enforcement | In table | ✅ |
| §4 PR body template | **Missing** | **Add** |
| §5 Waiver process | **Missing** | **Add** |
| Verify gate pytest count | 165 | HTML deploy: 156 — **repo correct** |

**F-rules gap detail:**

| ID | HTML rule | In repo? |
|----|-----------|----------|
| F7 | Mark sprint DONE before PRs on master | ❌ |
| F8 | Skip assumptions step for ABAC/policy | ❌ (covered in L0 prose only) |
| F9 | Delete LESSONS_LEARNED entries | ❌ |
| F10 | core/ imports from mcp/ or cli/ | Partial (invariant list only) |

---

## 6. CLAUDE.md drift

| Field | HTML artifact | Repo |
|-------|---------------|------|
| File exists | Yes (tab content) | **No** |
| Karpathy 4 principles | Full | In `.cursorrules` L0 only |
| ACP-specific invariants | Listed | `.cursorrules` L3 |
| Path to CURSOR_RISK | `docs/CURSOR_RISK_POLICY.md` | Should be `docs/governance/...` |
| Lessons pointer | Yes | N/A until file created |
| Practice evidence | N/A | **Should add** post Studies 01–07 |

**R1-B status:** Planned in [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) — **still open**.

---

## 7. Studies 01–07 vs HTML governance model

| Governance layer | What Studies proved | CS / invariant |
|------------------|---------------------|----------------|
| L4 Evaluation | SMK 8/8 (Study 01); shipped parity via Profile B | CS-06 partial |
| L4 Runtime | `gov status` remote (06–07) | CS-02 visibility |
| L4 PB-9 | soak local (03) + remote (07) | **CS-05** strong slice |
| L3 Ops | portproxy, URL mismatch, Docker conflict | P-12 new |
| Invariant #4 | CLI HTTP-only across LAN + Tailscale | Studies 06–07 |

**Not proven by Studies (do not claim):** CS-01, CS-03, CS-04 hands-on; ~~5g kill switch~~ **proven G2-1**; 14-day PB-9 calendar.

Cross-reference: [`practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md).

---

## 8. Deploy checklist (HTML) — honest status

| # | Item | Status @ master |
|---|------|-----------------|
| 1–3 | Pre-deploy read / baseline / branch | ✅ Historical |
| 4 | Create `CLAUDE.md` | ❌ **Open** |
| 5 | Create `CURSOR_RISK_POLICY.md` | ✅ `docs/governance/` |
| 6 | Create `LESSONS_LEARNED.md` | ✅ Needs P-05/P-06 merge |
| 7 | Replace `.cursorrules` 6-layer | ✅ |
| 8 | ARCHITECTURE links | ✅ Partial (RISK only) |
| 9 | DEVELOPMENT_PROTOCOL sprint item | ⚠️ Verify |
| 10–13 | Verify + PR merge | ✅ Governance PRs merged |
| 14 | Post-deploy Cursor session | 🔄 Ongoing (Studies = extended validation |

---

## 9. Supersession rules (for Claude)

1. **Code + `ARCHITECTURE.md`** > reconciliation doc > HTML artifact > old audit HTML snapshots.
2. **`practice-evidence/RESULTS.md`** > conversation memory for operator runs.
3. **`GOVERNANCE_UX_RUNTIME.md`** > static HTML panes for CS-01..06 **runtime** wording.
4. HTML `karpathy_acp_artifacts_fixed.html` deploy packet pytest **156** → use **165** from CI / `CURSOR_RISK_POLICY.md`.
5. New drift event → row in `LESSONS_LEARNED.md` (P-11+) before next sprint close.

---

## 10. HTML / Claude artifact SSOT registry (@ 2026-06-27)

**Rule:** Do not execute stale prompts from HTML tabs. Use **code + practice-evidence + this doc**.

| Artifact | SSOT? | Stale claims (ignore) |
|----------|-------|------------------------|
| `governance_catalog.py` + `/governance/status` | **YES** | — |
| `GOVERNANCE_UX_RUNTIME.md` | **YES** | — |
| `GOVERNANCE_CATALOG_CLAUDE_SYNC_AUDIT.md` | **YES** | Maps Claude 3-stream prompt |
| `PB11_LEGAL_AUDIT.md` | **YES** | Legal sign-off |
| `practice-evidence/TASK_AUDIT_REMAINING_*.md` | **YES** | PB-12 open gates |
| `practice_studies_architecture_review.html` | Historical | Legal ABSENT; G-01 SKIPPED |
| `acp_full_audit_report.html` | Historical | SECURITY/CONTRIBUTING absent |
| `audit_reconcile_final.html` | Historical | Legal 0%; pytest 156 |
| `karpathy_acp_artifacts_fixed.html` | Historical | Pre-ML5 counts |
| Claude action packets (external) | Historical | Create legal files; fork JSON sample; **responsibility matrix @ 2026-06-26** |
| `CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md` | **YES** | Maps matrix rows → current status |
| `pb_final_blockers_packet.html` | Historical | [`PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md`](PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md) |
| `PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md` | **YES** | PB HTML tabs → current status |
| `pb_openapi_and_examples_ci.html` | Historical | [`PB_OPENAPI_AND_EXAMPLES_CI_RECONCILIATION.md`](PB_OPENAPI_AND_EXAMPLES_CI_RECONCILIATION.md) |
| `PB_OPENAPI_AND_EXAMPLES_CI_RECONCILIATION.md` | **YES** | OpenAPI + examples CI packet |
| `acp_status_audit_analysis.html` | Historical | [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md) |
| `ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md` | **YES** | Claude status audit → operator action plan |
| `PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` | **YES** | OP-01..11 task register through PB-12 |

**Onboarding:** `curl /governance/status` + [`CONTRIBUTING.md`](../../CONTRIBUTING.md) post-deploy checks.

---

## 11. Operator phase (@ 2026-06-27)

Engineering packets merged (#116–#118). Active phase = **operator pipeline** per [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md). Claude/Cursor: reconciliation + templates only unless operator requests code.

---

**Next:** [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](PUBLIC_BETA_OPERATOR_ACTION_PLAN.md)  
### 1.5 Post-roadmap P0–P2 @ `ad3d58a` (PR #153–#161)

| Area | Status | Residual |
|------|--------|----------|
| P-14 `gate_details` / `gates_blocking_pb12` | ✅ | `gates_remaining` still 7 until flip bump |
| P-15 k6 load smoke | ✅ `k6-policy-smoke/` | Not fleet-scale SLO proof |
| GHCR catalog coupling | ✅ auto-republish + verify script | Operator must `docker pull` after publish |
| `evaluation_path` on `/policy/evaluate` | ✅ | OIDC / identity federation deferred |
| Study 09 MCP inventory | ✅ | cyanheads E2E still `[mcp-unverified]` |
| SAPAL positioning | ✅ demoted @ 0.x | apex MVP unchanged |
| pytest baseline | **181** SMK **8/8** | — |
| PB-9 soak | 🔄 | Operator calendar unchanged |

**Last updated:** 2026-06-30 @ v1.5.0 post-roadmap reconcile

### 1.6 Mac Tier A pilot @ `8a4e7fa` (PR #172–#175)

| Area | Status | Residual |
|------|--------|----------|
| Production compose + `.env.production.example` | ✅ merged #172 | OIDC still PROPOSED (ADR-002) |
| `verify-pilot.sh` / `run-pilot-without-compose.sh` | ✅ merged #175 | — |
| Dockerfile `pip install -e ".[redis]"` | ✅ merged #175 | GHCR `demo` tag may lag until republish |
| Mac Mini operator PASS | ✅ 2026-06-30 | [`mac-pilot-deploy-2026-06-30/RESULTS.md`](practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md) |
| `policy_rules_count: 10` on pilot | ✅ Profile **B** bind mount | **Not** PB-9 fixture (8 rules) |
| PB-9 soak calendar | 🔄 unchanged | Pilot stack ≠ soak evidence stack |

**Drift rejects (pilot):** `export ACP_CONFIG_DIR` on host does not mount into Docker — use `ACP_HOST_CONFIG_DIR` in `.env.production`. `scripts/verify_*` from **repo root**, not `examples/minimal/`. `docker compose` plugin required on macOS (Docker Desktop or `brew install docker-compose`).

**Last updated:** 2026-06-30 @ Mac pilot evidence reconcile

---

**Last updated (§1 registry):** 2026-06-27 @ v1.3.3 artifact registry

---

## §12 — Composite drift risk khi đọc nhiều artifact cùng lúc

**Rủi ro:** Khi một phiên agent đọc **nhiều file lịch sử cùng lúc** (ví dụ: tổng hợp nhiều báo cáo Cursor thành một document dài), banner deprecation đơn lẻ trên từng file có thể **không đủ nổi bật** để ngăn trộn lẫn số liệu giữa các mốc thời gian khác nhau (ví dụ: SHA cũ + catalog version mới bị ghép sai).

**Rule bắt buộc cho agent:** Khi nhận một artifact tổng hợp (multi-session report, file `.docx` / `.md` dài >500 dòng tự ghép nhiều mốc thời gian), **PHẢI:**

1. Xác minh anchor hiện tại bằng **lệnh thật** trước khi tin bất kỳ SHA/version nào trong artifact đó (`git log -1 --oneline`, `curl …/governance/status`, `pytest --collect-only -q | tail -1`).
2. Gắn nhãn rõ **"theo báo cáo X, chưa verify độc lập"** cho mọi số liệu chưa confirm bằng output terminal thật.
3. **Không** tự nhảy anchor sang baseline mới chỉ vì artifact tự xưng "đã hoàn tất".

**SSOT anchor:** [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md) · `GET /governance/status` · `scripts/verify_governance_status_runtime.sh`
