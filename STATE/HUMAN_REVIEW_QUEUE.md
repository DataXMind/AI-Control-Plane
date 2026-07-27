# HUMAN REVIEW QUEUE — ACP

**Mục đích:** hiển thị đầu mỗi phiên/ngày các việc CHỜ HUMAN (quyết định, credential, hoặc duyệt merge). Agent tự cập nhật cột trạng thái khi làm được phần của mình; việc nào chỉ Human mới xử lý được thì giữ nguyên chờ.

**Cập nhật lần cuối:** 2026-07-26/27 (lượt 3, cùng phiên) bởi Claude (Sonnet 5, Claude Code) — Human approve trực tiếp → đã merge PR #206/#207/#208/#209 (mục A.1-5 giờ 🟢). Điều tra sâu + vá F-01 (mục 0) → PR #210 mở, chờ merge (mục A.14). Viết lại mục B bằng ngôn ngữ dễ hiểu theo yêu cầu Human + soạn sẵn diff Q-15 cụ thể (mục 6) để Human chỉ cần approve, chưa áp dụng. Mục C giữ nguyên, chỉ diễn giải lại. Lượt 2 cùng ngày: đóng gói branch/working-tree thành PR. Lượt 1: đóng A.4 (PR #201). Batch trước: 2026-07-19 (Fable 5 finder + Opus 4.8 cross-review).
**Quy ước:** 🔴 chỉ Human · 🟡 agent đã làm, chờ Human duyệt/merge · 🟢 đã đóng

---

## 🚨 0. REVIEW PASS 2026-07-19 (Prompt-1 finder + Prompt-2 executor, HEAD `cad0f70`)

Pipeline review toàn repo. Handoff Package validate PASS theo `HANDOFF-CONTRACT.schema.json` v2.0 (lưu tại `STATE/review-2026-07-19-handoff.json`). 3 finding — 2 CRITICAL (Tier C, KHÔNG tự vá), 1 Tier A (đã vá trên branch).

