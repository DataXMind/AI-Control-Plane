# DECISIONS — ACP (ai-control-plane)
Cập nhật lần cuối: 2026-07-26 bởi Claude (Sonnet 5, Claude Code) — phân xử #7 (giữ CLAUDE.md §5.13, Human approve qua merge PR #207) và #6 (F-01 fix direction = pattern-match, không đổi loader; PR #210 chờ merge) — không xoá 2 dòng câu hỏi mở gốc, chỉ đánh dấu supersede. Trước đó: 2026-07-07 bởi Claude (Sonnet 5, Claude Code)

## Câu hỏi mở (chưa phân xử)

| # | Câu hỏi | Phạm vi ảnh hưởng | Người/Agent nêu | Ngày |
|---|---|---|---|---|
| 1 | SACP `/v1/chat/completions` có nên đi qua ACP `/policy/evaluate` thay vì H-2 local regex không? | **XUYÊN-REPO** (ACP ⇄ SACP) — đã ghi ở `Fable5_Kickoff_Brief` §2a (P1, "đợi quyết định Product") | Operator / audit (Hybrid-AI-Gateway) | 2026-07-06 |
| 2 | SACP⇄AEOS quota/credit interface: thiết kế cụ thể ra sao (endpoint, ledger semantics, version)? | **XUYÊN-REPO** (SACP ⇄ AEOS) — đã ghi ở `Fable5_Kickoff_Brief` §2c/§9 (phía OS Agent 0% implementation, thiết kế mới từ v1.0) | Claude Sonnet 5 (audit hợp nhất trong Brief) | 2026-07-06 |
| 3 | PB-10 GA soak — thời điểm chính thức bắt đầu clock 30 ngày? | Nội bộ ACP | — | — |
| 4 | PolicyEngine fallthrough cuối là `default_allow` — có chuyển sang chế độ "deny mọi tool chưa khai báo" (deny-by-default tuyệt đối) không? Brief Mục 5 tuyên bố "deny-by-default" là nguyên tắc, nhưng code thật chỉ fail-closed khi service lỗi + deny khi rule khớp | **XUYÊN-REPO — luật ACP áp cho cả 3 repo** — đã ghi vào Brief §5 (master) @ v0.8; nguồn: `ACP_Guardrails_report.md` v3 §2.5B + §8 next-step #5 | Audit report v3 / Claude Sonnet 5 (escalate khi đóng Brief §5) | 2026-07-07 |
| 5 | Audit-trail cho `POST /policy/evaluate`: khi implement (report v3 next-step CRITICAL #1), schema event và retention policy chọn thế nào? | Nội bộ ACP (implementation), nhưng ảnh hưởng niềm tin audit của SACP/AEOS — cân nhắc escalate khi thiết kế | Audit report v3 | 2026-07-07 |
| 7 | **[SUPERSEDE 2026-07-26 → xem "Đã phân xử" #5]** Human cung cấp 1 prompt tổng quát "session close-out" (verify thật trước khi ghi done, phân loại đúng file, không xoá/ghi đè, xử lý conflict bằng cách ghi cả 2 nguồn). So sánh với batch 07-20 (`STATE/PROGRESS.md` "🔒 WINDOW-CLOSE"), thấy đây gần như đúng cùng kỷ luật đã tự phát sinh trong thực tế — nên **chính thức hoá** thành `CLAUDE.md` §5.13 (mới) hay để mỗi phiên tự áp dụng theo tinh thần §5.2/§5.10/§5.12 hiện có, không thêm mục mới? Đã soạn sẵn bản nháp §5.13 trong `CLAUDE.md` (uncommitted, cùng batch với §5 đang chờ duyệt mục A.5) — cần Human xác nhận giữ hay bỏ trước khi cả batch CLAUDE.md §5 được duyệt | Nội bộ ACP — process, không phải code, nhưng CLAUDE.md là L0 nên mọi thay đổi cần duyệt theo §5.9 | Claude (Sonnet 5), so sánh trực tiếp 2 nguồn theo yêu cầu Human | 2026-07-26 |
| 6 | **[SUPERSEDE 2026-07-26 → xem "Đã phân xử" #6, PR #210]** **F-01 CRITICAL:** `ConditionEvaluator.evaluate()` so khớp key `actions` (số nhiều) bằng exact membership, nhưng loader ghi wildcard (`k8s_apply_*`) vào đúng key đó khi rule có >1 action → `Deny-prod-k8s` KHÔNG chặn được `k8s.apply` ở prod chưa duyệt (rơi xuống `default_allow`). Cách vá đúng: đổi `actions` sang so khớp pattern (như key `action` số ít đã làm), hay đổi loader không sinh wildcard vào key số nhiều? Cần Human/Fable quyết hướng vá vì chạm invariant #1 (PolicyEngine) — không tự sửa | Nội bộ ACP — nhưng CRITICAL vì đây là gap ở đúng cổng phê duyệt k8s prod, giá trị kiểm soát cao nhất của ACP | Batch REVIEW-01 (Fable 5 finder), xác nhận lại bằng đọc code 2026-07-20 | 2026-07-19 |

## Đã phân xử (quyết định cuối)

| # | Quyết định | Lý do | Phạm vi ảnh hưởng | Ngày chốt |
|---|---|---|---|---|
| 1 | Naming: **ACP** = AI-Control-Plane (agent tool/action policy, repo này) · **SACP** = Sovereign AI Control Plane (tên dùng ở repo Hybrid-AI-Gateway, LLM gateway) · **AEOS** = repo `aeos` (session orchestrator) — AEOS gọi **thẳng ACP** để xin quyết định tool-policy, KHÔNG đi qua SACP | Tránh conflation "ACP" ↔ "SACP"; verify thực tế cho thấy AEOS × ACP đã PASS trực tiếp (không qua SACP) | **XUYÊN-REPO** — đã ghi ở `docs/integrations/HYBRID_AI_GATEWAY.md` §0 + `aeos-acp-integration/RESULTS.md` §2 (repo này) và `Fable5_Kickoff_Brief` Mục 0 (ngoài repo, master) | 2026-07-05/06 |
| 2 | Phạm vi ACP Guardrails **MỞ LẠI**: bao gồm cross-tool/cross-máy (Antigravity, VS Code, Cursor), không chỉ governance cho SACP+OS Agent | Xác nhận trực tiếp từ stakeholder | **XUYÊN-REPO** — đã ghi ở `Fable5_Kickoff_Brief` Mục 8 (ngoài repo, master) | 2026-07-05 |
| 3 | 8 Hard Invariants + phân loại rủi ro LOW/MEDIUM/HIGH/CRITICAL là luật ACP áp dụng cho cả 3 repo | — | **XUYÊN-REPO** — `ARCHITECTURE.md` (repo này, nguồn gốc luật) | (từ đầu dự án) |
| 4 | PB-12 **GO** — flip repo public, phát hành `v0.1.0-beta.1`, PB-10 deferred sang GA track | PB-9 Day 14 PASS, `gates_remaining=1` | Nội bộ ACP | 2026-07-06 |
| 5 | **Câu hỏi #7 ĐÃ PHÂN XỬ:** giữ `CLAUDE.md` §5.13 (Session close-out checklist) — Human approve nguyên batch §5 qua merge PR #207 | Human approve trực tiếp, không yêu cầu sửa gì thêm | Nội bộ ACP — process (CLAUDE.md §5.9) | 2026-07-26 |
| 6 | **Câu hỏi #6 (F-01) ĐÃ PHÂN XỬ kỹ thuật, chờ Human merge PR:** chọn vá `ConditionEvaluator.evaluate()` để pattern-match key `actions` (số nhiều) qua `_matches_any_action()` — **KHÔNG** đổi loader bỏ wildcard. Lý do: điều tra trực tiếp code xác nhận wildcard `k8s_apply_*` khớp họ action `k8s_apply_dev/stage/prod` **có thật** ở nơi khác trong hệ thống (`core/policies.py` `_DEFAULT_WRITE_ACTIONS`, `tests/test_registry.py`) — bỏ wildcard sẽ thu hẹp phạm vi chặn dưới ý đồ gốc; pattern-match key `actions` chỉ là áp dụng đúng cách mà key `action` số ít + toàn bộ path RBAC đã làm từ trước, không phải lựa chọn tuỳ ý | Nội bộ ACP — CRITICAL, PolicyEngine/Invariant #1 | Claude Sonnet 5, điều tra sâu 2026-07-26; PR [#210](https://github.com/DataXMind/AI-Control-Plane/pull/210) — merge vẫn chờ Human (quyết định kỹ thuật đã xong, merge là hành động riêng) |

---

## Lưu ý escalation (quy tắc leo thang local ⇄ master)

Câu hỏi #1–2 và quyết định #1–2 ở trên **đã được ghi nhận** tại nguồn sự thật dùng chung ngoài repo này:
`D:\Projects\Material-Fable5\Instructions\Fable5_Kickoff_Brief_SACP_OS_Agent_v7_FINAL.md` (Mục 8 — Locked, Mục 9 — Open).

Theo `AGENT_ORCHESTRATION.md` §4: **không tạo thêm** một file `MASTER/DECISIONS.md` cạnh tranh bên trong repo ACP này — Kickoff Brief ngoài repo đã đóng vai trò master thật sự cho các quyết định xuyên-repo. File `STATE/DECISIONS.md` này chỉ trích dẫn lại để repo ACP có bản ghi local, không phải bản gốc.

## Gap phát hiện — ĐÃ ĐÓNG 2026-07-07

**Fable5_Kickoff_Brief §5** từng ghi `"(điền — chưa có audit report ACP đầy đủ)"` dù `Layer5\ACP_Guardrails_report.md` v3 (baseline `a5d5776`, audit 2026-07-06) đã tồn tại — meta-drift.

**Đã xử lý (Brief v0.7 → v0.8, 2026-07-07, sau khi người dùng ra lệnh "Continue"):** điền §5 danh mục rule + interface contract OS Agent + audit-trail từ report v3; cập nhật "Trạng thái tổng"; gạch 2 dòng "Ô còn trống thật"; thêm changelog row. Việc điền là trích xuất cơ học từ report có sẵn (Sonnet-eligible theo nguyên tắc mơ hồ/rủi ro của `AGENT_ORCHESTRATION.md` Mục 1) — không tự đặt luật mới. Hai phát hiện kèm theo đã escalate thành câu hỏi mở #4, #5 ở trên.

---

## Opus Review Gate — Batch ACP-02 (2026-07-08)

**Reviewer:** Opus 4.8 (Gatekeeper, Orchestration v2 Mục 6). **Batch:** ACP-02, repo ACP (`d:\Projects\ai-control-plane`), thực hiện bởi Fable 5, 2026-07-08.
**Artifacts review:** repo mới `D:\Projects\ACP-SACP-AEOS` commit `413ba11` + `68b719d`; nhánh `low/state-batch-acp02` commit `d48392c` (STATE local, không push); Q-15 evidence + proposal; baseline verify gate.

### VERDICT: ✅ **PASS**

Kết quả đối chiếu 5 điểm checklist Mục 6 (mọi khẳng định gắn bằng chứng đã tự xác minh trong code, không nhận trên lời):

**1. Definition of Done (Mục 11) cho phần việc tương ứng — ĐẠT.**
Batch ACP-02 không phải burst sinh code Giai đoạn B (Rust Gateway/quota engine); phần việc tương ứng của repo ACP là Giai đoạn A bước 5 (đối chiếu hiện trạng thật với quy trình — xác lập baseline verify gate) + xác minh evidence Q-15. Output đúng định dạng Giai đoạn A: mỗi phát hiện gắn mức độ tin cậy (verified-in-code vs suy luận). Baseline gate được ghi rõ kèm giải thích trung thực 1 fail (220/221 = path-translation Windows→WSL của test harness, script thật exit 0) — không giấu.

**2. Vi phạm luật ACP (deny-by-default / Allow/Deny / audit-trail) — KHÔNG.**
`config/policies.yml` và `customer-bundle/production-config/policies.yml` đều KHÔNG bị sửa — `session.create` vẫn vắng mặt ở cả 2 (đã grep xác nhận). Proposal vá được GIỮ CHỜ HUMAN (STOP-3), đúng luật "policies.yml luôn CRITICAL, luôn cần Human". Dòng `+admin.budget.freeze` khác biệt so với master là từ commit `2ee9e71` có trước (không phải batch này, không phải session.create). Không chạm engine Allow/Deny, không tạo regression audit-trail. Batch tôn trọng deny-by-default bằng chính việc TỪ CHỐI tự áp policy change.

**3. Giao thức SACP⇄AEOS — xử lý ĐÚNG giới hạn.**
Batch có chạm cross-repo (Q-15 ACP⇄AEOS; GATE-O1 dính SACP). SACP STATE/contract không truy cập được vì origin chưa push — batch KHÔNG bịa phía SACP, KHÔNG tự chọn "bản đúng"; đã ghi rõ ở Brief Mục 9 rằng `git fetch` Hybrid-AI-Gateway origin/main @ `c6ec8e4` (07-06) không chứa contract draft lẫn STATE/, và treo GATE-O1 như blocker #1. Đây đúng hành vi checklist yêu cầu ("lệch/thiếu → không tự chọn, ghi rõ"). Mô tả Q-15 phía ACP (session.create DENY, giả thuyết sync đè, canonical name) nhất quán với mô tả phía AEOS được tham chiếu. Cross-check cuối cùng của GATE-O1 vẫn treo chờ SACP push — không phải lỗi của batch này.

**4. Làm tắt / bỏ sót edge case — KHÔNG thấy dấu hiệu.**
Evidence Q-15 truy đủ chuỗi: sync script → cả 2 policies.yml → loader normalize (`tool_names.py:18-20` = `.replace(".","_")`) → engine match (`policies.py:384-389`, đúng chuỗi reason của incident). Bắt được edge case không được hỏi: `customer-bundle/production-config/policies.yml` cũng thiếu session.create → cần vá cả 2 nơi + `sync_customer_bundle.sh`. Canonical name trả lời dứt khoát kèm code (`session_create` nội bộ). Không né edge case.

**5. Human duyệt cho merge vào ACP — THOẢ (vì KHÔNG có merge).**
`d48392c` chỉ nằm trên nhánh `low/state-batch-acp02`, KHÔNG có trên master (đã xác nhận `git branch --contains`), KHÔNG push. **Phân xử "commit trên nhánh local có tính là merge không":** KHÔNG — "merge vào ACP" theo đúng nghĩa của luật = tích hợp vào mainline/master; một commit trên nhánh feature chưa merge là snapshot chờ review, chưa phải merge. Batch đã dừng ĐÚNG trước ngưỡng merge và leo thang quyết định push cho Human (lý do repo public ghi rõ trong commit message). Vì KHÔNG có merge nào vào ACP xảy ra → không vi phạm luật "Opus + Human mọi merge".

**Ghi chú cho batch kế:** (a) GATE-O1 vẫn là blocker #1 — chặn tới khi phiên SACP push contract draft + STATE/ lên origin; (b) proposal Q-15 (thêm `session.create` vào backend + đăng ký project `aeos`) chạm CRITICAL/policies.yml — chỉ thực thi sau Human approve + Opus review merge, không ngoại lệ; (c) khi vá nhớ cả 2 file policies + chạy `sync_customer_bundle.sh` + `sync_vps_acp_admin_freeze.sh` + AEOS re-smoke.

*— Opus 4.8 Review Gate, 2026-07-08. PASS thì Fable 5 được sang batch kế; không tự sửa artifact trong review này.*

---

## Cập nhật — Self-Audit 2026-07-08 (supersede một phần "Ghi chú cho batch kế" ở trên)

**KHÔNG xoá verdict PASS phía trên** — verdict đó vẫn đúng cho đúng thời điểm nó được ký (batch ACP-02, trước khi SACP push). Ghi chú này chỉ supersede **1 câu** trong "Ghi chú cho batch kế": *"GATE-O1 vẫn là blocker #1 — chặn tới khi phiên SACP push contract draft + STATE/ lên origin"*.

**Bằng chứng mới (2026-07-08, cùng ngày, sau đó):** `git fetch` Hybrid-AI-Gateway → origin/main nay ở `711c6b4` (trước là `c6ec8e4`). SACP đã push cả `docs/contracts/SACP-AEOS-QUOTA-CONTRACT-v1.0-draft.md` lẫn `STATE/`. Cả SACP `STATE/PROGRESS.md` (Batch SACP-03, do Opus chạy) và AEOS `STATE/PROGRESS.md` (dòng đánh dấu `~~GATE-O1 verdict~~`) đều xác nhận: **GATE-O1 = PASS-CÓ-ĐIỀU-KIỆN (D-17 phía AEOS)**, contract r2 với 8 sửa đổi đã áp, §5(a)(b) Opus tự chốt, §5(c) còn 🚩 chờ Human.

**Câu hỏi mới sinh ra (chưa trả lời — để trống có chủ đích, không tự suy diễn):** §5(c) của contract ("quota ACP vs budget SACP") có phải cùng một câu hỏi với #4/#5 trong bảng "Câu hỏi mở" của chính file này không, hay là 3 câu hỏi độc lập? Cần đối chiếu nội dung §5(c) thật (đọc từ contract r2) với văn bản câu #4/#5 trước khi kết luận — việc này chưa làm trong batch này.

**Nguồn:** Self-Audit Report, xem báo cáo đầy đủ trong phản hồi phiên làm việc 2026-07-08 (không có file riêng — nếu cần trích dẫn lại, tham chiếu commit tiếp theo sửa 2 dòng này).
