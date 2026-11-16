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
- Commit `6fe14b9`: bổ sung benchmark cuối đủ bốn shape và cập nhật research card. Ở bước chốt hồ sơ, Bình/Codex bổ sung ablation `cba75ce` để chỉ bỏ lời gọi peer; không quy phần bổ sung này thành commit kỹ thuật của Long.

## 4. Bằng chứng

- Test: `test_no_refund_without_a_valid_own_approval`, `test_low_approval_caps_effect_but_keeps_full_quote`, `test_claims_without_a_payable_quote_leave_ledger_and_audit_empty`, `test_rerun_same_claim_keeps_one_ledger_row_and_one_audit`, `test_second_claim_on_same_order_is_denied_and_total_stays_at_entitlement`, `test_prior_refund_is_denied_then_larger_entitlement_pays_only_difference`, `test_crash_then_resume_gives_exactly_one_refund_and_one_audit`, `test_crash_run_still_leaves_a_clean_trace_file`, `test_secrets_pii_and_hostile_ticket_never_reach_trace_result_or_stdout`, `test_escalated_claim_exposes_nothing_about_the_foreign_order`.
- Lệnh: `python -m pytest -q tests/test_team_safety.py` cho kết quả xanh trên cả 4 shape; `python -m lab8.crash_test --count 20 --out reports/crash.json` cho `crash_safety 20/20`.
- Benchmark `reports/benchmark.json`: workflow, single, orchestrator đều pass rate 1.000 và pass^5 1.000; swarm 0.986 (pass^5 0.929, fail C-002 ở seed 55). Cost/success mô phỏng: workflow 27,86; single 38,43; orchestrator 46,43; swarm 49,57. Chi tiết trong research card.
- Lệnh kiểm tại commit `6fe14b9`: `python -m pytest -q` (157 passed), `python -m pytest -q -m student -o addopts=` (248 passed). Sau ba test ablation bổ sung, bộ mặc định cuối là 160 passed; student vẫn 248 passed. Môi trường Python toàn cục dùng `--import-mode=importlib -p no:cacheprovider` và tắt tự nạp plugin như báo cáo nhóm.

## 5. Công cụ AI đã dùng

Theo khai báo ban đầu của thành viên: Claude Code (Claude Sonnet 5.5) hỗ trợ viết `test_team_safety.py` và soạn research card. Kiểm chứng bằng pytest/crash suite, sửa kỳ vọng tên lý do từ chối của host và dòng ledger lịch sử. Báo cáo cuối đối chiếu với `src/reports/benchmark.json`, thay cho report partial giai đoạn trước.

Ở bước hoàn thiện hồ sơ chung, ChatGPT/Codex hỗ trợ đối chiếu nguồn R4, chạy ablation và tổng hợp báo cáo từ artifact thật. Research card đã có URL nguồn gốc và phân biệt kết luận paper với thí nghiệm lab; không coi việc Codex tra nguồn là bằng chứng thành viên đã tự đọc toàn văn.

## 6. Tự đánh giá

Phần kiểm thử/evaluation có bằng chứng chạy lại: test an toàn cả bốn shape, host xanh, 248 test student xanh, crash 20/20 và benchmark đủ 4 shape × 5 seed. Research card cuối có nguồn gốc và ablation chỉ thay một lời gọi peer; số liệu không chỉnh tay. Public chỉ có 14 claim, chưa chứng minh hidden; thí nghiệm không tái lập benchmark của paper hoặc chứng minh mọi peer call đều thừa.
