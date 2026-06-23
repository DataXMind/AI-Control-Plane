# Phase 2 Sprint 1 — Consolidated Audit (FINAL)

**Document ID:** ACP-GOV-PHASE2-S1-AUDIT-FINAL  
**Version:** 2.0 FINAL  
**Date:** 2026-06-22  
**Supersedes:** [`PHASE2_SPRINT1_CONSOLIDATED_AUDIT.md`](PHASE2_SPRINT1_CONSOLIDATED_AUDIT.md) v1.0

**Sources verified:**

| Source | Items | Role |
|--------|-------|------|
| `sprint1_master_checklist_and_quickref.html` (Claude, mới) | **38** checklist + quick ref | DoD Sprint 1, HTTP contracts, coverage targets |
| `phase2_execution_completion.html` (Claude, cũ) | 47 checklist + 5 Cursor rules | Pipeline + Rule 1 (1 PR/task) |
| Repo `origin/master` @ `7f5dcd5` | — | Trạng thái production branch |
| Branch `phase2/p2-0-tool-naming-and-p2-2` @ `43dfe1e` | — | Sprint 1 work-in-flight (+ audit doc chưa commit) |
| Local gates (WSL venv) | 123 / 8 / 4 tests | pytest · smoke · shipped parity |

**Related:** [`PHASE2_SPRINT1_REPORT.md`](PHASE2_SPRINT1_REPORT.md) · [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md)

---

## 1. Verdict cho quyết định tiếp theo

| Câu hỏi | Trả lời ngắn |
|---------|--------------|
| Code Sprint 1 có đủ chất lượng merge? | **Có** — 123 pass, 82% cov, invariants OK, HTTP contracts đúng trên branch |
| Checklist 38/38 hoàn thành? | **Không** — ~**29/38** code trên branch · ~**12/38** trên master · process ~**15/38** |
| Sprint 1 "DONE" theo artifact? | **Chưa** — Step 7 + PR merge MB-S1 chưa xong trên master |
| Nên làm gì tiếp? | **Path A (khuyến nghị):** 1 PR merge 8 commits → master + issue hygiene |

---

## 2. Artifact mới — `sprint1_master_checklist_and_quickref.html`

### 2.1 Cấu trúc (2 tab)

| Tab | Nội dung |
|-----|----------|
| **Master checklist** | 38 items, 7 sections (PRE + Steps 1–7), progress bar 0/38 |
| **Quick reference** | Step sequence, HTTP contracts §3.3+§3.4, invariants #1/#2/#3/#4/#6/#7, coverage targets, non-goals Sprint 2 |

### 2.2 Khác biệt so với artifact cũ (47 items)

| Thay đổi | Ý nghĩa audit |
|----------|---------------|
| 38 items (gọn hơn 47) | Bỏ trùng lặp branch/PR; gộp Step 5a+5b thành **S5** (5 items) |
| Không tab "5 Cursor rules" | Rule 1 (1 PR/task) **vẫn implied** qua tên branch riêng từng step |
| HTTP contract table | **Chuẩn xác** — khớp implementation trên branch |
| Coverage baseline 64.5% → 72%+ | Branch đạt **82%** — vượt target |
| Non-goals rõ (Redis, MCP E2E, public) | Align Sprint 2 — không audit fail |

### 2.3 Quick ref — HTTP contracts (verified on branch)

| Endpoint | Condition | Expected | Branch |
|----------|-----------|----------|--------|
| `POST /policy/evaluate` | authorized | 200 + allow | ✅ |
| `POST /policy/evaluate` | denied | 200 + deny + reason | ✅ |
| `POST /policy/evaluate` | kill_switch | 200 + deny | ✅ |
| `POST /policy/evaluate` | unavailable | 503 | ✅ |
| `POST /identity/verify` | valid JWT | 200 + AgentIdentity | ✅ |
| `POST /identity/verify` | invalid JWT | 401 | ✅ SMK-06b |
| `POST /identity/verify` | unknown agent | 401 | ✅ SMK-06c (extra vs checklist) |
| `POST /identity/verify` | internal error | 503 | ✅ |
| `GET /health` | kill_switch bypass | 200 | ✅ |

**Lệch nhỏ vs checklist S6:** artifact ghi SMK-06a+06b; code có thêm **SMK-06c** (unknown agent) — **tốt hơn** plan.

---

## 3. Master checklist 38 items — verify từng item

