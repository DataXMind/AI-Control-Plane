# PROGRESS — ACP (ai-control-plane)
Cập nhật lần cuối: 2026-07-19 (Batch REVIEW-01 — Prompt-1/2 pipeline) bởi Claude **Fable 5** (finder+verify) + **Opus 4.8** (cross-review §5.7), Claude Code / VS Code extension

---

# 🔒 WINDOW-CLOSE — 2026-07-20 (Claude, Sonnet 5) — ĐỌC PHẦN NÀY TRƯỚC

**Mục đích của phần này:** đóng lại cửa sổ hội thoại rất dài vừa qua (nhiều batch, nhiều model, trải 2026-07-07→2026-07-20) và làm SSOT cho bất kỳ session/agent nào mở repo này tiếp theo — để tránh làm lại việc đã xong, tránh drift, tránh xung đột nhánh.

**Trước khi tin bất kỳ dòng nào dưới đây là "hiện tại":** đã chạy `git fetch origin` và đối chiếu trực tiếp — không suy từ trí nhớ hội thoại. Đây chính là kỷ luật P-19/P-20 (đã ghi trong `LESSONS_LEARNED.md`) áp dụng cho chính lượt đóng cửa sổ này.

## Vì sao KHÔNG tạo file `HANDOFF.md` mới