| # | Finding | Mức | Bằng chứng (repro thật) | Trạng thái |
|---|---|---|---|---|
| F-01 | 🟡 **ABAC `Deny-prod-k8s` KHÔNG chặn `k8s.apply` prod chưa duyệt** → rơi xuống `default_allow=True`. Root cause CONFIRMED sau điều tra sâu hơn (2026-07-26): wildcard `k8s_apply_*` sinh bởi loader là **có chủ đích** (khớp họ action `k8s_apply_dev/stage/prod` dùng thật ở nơi khác trong code, xem `core/policies.py` `_DEFAULT_WRITE_ACTIONS` + `tests/test_registry.py`) — lỗi thật nằm ở `ConditionEvaluator.evaluate()` so khớp key số nhiều `actions` bằng EXACT membership thay vì pattern-match (trong khi key số ít `action` và toàn bộ path RBAC đã dùng `_matches_any_pattern`/`_matches_any_action` đúng từ trước). | **P0 CRITICAL** | Repro qua shipped config thật (role infra, k8s_apply, prod+not_approved) → `allowed=True path=default_allow`, khớp chính xác báo cáo cũ | 🟡 **PR [#210](https://github.com/DataXMind/AI-Control-Plane/pull/210)** (2026-07-26) — vá `_matches_any_action()` cho key `actions`; KHÔNG đổi cách loader sinh wildcard (đã xác minh cách đó đúng ý đồ thiết kế, xoá nó sẽ thu hẹp phạm vi chặn dưới mức dự kiến). Có test hồi quy chứng minh red-trước-vá/green-sau-vá bằng `git stash`. Verify: ruff/mypy PASS, pytest 253 (was 252, +1), smoke 8/8, shipped_config_parity 6/6 (was 5, +1). Chờ Human merge (không tự merge — luật ACP). |
| F-02 | 🟢 **Role-trust escalation trên `/policy/evaluate`** | **P1 CRITICAL** | — | **Đã merge** 2026-07-26/27 — PR [#209](https://github.com/DataXMind/AI-Control-Plane/pull/209) (`b69f776`), Human-approved trực tiếp (queue từng ghi "chờ Opus review + Human merge" — Human tự duyệt, không chờ Opus review riêng — ghi nhận rõ để không ai hiểu nhầm bước Opus đã chạy) |
| F-03 | 🟢 Test `test_policy_evaluate_timeout_fail_closed` bỏ rơi coroutine `to_thread` → RuntimeWarning. | P3 test-only | — | **Đã merge** 2026-07-26/27 — PR [#208](https://github.com/DataXMind/AI-Control-Plane/pull/208) (`1b8e730`) |

**Cập nhật 2026-07-26 (lượt 3):** F-02 và F-03 đã merge. F-01 đã có fix hoàn chỉnh + test hồi quy, đang chờ merge ở PR #210 — đây là **hạng mục CRITICAL cuối cùng còn treo** trong toàn bộ mục 0. Sau khi #210 merge, `Deny-prod-k8s` sẽ chặn đúng cả 3 action như thiết kế ban đầu.

---

## A. Chờ Human DUYỆT MERGE (agent đã làm xong + test, KHÔNG tự merge — luật ACP)

| # | Việc | Branch / File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 1 | 🟢 Fix bảo mật A1/A3/A5/A6 (role-trust, audit-trail, loader warnings) | PR [#209](https://github.com/DataXMind/AI-Control-Plane/pull/209) | **Đã merge** 2026-07-26/27 (`b69f776`) | Human-approved trực tiếp |
| 2 | 🟢 A7 invariant test (Inv #1 no-OSS-engine, Inv #4 cli HTTP-only) | Cùng PR #209 | **Đã merge** | 21 case pass |
| 3 | 🟢 Sửa drift timeline (PUBLIC_BETA_SPRINT_PLAN) | PR [#206](https://github.com/DataXMind/AI-Control-Plane/pull/206) | **Đã merge** 2026-07-26/27 (`be6d306`) | — |
| 4 | 🟢 PR #201 (post-flip status ticks) | GitHub | **Đã merge** 2026-07-16 (squash `ab5a2a7`) | — |
| 5 | 🟢 CLAUDE.md §5 (+ §5.13) + LESSONS P-18..21 + bootstrap `STATE/*.md` vào git | PR [#207](https://github.com/DataXMind/AI-Control-Plane/pull/207) | **Đã merge** 2026-07-26/27 (`a2ccc13`) — Human approve process theo §5.9 | `STATE/ACP_MOAT_STRATEGY.md` vẫn bị loại khỏi git (`.gitignore`) |
| 14 | 🟡 Fix F-01 (xem mục 0) | PR [#210](https://github.com/DataXMind/AI-Control-Plane/pull/210) | Chờ Human merge | CRITICAL, PolicyEngine/ABAC/Invariant #1 — mục cuối cùng còn treo trong batch review 07-19 |

## B. Chờ Human QUYẾT ĐỊNH (thiết kế/sản phẩm — agent không tự quyết)

**Giải thích chung (thêm 2026-07-26 vì Human ghi "không hiểu rõ nội dung này"):** đây KHÔNG phải việc còn dang dở do thiếu code — đây là 6 câu hỏi mà chỉ Human mới trả lời được (đánh đổi sản phẩm, quyết định kiến trúc xuyên-repo, hoặc thẩm quyền vượt phạm vi 1 agent). Đã rà lại từng mục 2026-07-26, xác nhận vẫn đúng nguyên trạng, và với mục 6 đã chuẩn bị sẵn **diff cụ thể** để Human chỉ cần đọc và approve (không cần tự viết YAML).

| # | Việc | Giải thích ngắn (Human đọc hiểu ngay) | Đã chuẩn bị gì cho Human | Tại sao agent không tự quyết |
|---|---|---|---|---|
| 6 | Vá `config/policies.yml` Q-15 — thêm `session.create` vào quyền của role `backend` | AEOS gọi ACP xin phép tạo session, nhưng role `backend` chưa được cấp quyền `session.create` trong file luật → AEOS phải tắt tạm `ACP_ENABLED` để không bị chặn. Cần thêm đúng 1 dòng vào 2 file YAML. | **Diff cụ thể đã soạn sẵn — xem ngay bên dưới**, chưa áp dụng, chỉ chờ Human đọc + approve | `policies.yml` là CRITICAL tuyệt đối theo luật ACP — bắt buộc Human duyệt TRƯỚC khi agent chạm vào, không phải sau |
| 7 | A2: bật thật sự việc chặn (`requires_approval`) hay chỉ ghi log? | Hiện `requires_approval` có thể mới là "ghi nhận cần duyệt" chứ chưa thật sự CHẶN hành động cho tới khi duyệt — nếu bật chặn thật, AEOS/SACP đang tích hợp sẵn có thể bị lỗi vì họ đang giả định hành vi cũ | Không có gì để chuẩn bị trước — cần Human trả lời có/không trước, sau đó agent mới biết code gì | Đổi hành vi API đang chạy thật (breaking change) — quyết định sản phẩm |
| 8 | Thứ tự kiểm tra quota ACP vs ngân sách SACP, cái nào check trước | Khi 1 request vừa tốn quota ACP vừa tốn ngân sách SACP, cần biết kiểm cái nào trước để tránh trường hợp 1 bên cho phép, bên kia từ chối, gây lẫn lộn | Không thể tự chuẩn bị — cần thiết kế phối hợp với repo SACP, ngoài phạm vi ACP một mình | Xuyên 2 repo, ngoài thẩm quyền của agent lẫn Opus (đã ghi trong Opus Review Gate 07-08) |
| 9 | SACP có nên gọi ACP để kiểm tra mỗi tin nhắn chat hay không (thay vì tự kiểm tra bằng luật riêng)? | Đánh đổi: gọi ACP mỗi lần = chậm hơn nhưng nhất quán luật; giữ luật riêng = nhanh hơn nhưng có thể lệch luật ACP | Không thể tự chuẩn bị — đây là lựa chọn tốc độ-vs-nhất-quán, phải do người có quyền sản phẩm chọn | Đánh đổi hiệu năng/tuân thủ — quyết định Product |
| 10 | Đăng ký `aeos` như một "dự án" riêng trong ACP (thay vì mượn tạm dự án `rust-gateway`) | AEOS hiện đang "mượn" nhận diện của dự án khác để gọi ACP — hoạt động được nhưng không đúng tên. Cần biết đường dẫn/nhánh/môi trường thật của repo `aeos` để đăng ký đúng | **Không tự soạn được** — đã xem `config/projects.yml` thật, cần thông tin cụ thể từ repo `aeos` (đường dẫn code, tên nhánh) mà agent chưa được giao nhiệm vụ đọc trong phiên này; bịa số liệu ở đây rủi ro hơn là để trống | Cần thông tin cụ thể từ repo khác + quyết định thiết kế, không phải làm theo mẫu có sẵn |
| 11 | AEOS nên là "trạm điều phối" đơn giản hay tự vận hành cả tổ chức 50 agent? | Câu hỏi định hướng chiến lược dài hạn cho dự án `aeos`, không phải lỗi/tính năng cụ thể | Không thể chuẩn bị — cần tầm nhìn sản phẩm | Định hướng chiến lược, chạm văn kiện kiến trúc (ADR) |

### Đề xuất Q-15 — diff cụ thể, chỉ chờ approve (không tự áp dụng)

```diff
--- a/config/policies.yml
+++ b/config/policies.yml
@@ rbac.roles.backend.allowed_actions
         - cargo.clippy
         - admin.budget.freeze
+        - session.create
```
Áp dụng **giống hệt** cho `customer-bundle/production-config/policies.yml` (cùng cấu trúc, dòng tương ứng). Sau khi Human approve, verify bắt buộc trước merge: `pytest tests/test_shipped_config_parity.py -m shipped_config`, rồi chạy `scripts/sync_customer_bundle.sh` + `scripts/sync_vps_acp_admin_freeze.sh` trên VPS + AEOS re-smoke + bật lại `ACP_ENABLED`. Phần đăng ký project/agent riêng cho `aeos` (mục 10) **tách riêng**, không đi chung — vì đó cần thông tin thêm, còn phần `session.create` này tự đủ để verify.

## C. Chờ Human HÀNH ĐỘNG VẬN HÀNH (credential / thao tác thật — Tier B)

| # | Việc | Giải thích ngắn | Tại sao |
|---|---|---|---|
| 12 | Bắt đầu đếm ngày cho giai đoạn "soak" 30 ngày trước khi lên bản Production chính thức (PB-10) | Đây là một mốc thời gian vận hành thật (theo dõi hệ thống chạy ổn định 30 ngày liên tục), không phải việc sửa code — phải do Human bấm "bắt đầu" | issue #78 — thao tác vận hành, không có lệnh nào agent chạy để "bắt đầu đếm ngày" thay Human |
| 13 | Đổi token NGROK (một loại chứng chỉ kết nối mạng) trên VPS | Đây là thông tin đăng nhập thật trên máy chủ thật — agent không có và không nên có quyền truy cập | Credential thật trên VPS — ngoài quyền hạn agent theo thiết kế |

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