**Legend:**  
- **B** = done on branch @ `43dfe1e`  
- **M** = done on `master` @ `7f5dcd5`  
- **P** = process item (branch/PR/issue)  
- ✅ / ⚠️ / ❌

### PRE — Pre-sprint (3)

| ID | Item | B | M | P | Verdict |
|----|------|---|---|---|---------|
| PRE-1 | Codecov token + `gh secret set` | — | — | N/A | Không re-verify; PHASE1 §8 ghi đã set |
| PRE-2 | `master @ 83e3ab5`: 91 pass · SMK 5/5 · ruff · mypy | — | ✅ | ✅ | Đúng tại sprint start |
| PRE-3 | MB Sprint 1 scope approved | — | — | N/A | Giả định human approve |

**PRE score: 1/3 verified · 2/3 N/A**

---

### S1 — P2-0+P2-2 (9)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S1-1 | Branch `phase2/p2-0-tool-naming-and-p2-2` | ✅ | ✅ | ✅ — nhưng **reuse** cho Steps 2–7 (vi phạm process) |
| S1-2 | `core/tool_names.py` + 3 exports | ✅ | ✅ | ✅ PR #44 |
| S1-3 | `loader.py` — no duplicate, import `tool_names` | ✅ | ✅ | ✅ |
| S1-4 | `mcp/git_server.py` imports `tool_names` | ✅ | ✅ | ✅ |
| S1-5 | `api/server.py` imports `resolve_policy_tool_name` | ✅ | ✅ | ✅ |
| S1-6 | `ARCHITECTURE.md` § Tool naming | ✅ | ✅ | ✅ |
| S1-7 | `DEVELOPMENT_PROTOCOL.md` P0-2b CLOSED | ✅ | ✅ | ✅ |
| S1-8 | Gate: 91 · SMK 5/5 · parity 4 · ruff · mypy | ✅ | ✅ | ✅ at P2-0 merge |
| S1-9 | PR merged · **#8 closed** · D3 closed | ⚠️ | ⚠️ | PR #44 merged; **#8 vẫn OPEN** |

