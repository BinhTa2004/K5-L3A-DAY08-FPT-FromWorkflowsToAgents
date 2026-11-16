# Báo cáo cá nhân — 2A202603670_HoangHaiLong

## 1. Thông tin thành viên

- Họ tên: Hoàng Hải Long
- MSSV: 2A202603670
- Email: 26ai.longhh@vinuni.edu.vn
- GitHub: https://github.com/hwangron

## 2. Phần việc phụ trách

Kiểm thử an toàn trên các shape, crash suite, benchmark và research card (câu R4).

## 3. Đóng góp cụ thể

- Commit `def285d`: thêm `src/tests/test_team_safety.py`, chạy cùng một kịch bản qua từng shape đã cài đặt (workflow, orchestrator, swarm; single tự bật khi `single.py` hết là stub). Sau khi `single.py` được tích hợp, bộ mặc định có 157 passed, không còn test skip.
- Commit `cf9dafc`: điền `report/team/research_card.md` (R4) từ số liệu thật, thêm `src/reports/crash.json` (crash suite 20/20).
- Quyết định kỹ thuật: kiểm lý do từ chối đúng theo host (`missing_approval`, `approval_expired`, `approval_revoked`, `non_positive_amount`, `approval_claim_mismatch`, `order_already_refunded`) thay vì chỉ kiểm status; so ledger theo từng claim vì DB public đã có sẵn dòng hoàn tiền lịch sử; dùng seed 11 để swarm không rơi vào điểm yếu cố ý ở seed chia hết cho 5.
- Sau khi ba shape được tích hợp: chạy host gate (157 passed), student matrix (248 passed), crash suite (20/20) và benchmark 4 shape × 5 seed vào `src/reports/benchmark.json`, rồi cập nhật research card.

## 4. Bằng chứng

- Test: `test_no_refund_without_a_valid_own_approval`, `test_low_approval_caps_effect_but_keeps_full_quote`, `test_claims_without_a_payable_quote_leave_ledger_and_audit_empty`, `test_rerun_same_claim_keeps_one_ledger_row_and_one_audit`, `test_second_claim_on_same_order_is_denied_and_total_stays_at_entitlement`, `test_prior_refund_is_denied_then_larger_entitlement_pays_only_difference`, `test_crash_then_resume_gives_exactly_one_refund_and_one_audit`, `test_crash_run_still_leaves_a_clean_trace_file`, `test_secrets_pii_and_hostile_ticket_never_reach_trace_result_or_stdout`, `test_escalated_claim_exposes_nothing_about_the_foreign_order`.
- Lệnh: `python -m pytest -q tests/test_team_safety.py` cho kết quả xanh trên cả 4 shape; `python -m lab8.crash_test --count 20 --out reports/crash.json` cho `crash_safety 20/20`.
- Benchmark `reports/benchmark.json`: workflow, single, orchestrator đều pass rate 1.000 và pass^5 1.000; swarm 0.986 (pass^5 0.929, fail C-002 ở seed 55). Cost/success mô phỏng: workflow 27,86; single 38,43; orchestrator 46,43; swarm 49,57. Chi tiết trong research card.
- Lệnh kiểm: `python -m pytest -q` (157 passed), `python -m pytest -q -m student -o addopts=` (248 passed).

## 5. Công cụ AI đã dùng

Claude Code (Claude Sonnet 5.5): hỗ trợ viết `test_team_safety.py` và soạn research card. Tôi tự kiểm tra bằng cách chạy pytest và crash suite trên máy, sửa hai chỗ test sai kỳ vọng (tên lý do từ chối của host và dòng ledger lịch sử), và đối chiếu số liệu research card với `benchmark_partial.json`. Phần nguồn của R4 chỉ dựa trên tóm tắt trong `docs/bonus_topics.md`, chưa đọc toàn văn paper.

## 6. Tự đánh giá

Các mục tiêu của phần tôi đã đạt và có bằng chứng chạy lại được: test an toàn trên cả 4 shape, host xanh, 248 test student xanh, crash suite 20/20, benchmark đủ 4 shape × 5 seed và research card có số liệu thật. Hạn chế: bộ public chỉ có 14 claim nên pass rate 1.000 chưa chứng minh kết quả trên bộ hidden; nguồn paper R4 chưa được đối chiếu toàn văn.