Repo này **đã từng có đúng loại file bạn có thể nghĩ tới**: `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` ở root. Nó đã bị lỗi thời và một phiên khác đã **archive nó sang `docs/governance/ACP_HANDOFF_FOR_NEW_CONVERSATION_2026-06-27.md`** (PR #202, merged origin/master 2026-07-16) kèm cảnh báo:

> "This document is STALE for ops state... Do NOT use for: gate status, timeline, test counts, SHA, or open questions."

Tạo lại một file "HANDOFF.md" mới ở root sẽ lặp lại đúng lỗi đó (P-18: SSOT thứ hai cạnh tranh). Thay vào đó, tôi dùng đúng cơ chế repo đã có sẵn và đang tích cực bảo trì:
- **`docs/prompts/ANCHOR_CURRENT.md`** — living one-liner anchor, "update after major merge" — đã cập nhật ngay trước phần này.
- **`STATE/PROGRESS.md`** (file này) — nhật ký batch chi tiết, append-only.
- **`STATE/DECISIONS.md`** — câu hỏi mở / đã phân xử.
- **`STATE/HUMAN_REVIEW_QUEUE.md`** — việc chờ Human, cập nhật rất mới (2026-07-19).

## Checkpoint/Anchor xác minh trực tiếp (không phải trí nhớ)

| # | Sự kiện | Bằng chứng xác minh 2026-07-20 |
|---|---|---|
| 1 | `origin/master` = `9607dbc` (2026-07-16) — **local `master` từng lệch 10 ngày / 6 commit**, đã fast-forward xong lượt này | `git fetch origin` + `git log master..origin/master` |
| 2 | 6 commit mới trên master mà hội thoại trước KHÔNG biết: #201 (post-flip ticks, PR của chính tôi — **đã merge**), #202 (archive handoff doc), #203 (strip dated content khỏi SESSION_ANCHOR_TEMPLATE.md), #204 (AGENT_OPERATING_SYSTEM.md trỏ ANCHOR_CURRENT.md thay vì SHA cứng), #205 (fix verify_governance_status_runtime.sh cho v1.6.0), a5d5776 (đã biết) | `git log master..origin/master --oneline` |
| 3 | **F-01 — CRITICAL MỚI, tôi tự verify lại bằng cách đọc code (không chỉ tin báo cáo):** `ConditionEvaluator.evaluate()` so khớp key `actions` (số nhiều) bằng **exact membership** (`context.get("action") not in expected`), nhưng loader (`_map_abac_entry`) khi có >1 action lại ghi `"k8s_apply_*"` (wildcard) vào đúng key số nhiều đó. Kết quả: `k8s.apply` không bao giờ khớp `"k8s_apply_*"` bằng so sánh `in` → **rule `Deny-prod-k8s` KHÔNG chặn được `k8s.apply` ở prod chưa duyệt**, rơi xuống `default_allow`. `helm.upgrade`/`k8s.delete` (không có wildcard) vẫn bị chặn đúng — bất đối xứng chính là dấu hiệu. **CHƯA VÁ trên bất kỳ branch nào.** | Tự đọc lại `core/policies.py` (đã đọc đầy đủ file này ở batch 07-09) + đối chiếu `config/loader.py::_map_abac_entry` — khớp chính xác claim của batch REVIEW-01 |
| 4 | **F-02 = A1 (đã biết từ 07-09):** fix đã viết + test + verify gate xanh trên branch `critical/policy-trust-hardening` (`9c56efa` + `12d7a97`) nhưng **CHƯA MERGE** → vẫn LIVE trên master | `git log master..critical/policy-trust-hardening --oneline` |
| 5 | **F-01 + F-02 hợp lại = bypass hoàn toàn cổng phê duyệt k8s prod** — kiểm soát giá trị cao nhất của ACP | Batch REVIEW-01 (2026-07-19) + xác nhận lại hôm nay |
| 6 | F-03 (RuntimeWarning coroutine test) đã vá trên branch `fix/f03-timeout-test-coroutine-warning` @ `b16052c` — Tier A, không CRITICAL | `STATE/PROGRESS.md` Batch REVIEW-01 |
| 7 | Q-15 (VPS policy regression, `session.create` thiếu cho backend) — **vẫn CHƯA vá**, proposal vẫn chờ Human approve, không đổi từ 07-09 | Không có commit nào chạm `config/policies.yml` trên bất kỳ branch nào kể từ đó |
| 8 | AEOS: đính chính P-21 (07-09) vẫn đúng — AEOS đang vận hành thật, chỉ thiếu project/agent riêng, `ACP_ENABLED=false` là tạm thời | Không có thay đổi mới từ phía AEOS trong cửa sổ này |

## Bản đồ nhánh — TẤT CẢ chưa merge (kiểm tra lại trước khi mở nhánh mới)

| Nhánh | HEAD | Ngày | Nội dung | Trạng thái |
|---|---|---|---|---|
| `critical/policy-trust-hardening` | `12d7a97` | 07-09 | Fix A1/A3/A5/A6 + A7 invariant test (của tôi, batch trước) | 🟡 Chờ Human merge — vá F-02 |
| `fix/f03-timeout-test-coroutine-warning` | `b16052c` | 07-19 | Fix F-03 (test warning) — **branch đang checkout hiện tại** | 🟡 Chờ Human merge |
| `docs/post-flip-status-0707` | `cad0f70` | 07-07 | Base cho working-tree edits của tôi (CLAUDE.md §5, LESSONS P-18..21, PUBLIC_BETA_SPRINT_PLAN fix) — **các edit này hiện đang uncommitted, base branch đã lỗi thời** (không chứa #201-#205) | 🟡 Cần rebase/reapply trước khi commit — xem "Việc cần làm ngay" bên dưới |
| Không có branch nào vá F-01 | — | — | — | 🔴 Chưa ai chạm — cần Human approve trước (CRITICAL/ABAC/invariant) |

## ⚠️ Vấn đề cụ thể cần Human xử lý ngay khi mở lại cửa sổ mới

1. **Working tree hiện có edit uncommitted** (CLAUDE.md, LESSONS_LEARNED.md, PUBLIC_BETA_SPRINT_PLAN.md, .gitignore) được tạo trên nền `docs/post-flip-status-0707` (`cad0f70`) — nền này **đã lỗi thời 10 ngày**. **Đã verify (2026-07-20):** `PUBLIC_BETA_SPRINT_PLAN.md` KHÔNG bị commit nào trên `origin/master` chạm tới kể từ `fe832a9` (06-28, chính là baseline lỗi thời tôi đã sửa) — PR #201 chỉ sửa `PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` (file khác) — nên fix của tôi **không trùng, không xung đột, vẫn còn giá trị nguyên vẹn**. Việc còn lại thuần tuý: `git stash`, checkout nhánh mới từ `origin/master` hiện tại, `git stash pop`, rồi commit.
2. **F-01 cần một branch riêng, KHÔNG gộp chung với F-02** (luật F4 — không trộn risk level/loại lỗi trong 1 PR) — dù cùng CRITICAL, root cause khác nhau (ABAC condition-matching vs role-trust).
   *(Đã verify thêm: `CLAUDE.md` cũng an toàn tương tự — lần cuối bị chạm trên `origin/master` là `4ca8d8f` (06-25), TRƯỚC baseline edit của tôi (07-09) rất lâu; 6 commit mới `master..origin/master` không có commit nào chạm `CLAUDE.md`. Không cần diff, chỉ cần rebase branch.)*
3. Toàn bộ 13 mục trong `STATE/HUMAN_REVIEW_QUEUE.md` vẫn treo — không mục nào tự đóng trong cửa sổ này.

## Giá trị ĐÃ LỖI THỜI — đừng dùng lại

- ❌ "risk LOW" (anchor cũ 07-06) — nay là **CRITICAL** (2 finding chưa vá).
- ❌ "master @ a7769fb" hay bất kỳ SHA nào trước `9607dbc` — local từng lệch, đã sync.
- ❌ PR #201 "chờ Human skim + merge" (câu tôi viết ở batch 07-09) — **đã merge từ lâu** (`ab5a2a7`, một phần của `9607dbc`); `HUMAN_REVIEW_QUEUE.md` mục A.4 cần được đóng bởi phiên kế (tôi không sửa file đó vì thuộc quyền cập nhật của batch REVIEW-01 vừa rồi, để tránh 2 phiên ghi đè nhau).
- ❌ "ACP_HANDOFF_FOR_NEW_CONVERSATION.md ở root" — đã archive, không còn tồn tại trên master (chỉ còn trên các nhánh cũ chưa rebase).

---

## 🔒 WINDOW-CLOSE — 2026-07-26 (Claude, Sonnet 5) — độc lập re-verify phần trên, không ghi đè

**Không sửa nội dung của phần "🔒 WINDOW-CLOSE — 2026-07-20" phía trên** — chỉ bổ sung xác nhận độc lập, đúng nguyên tắc "2 nguồn khớp nhau thì ghi cả 2, không chọn 1 bên" khi chúng thực sự khớp.

**Re-verify vừa chạy lại (không suy từ hội thoại trước), tất cả khớp claim đã có ở trên:**

| Claim đã có ở batch 07-20 | Cách tôi re-verify lúc này | Kết quả |
|---|---|---|
| `CLAUDE.md` chưa bị `origin/master` chạm từ `4ca8d8f` (06-25) | `git log origin/master -1 -- CLAUDE.md` | Khớp — vẫn `4ca8d8f` |
| `PUBLIC_BETA_SPRINT_PLAN.md` chưa bị chạm từ `fe832a9` (06-28); PR #201 chỉ sửa `PUBLIC_BETA_OPERATOR_ACTION_PLAN.md` (file khác) | `git log origin/master -1 -- <file>` + `git show --stat ab5a2a7` | Khớp — không xung đột |
| F-01 root cause (wildcard `k8s_apply_*` vào key số nhiều `actions`, so khớp exact-membership) | Đọc trực tiếp `config/loader.py:182-193` (đặc biệt dòng 189: `normalized.append("k8s_apply_*" if action_norm == "k8s_apply" else action_norm)`) + `core/policies.py:163-166` (`elif key == "actions": if context.get("action") not in expected: return False`) | **Khớp chính xác** — tự suy luận lại từ 2 đoạn code này ra đúng cùng kết luận bất đối xứng (helm.upgrade/k8s.delete không bị wildcard hoá nên vẫn match đúng; k8s.apply bị đổi thành `k8s_apply_*` nên exact-match luôn thất bại) mà không đọc lại phần diễn giải ở trên trước |
| `critical/policy-trust-hardening` = 2 commit (`9c56efa`, `12d7a97`) trên nền `cad0f70`, chưa merge | `git log origin/master..critical/policy-trust-hardening --oneline` | Khớp |
| PR #201 "đã merge" | `gh pr view 201 --json state,mergedAt,mergeCommit` | Khớp — `MERGED`, `ab5a2a7`, 1 parent (squash), tác giả `mobilexmind` |

**Việc đã đóng thêm trong lượt này (ngoài phạm vi batch 07-20, không trùng):**
- `STATE/HUMAN_REVIEW_QUEUE.md` mục A.4 (PR #201) → chuyển 🟡→🟢 kèm bằng chứng (xem file, không lặp lại ở đây).
- `STATE/HUMAN_REVIEW_QUEUE.md` mục D → thêm 1 dòng cho PR #202-205 (đã merge 2026-07-16, trước cả batch REVIEW-01 07-19 — không liên quan finding F-01/F-02/F-03).
- Không đụng mục 0/A.1/A.2/A.3/A.5/B/C của `HUMAN_REVIEW_QUEUE.md` — đúng nguyên tắc "mỗi batch chỉ sửa phần mình có bằng chứng trực tiếp", tránh 2 phiên ghi đè nhau như batch 07-20 đã tự đặt ra.

**Vẫn treo, xác nhận lại KHÔNG có gì đổi từ batch 07-20:**
- Working tree uncommitted (`CLAUDE.md`, `LESSONS_LEARNED.md`, `PUBLIC_BETA_SPRINT_PLAN.md`, `.gitignore`, `ANCHOR_CURRENT.md`) vẫn trên nền `docs/post-flip-status-0707` (`cad0f70`) đã lỗi thời — **chưa thực hiện** thao tác stash/rebase/commit được đề xuất ở batch 07-20 mục "Việc cần làm ngay" #1; vẫn chờ quyết định rõ ràng trước khi ai đó chạy (không phải việc kỹ thuật thuần, có thể ảnh hưởng nhánh khác).
- F-01: vẫn CHƯA có branch nào vá — cần Human approve hướng vá trước (2 lựa chọn đã nêu ở `STATE/DECISIONS.md` câu hỏi mở #6, không lặp lại ở đây).
- Toàn bộ 13 mục `HUMAN_REVIEW_QUEUE.md` gốc vẫn treo, trừ mục A.4 vừa đóng ở trên.

### Lượt 2 (cùng phiên, 2026-07-26) — đóng gói mọi thứ "chờ Human" thành PR thật

Sau khi viết phần trên, phát hiện thêm: `critical/policy-trust-hardening` và `fix/f03-timeout-test-coroutine-warning` tồn tại **chỉ trên máy local, chưa từng push lên origin** — nghĩa là không Human hay agent nào ở máy/session khác có thể thấy hay review được, dù `HUMAN_REVIEW_QUEUE.md` đã ghi "chờ Human merge" cho cả hai. Cùng lúc, working-tree edit (`PUBLIC_BETA_SPRINT_PLAN.md`, và cả batch `CLAUDE.md`/`LESSONS_LEARNED.md`/`ANCHOR_CURRENT.md`/`STATE/*.md`) chỉ tồn tại uncommitted trên đúng 1 checkout — cùng một rủi ro "vô hình với session khác".

**Đã đóng gói thành 4 PR thật** (mỗi PR: rebase sạch lên `origin/master` hiện tại nếu cần, verify gate chạy lại thật — không chỉ trích dẫn kết quả cũ, `git diff --name-only` xác nhận đúng phạm vi file):

| PR | Nội dung | Nguồn gốc | Risk | Trạng thái mở |
|---|---|---|---|---|
| [#206](https://github.com/DataXMind/AI-Control-Plane/pull/206) | Sửa drift `PUBLIC_BETA_SPRINT_PLAN.md` | working tree cũ (`docs/post-flip-status-0707`) | LOW/docs-only | PR thường |
| [#207](https://github.com/DataXMind/AI-Control-Plane/pull/207) | `CLAUDE.md` §5 (+ §5.13 mới) + LESSONS P-18..21 + bootstrap `STATE/PROGRESS.md`/`DECISIONS.md`/`HUMAN_REVIEW_QUEUE.md` vào git lần đầu + `ANCHOR_CURRENT.md` resync | working tree cũ | LOW file-scope nhưng process-risk | **DRAFT — cố ý chưa sẵn sàng merge**, cần quyết định §5.13 trước (xem `STATE/DECISIONS.md` #7) |
| [#208](https://github.com/DataXMind/AI-Control-Plane/pull/208) | Fix F-03 (coroutine warning) | branch local `fix/f03-timeout-test-coroutine-warning` @ `b16052c`, chưa từng push | Tier A / LOW | PR thường |
| [#209](https://github.com/DataXMind/AI-Control-Plane/pull/209) | Fix A1/A3/A5/A6 (F-02) + A7 invariant test | branch local `critical/policy-trust-hardening`, chưa từng push | **CRITICAL** | PR thường nhưng ghi rõ "chờ Opus review + Human merge", KHÔNG vá F-01 |

**Cố ý loại trừ khỏi mọi commit:** `STATE/ACP_MOAT_STRATEGY.md` — file tự ghi "KHÔNG publish lên repo public"; đã thêm dòng loại trừ vào `.gitignore` (bảo vệ cho mọi session sau, không chỉ lượt này).

**Còn nguyên, cố ý không đụng:** working tree hiện tại (`fix/f03-timeout-test-coroutine-warning`) vẫn còn bản sao uncommitted của các file đã đóng gói ở trên (`CLAUDE.md`, `LESSONS_LEARNED.md`, `PUBLIC_BETA_SPRINT_PLAN.md`, `ANCHOR_CURRENT.md`, `.gitignore`, `STATE/*.md`) — **giờ là dữ liệu dư thừa an toàn** (đã có bản backup trong PR #206/#207), có thể `git checkout -- <file>` / để nguyên tuỳ Human, KHÔNG tự ý discard vì đó là thao tác phá dữ liệu chưa được xác nhận rõ ràng (git safety protocol).

**Việc mới phát sinh trong lượt này — xem `STATE/DECISIONS.md` câu hỏi mở mới** về việc có nên chính thức hoá quy trình "đóng cửa sổ phiên làm việc" (session close-out) thành một mục riêng trong `CLAUDE.md` §5 hay không — dựa trên so sánh giữa một prompt close-out tổng quát do Human cung cấp và cách batch 07-20 ở trên đã tự làm trên thực tế.

---

## Batch REVIEW-01 — 2026-07-19 (review + refactor toàn repo qua Prompt-1/2)

**Model-identity (CP-0):** finder pass + repro verify chạy dưới `claude-fable-5`; cross-review độc lập (§5.7, reviewer≠finder) tiếp tục dưới `claude-opus-4-8` (đổi model giữa phiên qua `/model opus`). Baseline freeze (CP-BL): `model_id=claude-fable-5`, `effort=high`, `rubric_version=acp-review-1.0`.

**Baseline verify gate (CP-3, HEAD `cad0f70`, output thật):** `ruff check src/ tests/` → All checks passed · `mypy src/ai_control_plane/ --strict` → no issues in 40 files · `pytest tests/` → 221 passed, 2 warnings.

**Handoff Package:** `STATE/review-2026-07-19-handoff.json` — validate PASS theo `HANDOFF-CONTRACT.schema.json` v2.0 (3 findings). Nguồn schema + Prompt 1/2 đã lọc bỏ nội dung repo khác (SACP/CWOS/AEOS) — chỉ áp phần khớp ACP (stack Python, verify gate ACP, invariants ACP).

**Findings (đã verify bằng repro thật, xem `STATE/HUMAN_REVIEW_QUEUE.md` §0):**
- **F-01 (P0 CRITICAL, MỚI):** ABAC `Deny-prod-k8s` không chặn `k8s.apply` prod chưa duyệt → `default_allow=True`. Root cause: mismatch wildcard(loader)/exact(`core/policies.py:163-166`) ở key số nhiều `actions`. Tier C — CHƯA vá, chờ Human.
- **F-02 (P1 CRITICAL, đã biết=A1):** role-trust escalation `/policy/evaluate` (`_resolve_role` tin `body.role`). Xác nhận vẫn live master. Fix ở branch `critical/policy-trust-hardening` chờ merge. Chained F-01+F-02 = bypass toàn bộ cổng phê duyệt prod k8s.
- **F-03 (P3, Tier A):** ĐÃ VÁ — branch `fix/f03-timeout-test-coroutine-warning` @ `b16052c`. Smoke: ruff/mypy/221 pass, warnings 2→1. Chờ Human merge (không tự merge — luật ACP).

**Variance:** F-01/F-02/F-03 = MATCH với forecast. Không phát sinh regression (221→221). F-01 là false-negative của bộ test hiện tại (blind spot: fixture 1-action che khuất path số nhiều của shipped config) — bài học cho LESSONS_LEARNED khi merge.

---


> **Khai báo danh tính & môi trường (bắt buộc theo Orchestration v2 Mục 0):** phiên hiện tại chạy **Fable 5** (`claude-fable-5`, xác nhận từ system prompt sau lệnh `/model claude-fable-5` ngày 2026-07-08) trên **VS Code extension** (không phải Cursor — chấp nhận theo ghi chú Mục 0 "có thể chạy VS Code nếu Cursor không sẵn"). **Đính chính lịch sử:** các mục ghi "Sonnet 5" ở batch 2026-07-07→08 trước đó (bootstrap STATE, Brief §5, SPEC-AEOS-S01/S02/S03) là **mislabel** — model thực tế đã là Fable 5 từ sau lệnh /model; nội dung công việc không đổi, chỉ sai nhãn người ký. Việc lấn sang repo AEOS ở 2 batch đó = **Human override trực tiếp** (lệnh "Thực hiện tiếp S01 > S03", 2026-07-08) — ghi theo luật Human override, KHÔNG theo ma trận Mục 2.

> **⚠️ VIỆC CHỜ REPO NÀY — ưu tiên cao nhất (từ Brief v0.11 Mục 9, Batch AEOS-03, 2026-07-08):**
> **INCIDENT Q-15 — VPS ACP policy regression.** Smoke từng PASS 2026-07-05 (`agent2/backend/rust-gateway` + `session.create`) nay **DENY** — reason `'session_create' not in allowed_actions for role 'backend'`. Giả thuyết chính: `scripts/sync_vps_acp_admin_freeze.sh` (PR #200 `a5d5776`) copy git `config/policies.yml` (không có session.create cho backend) đè bản sửa tay VPS. AEOS đã tắt `ACP_ENABLED` chờ vá. **3 yêu cầu cho repo ACP:**
> 1. Đưa `session.create` vào `backend.allowed_actions` **trong git** `config/policies.yml` (chấm dứt sửa tay VPS) — **CRITICAL theo L2** (PolicyEngine/policies) → cần Human approve trước + Opus review merge.
> 2. Đăng ký project `aeos` + agent riêng trong `config/agents.yml` + production-config (đóng O-02/Q-02 phía AEOS) — cùng lượt vá.
> 3. Xác nhận canonical tool name: `session_create` vs `session.create` (xem `core/tool_names.py` resolve_policy_tool_name).
> Sau vá: chạy `pytest tests/test_shipped_config_parity.py -m shipped_config` + sync VPS bằng đúng script + AEOS re-smoke.
>
> **✅ EVIDENCE XÁC MINH XONG @ 2026-07-08 (Batch ACP-02, Fable 5 — chỉ đọc, chưa sửa):**
> - Root cause **CONFIRMED**: `scripts/sync_vps_acp_admin_freeze.sh:8-9,22` copy git `config/policies.yml` → `/opt/acp/production-config/policies.yml`; git backend allowed_actions (`config/policies.yml:23-31`) = git.*/test.run/build.rust/cargo.clippy/admin.budget.freeze — **KHÔNG có session.create** → sync 2026-07-06 đè mất bản sửa tay VPS 2026-07-05.
> - Canonical tool name (trả lời ask #3): nội bộ engine = **`session_create`** (loader chuẩn hoá dot→snake lúc load — `config/loader.py:118,123`; engine so khớp bản chuẩn hoá — `core/policies.py:384-389`; client gửi `session.create` HAY `session_create` đều được — `core/tool_names.py`). Convention YAML repo = dot-notation → fix nên viết `- session.create`.
> - `customer-bundle/production-config/policies.yml:22-31` cũng thiếu session.create (nhất quán — cần vá cả 2 nơi + `bash scripts/sync_customer_bundle.sh`).
>
> **📋 PROPOSAL CHỜ HUMAN APPROVE (STOP-3 — không tự thực thi):**
> 1. Thêm `- session.create` vào `rbac.roles.backend.allowed_actions` ở **cả** `config/policies.yml` và `customer-bundle/production-config/policies.yml`.
> 2. Đăng ký project `aeos` (`projects.yml`) + agent riêng (đề xuất: `agent5`/aeos-bridge, role backend, projects [aeos]) ở cả shipped + production-config — sau đó AEOS đổi `ACP_PROJECT_ID=aeos`, `ACP_AGENT_ID=agent5`.
> 3. Verify: shipped_config parity test + full gate; merge qua Opus + Human (luật ACP); sau merge chạy sync script trên VPS + AEOS re-smoke + bật lại `ACP_ENABLED`.
>
> **🔄 CẬP NHẬT — 2026-07-08 (Self-Audit, sau khi khối trên được viết cùng ngày):** dòng "GATE-O1 blocker — SACP chưa push" bên dưới trong `STATE/DECISIONS.md` (Opus Review Gate Batch ACP-02) **ĐÃ SUPERSEDE bởi bằng chứng mới, không xoá bản cũ:** `git fetch` lại Hybrid-AI-Gateway cho thấy origin/main đã tiến tới `711c6b4` (SACP đã push `docs/contracts/SACP-AEOS-QUOTA-CONTRACT-v1.0-draft.md` + `STATE/`). SACP `STATE/PROGRESS.md` (Batch SACP-03, Opus) và AEOS `STATE/PROGRESS.md` (dòng D-17) đều xác nhận độc lập: **GATE-O1 verdict = PASS-CÓ-ĐIỀU-KIỆN**, contract r2 với 8 sửa đổi đã áp. Điều kiện còn treo: §5(c) của contract (quota ACP vs budget SACP) vẫn 🚩 chờ Human — **cần đối chiếu xem đây có TRÙNG với câu hỏi mở #4/#5 của chính `STATE/DECISIONS.md` repo này không** (chưa đối chiếu — để trống có chủ đích, xem Self-Audit). Q-15 (mục việc trên) KHÔNG bị ảnh hưởng bởi cập nhật này — vẫn STOP-3 chờ Human riêng.

## Đính chính về AEOS (Self-audit 2026-07-09 — sửa lỗi over-claim ngược)

Báo cáo deep-audit trước đó gán nhãn tích hợp AEOS là "CHƯA ĐĂNG KÝ / không qua ACP check nào" — **SAI** (P-21). Sự thật đúng, tách theo đúng scope (nguồn: `Material-Fable5\Layer2\OSAgent_audit_report.md` §2.2/§4.2, verify trực tiếp):

- ✅ **AEOS ĐANG vận hành** — control plane Phase 3, session pipeline `budget gate → ACP gate → create session → concurrency → file lock → audit` chạy thật; `POST /sessions` gọi `acp_client.evaluate("session.create", ...)` trước khi tạo session; smoke PASS HTTP 201 @ 2026-07-05.
- ✅ **Tích hợp ACP là by-design và fail-closed** khi ACP lỗi/unavailable (→ 403).
- 🔸 **Còn treo (đúng):** `aeos` chưa có project/agent RIÊNG trong `config/` của ACP — mượn `agent2/backend/rust-gateway` (O-02).
- 🔸 **Tạm thời (đúng):** `ACP_ENABLED=false` chỉ ở AEOS **dev** trong lúc chờ vá Q-15 — KHÔNG phải bản chất tích hợp.

Kết luận: "chưa đăng ký danh tính riêng" ≠ "chưa vận hành" ≠ "bypass ACP". Ba mệnh đề khác scope, không được gộp.

## Đã hoàn thành

| Hạng mục | Bằng chứng (commit/file/test) | Ngày |
|---|---|---|
| Milestones A/B/C/C+ CLOSED (PolicyEngine, HTTP bridge, MCP git facade, `agentctl` CLI, SAPAL MVP) | `README.md:9`; `CHANGELOG.md` `[0.1.0-rc.1]` entry | 2026-06-28 |
| PB-9 staging soak Day 14 **PASS**, issue [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77) closed | `docs/governance/PB9_STAGING_SOAK_LOG.md` Day 14 review row; `CHANGELOG.md [0.1.0-beta.1]` | 2026-07-06 |
| PB-12 public flip **GO** — repo flipped public, release `v0.1.0-beta.1` | `docs/prompts/ANCHOR_CURRENT.md`; `.release-notes-v0.1.0-beta.1.md`; commit `a7769fb` | 2026-07-06 |
| Governance catalog **v1.6.0**, `gates_remaining`: PB-10 only | `docs/prompts/ANCHOR_CURRENT.md` | 2026-07-06 |
| SACP (Hybrid-AI-Gateway) prod integration **B1+B2 CLOSED** — health + admin-freeze allow-path wired on VPS | `docs/governance/practice-evidence/sacp-acp-gap/README.md`; commit `a5d5776` (#200) | 2026-07-06 |
| AEOS × ACP **Phase 2 smoke PASS** — `POST /sessions` → `session.create` evaluate, HTTP 201 | `docs/governance/practice-evidence/aeos-acp-integration/RESULTS.md` §5 | 2026-07-05 |
| Hybrid AI Gateway × ACP **CONNECT CLOSED** | `docs/integrations/HYBRID_AI_GATEWAY.md`; PR #188 @ `aeca32a` | 2026-07-05/06 |
| Post-public-flip security hardening — redact infra IPs, repo hygiene | commit `1eae819` | 2026-07-06/07 |
| External architecture audit `ACP_Guardrails_report.md` **v3** exists — 8 invariants marked Shipped in code, decision types, Karpathy/ECC tier all documented with evidence labels | `D:\Projects\Material-Fable5\Layer5\ACP_Guardrails_report.md` (baseline `a5d5776`) | 2026-07-06 |
| 221 pytest / smoke 8/8 gate | `README.md` §Tests (cited, **not re-executed this session**) | — |

## Đang làm dở

| Hạng mục | Trạng thái hiện tại | Việc còn lại | Bằng chứng |
|---|---|---|---|
| PB-10 production soak (30 ngày) | Deferred to GA track; not started | Operator starts soak clock + daily log | `CHANGELOG.md`; issue [#78](https://github.com/DataXMind/AI-Control-Plane/issues/78); `ANCHOR_CURRENT.md` "OPEN: PB-10 GA clock" |
| SACP LLM hot-path (`/v1/chat/completions`) gating via ACP | **OPEN by design** — SACP dùng regex local **H-1+H-3** (đính chính danh pháp 2026-07-08 theo Batch SACP-01, verified `compliance.rs:5`; các tài liệu cũ gọi "H-2" là lệch tên — H-2 per-tenant bị defer Phase 3), không gọi ACP `/policy/evaluate` | Product decision — đã leo thang Mục 9 Brief, chờ Human | Brief v0.11 Mục 9 entry 2026-07-08; `sacp-acp-gap/README.md` |
| NGROK token rotation (SACP side) | Flagged, not yet rotated | Operator action on Hybrid-AI-Gateway/VPS side | `ANCHOR_CURRENT.md:16`; `MANUAL_OPERATOR_PLAYBOOK.md:431`; `HYBRID_AI_GATEWAY.md:188` |
| SAPAL / `apex/` packaging decision (separate repo vs module vs archive) | Experimental @ 0.x, undecided | Review targeted at v0.3.0 | `CHANGELOG.md [Unreleased]` Notes |
| `agentctl policy diff` dry-run | Design issue only | Implementation deferred post-PB-12 | `CHANGELOG.md`; issue #184 |
| Audit-trail for every `/policy/evaluate` call | Not implemented per external audit | Add telemetry emit on evaluate path | `ACP_Guardrails_report.md` §5 (not independently re-verified against current code this session) |
| Multi-tenant auth on `/policy/evaluate` | Missing per external audit | Design + implement | `ACP_Guardrails_report.md` §1.4 |

## Bàn giao batch 2026-07-07 (bootstrap + đóng meta-drift Brief)

**Đã xong trong batch (Sonnet 5):** bootstrap `STATE/`; triage toàn batch; Brief v0.8 — đóng §5 (danh mục rule + interface contract + audit-trail, từ report v3) và đóng mâu thuẫn P3 ablation Harness-1 (D-04 = −5.4%, audit trực tiếp v9.2.html).

**→ Chờ FABLE 5** (model switch không khả dụng trong môi trường này — chạy ở phiên/môi trường khác):
| Việc | Cần gì | Ghi chú |
|---|---|---|
| Giai đoạn A bước 1+3+5 (phần SACP/OS Agent) | Quyền truy cập repo Hybrid-AI-Gateway | Bước 5 phần ACP đã được report v3 cover (baseline `a5d5776`; master hiện tại `cad0f70` chỉ thêm docs-only) |
| Giai đoạn A bước 2: thiết kế interface contract SACP⇄AEOS v1.0 | Kiến trúc mới từ đầu (OS Agent 0%) | Không phải xác nhận version có sẵn — Brief §2c |
| Giai đoạn B: Rust Gateway re-smoke (P0), quota/credit engine | Contract từ bước 2 + repo SACP | KHÔNG bắt đầu trước khi contract khoá |
| Brief §7a: Luật AI/Data/IP vs luật VN 91/2025 + 134/2025 | Repo SACP (module vật lý nằm đó) | Fable-tier theo chính Brief |

**→ Chờ OPUS Review Gate:** batch doc-edit này (Brief v0.7→v0.8 + bootstrap `STATE/`) — theo `AGENT_ORCHESTRATION.md` Bước 4. Chưa có merge nào vào git ACP (STATE files đang untracked; muốn commit cần branch + PR theo P-09).

## Gap còn thiếu (chưa bắt đầu)

| Hạng mục | Mô tả gap | Mức độ ưu tiên | Ghi chú |
|---|---|---|---|
| SACP⇄AEOS quota/credit interface | 0% implementation phía OS Agent; không có version nào để khoá | Cao (Track B — Fable 5) | `Fable5_Kickoff_Brief_SACP_OS_Agent_v7_FINAL.md` §2c/§9 — ngoài phạm vi repo ACP, chỉ ghi để tham chiếu |
| K8s-native ACP deployment manifest | Không có trong repo này; SACP hiện gọi ACP qua host Docker IP | Chưa xác định | `ACP_Guardrails_report.md` §1.2 |
| ~~Kickoff Brief §5 chưa trỏ tới `ACP_Guardrails_report.md`~~ | **ĐÃ ĐÓNG 2026-07-07** — Brief v0.8 điền §5 từ report v3; xem `STATE/DECISIONS.md` §Gap | — | 2 câu hỏi mở mới sinh ra từ việc đóng: DECISIONS.md #4 (default_allow vs deny-by-default), #5 (audit-trail evaluate) |
