# HUMAN REVIEW QUEUE — ACP

**Mục đích:** hiển thị đầu mỗi phiên/ngày các việc CHỜ HUMAN (quyết định, credential, hoặc duyệt merge). Agent tự cập nhật cột trạng thái khi làm được phần của mình; việc nào chỉ Human mới xử lý được thì giữ nguyên chờ.

**Cập nhật lần cuối:** 2026-07-26 (lượt 2, cùng phiên) bởi Claude (Sonnet 5, Claude Code) — đóng gói TOÀN BỘ nội dung "chờ Human merge" đang nằm ở dạng branch-chưa-push hoặc working-tree-chưa-commit thành PR thật trên GitHub: mục A.1/A.2 → PR #209 (CRITICAL, rebase sạch), A.3 → PR #206 (đã đóng, không còn working tree), A.5 → PR #207 (draft, cố ý chưa sẵn sàng merge), F-03 (mục 0) → PR #208. Không đổi nội dung/quyết định của mục 0 (F-01/F-02 vẫn đúng nguyên trạng, chỉ thêm link PR cho F-03) hay mục B/C — không thuộc phạm vi lượt này. Lượt 1 cùng ngày: đóng A.4 (PR #201) + thêm dòng mục D (PR #202-205). Batch trước: 2026-07-19 (Fable 5 finder + Opus 4.8 cross-review) — Prompt-1/2 review+refactor pipeline.
**Quy ước:** 🔴 chỉ Human · 🟡 agent đã làm, chờ Human duyệt/merge · 🟢 đã đóng

---

## 🚨 0. REVIEW PASS 2026-07-19 (Prompt-1 finder + Prompt-2 executor, HEAD `cad0f70`)

Pipeline review toàn repo. Handoff Package validate PASS theo `HANDOFF-CONTRACT.schema.json` v2.0 (lưu tại `STATE/review-2026-07-19-handoff.json`). 3 finding — 2 CRITICAL (Tier C, KHÔNG tự vá), 1 Tier A (đã vá trên branch).