**S1 score: 8/9 substance · 7/9 process (issue #8)**

---

### S2 — P2-1 Restrict-PII doc (4)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S2-1 | Branch `phase2/p2-1-pii-gap-doc` | ❌ | — | Không tạo — gộp branch |
| S2-2 | `ARCHITECTURE.md` § Policy YAML loading limits table | ✅ | ⚠️ | Master có doc P2-1; **full ABAC table** sau MB-S1-2 chỉ trên branch |
| S2-3 | GitHub GAP-ABAC-2 issue (#45) | ✅ | ✅ | Issue tồn tại — **vẫn OPEN** |
| S2-4 | PR merged · 91 pass docs-only | ⚠️ | ⚠️ | PR #46 merge kèm **agent4 config** (scope creep) |

**S2 score: 3/4 substance · 1/4 process**

---

### S3 — MB-S1-1 Guardrails (8)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S3-1 | Branch `milestone-b/s1-1-guardrails` | ❌ | — | Monolithic branch |
| S3-2 | `KillSwitch` in `models.py` + `__all__` | ✅ | ❌ | |
| S3-3 | `load_guardrails()` + `load_kill_switch()` | ✅ | ❌ | |
| S3-4 | `PolicyEngine` kill_switch + first-check deny | ✅ | ❌ | |
| S3-5 | `create_app()` wires guardrails + kill_switch | ✅ | ❌ | |
| S3-6 | Fixture `policies.yml` guardrails + kill_switch | ✅ | ❌ | |
| S3-7 | `test_guardrails.py` — 5 tests | ✅ **6** | ❌ | Vượt plan (OK) |
| S3-8 | Gate 96+ · SMK 5/5 · **PR merged** | ✅ 123 | ❌ | **#35 MB7 OPEN** |

**S3 score: 7/8 code · 0/8 on master · 0/8 PR merged**

---

### S4 — MB-S1-2 ABAC full (5)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S4-1 | Branch `milestone-b/s1-2-abac-full` | ❌ | — | |
| S4-2 | 3 evaluators implemented | ✅ | ❌ | |
| S4-3 | `load_policies()` loads role_not_in / approval_status / read_only | ✅ | ❌ | |
| S4-4 | New tests: PII+role_not_in, reviewer write, approval_status | ✅ | ❌ | |
| S4-5 | Regression 5 cases + **PR merged** | ✅ | ❌ | **#45 OPEN** |

**S4 score: 4/5 code · 0/5 master**

---

### S5 — MB-S1-3 coverage ∥ MB-S1-4 CLI (5)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S5-1 | `fail_under = 70` pyproject.toml | ✅ | ❌ | |
| S5-2 | `policies.py` ≥ 80% | ✅ **99%** | ❌ | |
| S5-3 | Total ≥ 70% · S1-3 PR merged first | ✅ **82%** | ❌ | Single branch, no separate PR |
| S5-4 | `test_cli_assign.py` 3 cases respx | ✅ | ❌ | |
| S5-5 | `test_cli_status.py` · cli ≥ 60% · Invariant #4 · PR | ⚠️ **~67%** | ❌ | Đạt floor; stubs approve/quota/logs 0% exec |

**S5 score: 5/5 code targets · 0/5 master**

---

### S6 — MB-S1-5 Identity JWT (5)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S6-1 | Branch `milestone-b/s1-5-identity-jwt` | ❌ | — | |
| S6-2 | `core/identity.py` JWTValidator HS256 stub | ✅ | ❌ | File **absent** on master |
| S6-3 | `/identity/verify` 401/503 contracts | ✅ | ❌ | |
| S6-4 | SMK-06a + SMK-06b | ✅ + **06c** | ❌ | |
| S6-5 | SMK 6/6 · ARCHITECTURE contract · **PR merged** | ✅ 8 smoke | ❌ | |

**S6 score: 4/5 checklist · 5/5 contracts on branch · 0/5 master**

---

### S7 — Archive + close (4)

| ID | Item | B | M | Verdict |
|----|------|---|---|---------|
| S7-1 | HTMLs in `docs/governance/` | ✅ | ✅ | Archived Milestone A; skip move |
| S7-2 | `PHASE2_SPRINT1_REPORT.md` | ✅ | ❌ | Close commit cần = merge SHA |
| S7-3 | `MILESTONE_B_BACKLOG.md` Sprint 1 DONE | ✅ | ❌ | |
| S7-4 | Final gates + **PR merged** | ✅ local | ❌ | Step 7 **sớm** vs artifact ("after all PRs merged") |

**S7 score: 3/4 docs on branch · 1/4 on master (HTML only) · 0/4 closed**

---

### 3.1 Tổng điểm checklist 38 items

| Layer | Done | Total | % |
|-------|------|-------|---|
| **Code/substance (branch)** | ~29 | 35* | **~83%** |
| **On master** | ~12 | 38 | **~32%** |
| **Process (branch/PR/issue đúng plan)** | ~15 | 38 | **~39%** |
| **Strict 38/38 (artifact DoD)** | — | 38 | **0%** |

\*35 = 38 trừ 3 PRE items không verify được

---

## 4. Pipeline thực tế vs artifact (cả 2 HTML)

```text
PLANNED (cả 2 artifacts):
  S1 → S2 → S3 → S4 → S5 → S6 → S7   (7 branch, 7+ PR)

ACTUAL:
  master: S1 (PR#44) + S2 partial (PR#46) + agent4 early
  branch: S3+S4+S5+S7 docs  (8 commits chưa merge)
```

**Bug ordering (vẫn valid):** `agent4` + PII restrictions trên master **trước** ABAC `role_not_in` code.

---

## 5. Coverage targets (quick ref vs actual, branch)

| Metric | Target (artifact) | Branch actual | master |
|--------|-------------------|---------------|--------|
| Total | ≥ 70% (fail_under) | **82.16%** | ~64–70% |
| `core/policies.py` | ≥ 80% | **99%** | thấp hơn |
| `cli/` | ≥ 60% | **~67%** | thấp hơn |
| `mcp/git_server.py` | (không gate S1) | **53%** | risk Sprint 2 |

---

## 6. Ba lựa chọn quyết định

| Path | Mô tả | Effort | Rủi ro |
|------|-------|--------|--------|
| **A — Merge forward (khuyến nghị)** | 1 PR: 8 commits branch → master + đóng issues + sửa docs | ~1–2h | Thấp — code đã verify |
| **B — Merge + harden** | Path A + shipped PII parity test + sync PHASE1_REPORT | ~2–3h | Thấp nhất governance |
| **C — Revert & replay pipeline** | Revert agent4/PR#46, tách 7 PR retroactive | ~2–3 ngày | Cao — không cần thiết |

---

## 7. Hành động: CÓ THỂ vs KHÔNG THỂ

### ✅ Có thể thực hiện ngay (feasible)

| # | Hành động | Ai | Effort | Impact |
|---|-----------|-----|--------|--------|
| F1 | **Mở PR** `phase2/p2-0-tool-naming-and-p2-2` → `master` (8 commits) | Human + Cursor | 30 min | **Unblock Sprint 1** |
| F2 | Chờ **CI green** (Smoke + Full suite + shipped parity) | CI | auto | Gate bắt buộc |
| F3 | **Merge PR** sau CI + review | Human | 5 min | MB-S1 lên master |
| F4 | **Đóng issues** #35, #45, #8 kèm merge SHA + comment | Human (`gh`) | 15 min | Sync GitHub ↔ code |
| F5 | Cập nhật `PHASE2_SPRINT1_REPORT.md` close commit = merge SHA | Cursor | 10 min | Doc truth |
| F6 | Thêm **shipped PII parity test** (Restrict-PII + role_not_in) | Cursor | 30–45 min | Đóng gap #45 evidence |
| F7 | Sync `PHASE1_REPORT_V2.md` §4.2 gaps → closed | Cursor | 20 min | Doc truth |
| F8 | Sync `DEVELOPMENT_PROTOCOL.md` SMK 8 tests / Sprint 1 closed | Cursor | 10 min | Doc truth |
| F9 | Commit file audit FINAL + push cùng PR hoặc follow-up | Cursor | 5 min | Audit trail |
| F10 | Tick checklist 38/38 **sau merge** (human, HTML artifact) | Human | 10 min | Formal DoD |

### ⚠️ Có thể nhưng không nên / không cần

| # | Hành động | Lý do |
|---|-----------|-------|
| W1 | Tách lại 7 branch/7 PR retroactive | Code đã tích hợp; cost >> benefit |
| W2 | Revert PR #46 (agent4) | Gây churn; merge MB-S1 fix ordering |
| W3 | Gọi Sprint 1 DONE trước merge | Vi phạm cả 2 artifacts |
| W4 | Amend Step 7 report trên branch rồi force-push | Không cần nếu update post-merge |

### ❌ Không thể / ngoài scope Sprint 1

| # | Hành động | Lý do |
|---|-----------|-------|
| X1 | **7 PR riêng đã merge** (replay history) | Đã qua — monolithic branch |
| X2 | **Branch protection** bắt buộc CI | Org free tier (GAP-BP-1) |
| X3 | **JWKS / RS256** production JWT | Milestone C — HS256 stub đủ S6 |
| X4 | **Redis QuotaStore** (#29–31) | Sprint 2 non-goal |
| X5 | **cli/approve, cli/quota, cli/logs** live | Sprint 2 (#30–32) |
| X6 | **MCP cyanheads E2E** in CI | Milestone C non-goal |
| X7 | **Public repo / PyPI** | Public Beta gates chưa đạt |
| X8 | **100% checklist** mà không merge MB-S1 | Mâu thuẫn — 26 items phụ thuộc master |
| X9 | **Sửa `mcp/` 53% → 80%** trong Sprint 1 | Không trong 38-item DoD |

---

## 8. Khuyến nghị cụ thể (Path B)

**Thứ tự thực hiện:**

1. **F6** — thêm shipped PII test (optional nhưng mạnh cho #45)
2. **F1 + F9** — PR gồm: 8 commits + audit FINAL (+ test nếu F6)
3. **F2** — CI green
4. **F3** — merge
5. **F4, F5, F7, F8** — issue + doc sync (cùng ngày merge)
6. **F10** — tick 38/38 trong HTML checklist

**PR title gợi ý:**  
`feat(phase2): Milestone B Sprint 1 — MB-S1-1..5 guardrails, ABAC, coverage, CLI tests, identity JWT`

**Không làm:** Path C, W1, gọi DONE trước F3.

---

## 9. Sign-off

| Dimension | Branch | Sau Path B |
|-----------|--------|------------|
| Code quality | ✅ Pass | ✅ |
| 38-item DoD | ❌ 0% strict | ✅ ~95%+ (PRE N/A) |
| master truth | ❌ 32% | ✅ |
| GitHub issues | ❌ drift | ✅ if F4 |
| Sprint 2 ready | — | ✅ unblock |

---

**Prepared for:** Human decision — Path A / B / C  
**Last updated:** 2026-06-22  
**Next:** Chọn path → thực hiện F1–F10 theo §8