| # | Finding | Mức | Bằng chứng (repro thật) | Trạng thái |
|---|---|---|---|---|
| F-01 | 🔴 **ABAC `Deny-prod-k8s` KHÔNG chặn `k8s.apply` prod chưa duyệt** → rơi xuống `default_allow=True`. Root cause: loader viết `k8s.apply`→`k8s_apply_*` (wildcard) vào key số nhiều `actions`, nhưng `ConditionEvaluator.evaluate` (`core/policies.py:163-166`) so khớp `actions` bằng EXACT membership. `helm.upgrade` bị chặn đúng (path=abac) → chứng minh bất đối xứng. Unit test xanh vì fixture dùng 1-action → map sang key số ít `action` (pattern-match đúng). | **P0 CRITICAL** | `repro_abac.py` qua loader thật + shipped config: infra+prod+not_approved+k8s.apply → `allowed=True path=default_allow` | 🔴 Chờ Human approve (CRITICAL/ABAC/invariant #1 — Tier C). CHƯA vá. |
| F-02 | 🔴 **Role-trust escalation trên `/policy/evaluate`**: `body.role` được tin nguyên văn (`api/server.py:_resolve_role` 246-257) → caller tự khai role bất kỳ. **Chained với F-01**: agent2 (backend, bị RBAC cấm k8s.apply) gửi `role='infra'` + `plan_submitted` + `environment=prod` → **unapproved prod k8s.apply = allowed=True**. Đây là A1/A3 đã biết. | **P1 CRITICAL** | `repro_roletrust.py` qua API thật (TestClient): combined exploit → `allowed=True path=default_allow` | 🔴 Đã có fix trên branch `critical/policy-trust-hardening` (#1 mục A) chờ merge. XÁC NHẬN vẫn LIVE trên master. |
| F-03 | 🟡 Test `test_policy_evaluate_timeout_fail_closed` bỏ rơi coroutine `to_thread` → RuntimeWarning. | P3 test-only | pytest warnings 2→1 sau vá | 🟡 **PR [#208](https://github.com/DataXMind/AI-Control-Plane/pull/208)** (branch cũ chỉ nằm local, chưa từng push — đã push + mở PR 2026-07-26, rebase sạch lên `origin/master` hiện tại). ruff/mypy/221 pass (re-run trên bản rebase, không chỉ trích dẫn). Chờ Human merge. |

**⚠️ F-01 + F-02 hợp lại = bypass HOÀN TOÀN cổng phê duyệt K8s production** — kiểm soát quan trọng nhất của ACP. F-01 là finding MỚI (chưa có trong queue trước), độc lập với branch trust-hardening; branch đó vá F-02 (role-trust) nhưng KHÔNG vá F-01 (ABAC wildcard) → cần fix riêng cho F-01 kể cả sau khi merge trust-hardening.

---

## A. Chờ Human DUYỆT MERGE (agent đã làm xong + test, KHÔNG tự merge — luật ACP)

| # | Việc | Branch / File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 1 | 🟡 Fix bảo mật A1/A3/A5/A6 (role-trust, audit-trail, loader warnings) | **PR [#209](https://github.com/DataXMind/AI-Control-Plane/pull/209)** (branch `critical/policy-trust-hardening` @ `9c56efa`, chưa từng push — đã push + mở PR 2026-07-26, rebase sạch) | Chờ Opus review + Human merge | CRITICAL — chạm auth endpoint quyết định. Verify re-run trên bản rebase: ruff/mypy PASS, pytest 252 pass/smoke 8/parity 5; exploit A1 verified closed. PR ghi rõ KHÔNG vá F-01 (khác root cause, xem mục 0) |
| 2 | 🟡 A7 invariant test (Inv #1 no-OSS-engine, Inv #4 cli HTTP-only) | Cùng PR **[#209](https://github.com/DataXMind/AI-Control-Plane/pull/209)** @ `12d7a97` | Chờ Human merge | 21 case pass (re-verify 2026-07-26) |
| 3 | 🟢 Sửa drift timeline (PUBLIC_BETA_SPRINT_PLAN: PB-9/PB-12 đang sai công khai) | **PR [#206](https://github.com/DataXMind/AI-Control-Plane/pull/206)** (đã đóng gói từ working tree `docs/post-flip-status-0707` cũ, mở 2026-07-26) | Chờ Human merge (đã đóng gói xong, không còn nằm working tree) | File public từng khẳng định PB-9 IN PROGRESS + PB-12 ❌ — đều sai, đã sửa; verify docs-only + smoke 8/8 pass |
| 4 | 🟢 PR #201 (post-flip status ticks) | GitHub, mở từ 07-07 | **Đã merge** 2026-07-16 (squash `ab5a2a7`, tác giả `mobilexmind`) | Đóng bởi phiên 2026-07-26 (Claude Sonnet 5): xác nhận qua `gh pr view 201` (`state: MERGED`) + `git log --oneline` trên `origin/master`; nội dung đã skim đầy đủ trước đó (5 file docs, số liệu 1.6.0/pytest 221/gates_remaining=1 khớp `ANCHOR_CURRENT.md`) |
| 5 | 🟡 CLAUDE.md §5 Autonomous protocol (+ mới §5.13 Session close-out) + LESSONS P-18..21 + bootstrap `STATE/*.md` vào git | **PR DRAFT [#207](https://github.com/DataXMind/AI-Control-Plane/pull/207)** (đã đóng gói từ working tree, mở draft 2026-07-26 — cố ý để DRAFT, không phải PR thường) | Chờ Human review + quyết định (không phải merge thường) | Thay đổi process → cần duyệt (CLAUDE.md §5.9); xem `STATE/DECISIONS.md` câu hỏi mở #7. `STATE/ACP_MOAT_STRATEGY.md` đã bị loại khỏi commit (thêm vào `.gitignore`) — file đó tự ghi rõ không được publish |

## B. Chờ Human QUYẾT ĐỊNH (thiết kế/sản phẩm — agent không tự quyết)

| # | Việc | Ở đâu | Tại sao cần Human |
|---|---|---|---|
| 6 | 🔴 Vá `config/policies.yml` Q-15 (thêm `session.create` cho backend) | ACP STATE §Q-15 | CRITICAL policies.yml — Human approve trước |
| 7 | 🔴 A2: có bật enforcement cho `requires_approval` không (breaking API contract AEOS/SACP đang phụ thuộc)? | Audit A2 | Breaking change hợp đồng live — quyết định sản phẩm |
| 8 | 🔴 §5(c) GATE-O1: quota ACP vs budget SACP — thứ tự check | SACP STATE D-17 | Chạm luật ACP, ngoài thẩm quyền Opus |
| 9 | 🔴 SACP LLM hot-path có bắt buộc qua ACP evaluate (Track B3) hay giữ H-1+H-3? | Brief Mục 9 | Quyết định Product, đánh đổi tốc độ/compliance |
| 10 | 🔴 Thiết kế project `aeos` riêng trong ACP config (roles/paths/env) | Chưa có file | Quyết định thiết kế, không phải copy-paste |
| 11 | 🔴 Q-10 AEOS: traffic-controller vs 50-agent org tự vận hành | AEOS STATE Q-10 | Định hướng chiến lược, chạm ADR charter |

## C. Chờ Human HÀNH ĐỘNG VẬN HÀNH (credential / thao tác thật — Tier B)

| # | Việc | Ở đâu | Tại sao |
|---|---|---|---|
| 12 | 🔴 Bắt đầu clock PB-10 (30d production soak) | issue #78 | Thao tác vận hành, không có code để agent chạy |
| 13 | 🔴 Rotate NGROK token | ANCHOR_CURRENT / playbook | Credential thật trên VPS — agent không có quyền |

## D. Đã đóng gần đây (agent tự làm được — không cần Human)

| # | Việc | Trạng thái |
|---|---|---|
| — | 🟢 Redact artifact khỏi claude.ai | Done 2026-07-09 |
| — | 🟢 Đính chính lỗi kết luận AEOS (P-21) | Done 2026-07-09 |
| — | 🟢 Xác minh + tái tạo exploit A1, rồi verify đóng | Done 2026-07-09 |
| — | 🟢 Đọc bù `ACP_Guardrails_report.md` §1 (P-20) | Done 2026-07-09 |
| — | 🟢 4 PR docs cleanup (session-handoff SSOT consolidation): archive `ACP_HANDOFF_FOR_NEW_CONVERSATION.md` → `docs/governance/` (#202), gỡ dữ liệu trôi khỏi `SESSION_ANCHOR_TEMPLATE.md` (#203), trỏ `AGENT_OPERATING_SYSTEM.md` baseline sang `ANCHOR_CURRENT.md` thay vì SHA cứng (#204), sửa 3 assertion sai trong `verify_governance_status_runtime.sh` cho catalog v1.6.0 post-PB-12-flip (#205) | Done 2026-07-16 — merged; mỗi PR verify: docs-only diff (`git diff --name-only origin/master` không có `src/`) + `bash scripts/verify_governance_memory.sh` PASS + smoke 8/8 PASS (WSL venv); #205 verify thêm bằng chạy API thật + curl `/governance/status` |

---

*Agent tự cập nhật file này cuối mỗi batch. Human chỉ cần đọc cột 🔴 để biết việc gì đang chờ mình.*
