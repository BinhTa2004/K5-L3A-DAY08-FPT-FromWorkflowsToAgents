# Decision record

- Shape chọn: workflow
- Commit hash: cba75cea8dfab4bd26e5e22a6c852c49c9d65c3c
- Run id dẫn chứng: R-workflow-C-001-s11, R-workflow-C-014-s11; src/reports/benchmark.json
- Pass rate / pass^5 / seed min-max / variance: 1.0 / 1.0 / 1.0–1.0 / 0.0 (public, 14 claim × 5 seed)
- Cost per success (mô phỏng, VND): 27.857142857142858
- Crash safety: 20/20 (src/reports/crash.json); workflow còn qua test trực tiếp ba vị trí crash/resume
- Secret leak / approval bypass: 0 phát hiện trong public và test an toàn đã chạy; chưa có số đếm hidden chính thức

Commit trên là mốc code và bằng chứng tái lập; hồ sơ được commit sau đó theo thứ tự nộp của đề.

## Vì sao shape này

Chọn workflow vì task dùng order/policy có cấu trúc và các bước phụ thuộc tuần tự. Trên cùng 14 claim, seeds `11,22,33,44,55`, giá và evaluator, workflow/single/orchestrator đều pass 70/70. Workflow có cost/success 27,86 VND mô phỏng, thấp hơn single 38,43 và orchestrator 46,43, không cần gọi model.

Swarm đạt 69/70, pass^5 = 0,928571 và variance = 0,000816327. C-002 seed 55 fail do điểm yếu cố ý tin số ngày trong ticket. Workflow giữ dữ kiện order làm nguồn sự thật. Số liệu lấy từ `src/reports/benchmark.json`, không phải một lần chạy lẻ.

## Có đáng đổi lấy multi-agent không

Giữ workflow làm kiến trúc ít tự chủ nhất đáp ứng bằng chứng hiện có. Thêm điều phối/model chưa cải thiện public accuracy. Chỉ cân nhắc đổi khi corpus đại diện hơn cho thấy lợi ích đo được ở xử lý mơ hồ hoặc điều tra độc lập, vẫn giữ các cổng an toàn.

Ablation R4 bỏ riêng lời gọi `peer` của swarm giảm cost/success từ 49,566957 xuống 48,691594, nhưng giữ nguyên lỗi seed 55. Bỏ lời gọi dư giảm chi phí, không sửa lỗi nguồn dữ kiện. Xem `research_card.md`.

## Trace và bằng chứng

Workflow ghi `claim`, `order_scope`, `quote`, `refund_request`, `refund_outcome`, `decision` theo nhánh chạy. Claim chỉ ghi `found`, `has_order_id`; scope chỉ ghi `visible`, `reason`. Không ghi ticket, principal, nguyên claim/order, `parent_secret`, header, SĐT, địa chỉ, ghi chú nội bộ hoặc tên hàng.

Trace có run id từ `make_run_id`, được ghi ở nhánh trả sớm và crash; `finish()` đọc effect/audit thật từ ledger. Shape không tạo debug log ngoài thư mục trace. Test đặt canary trong secret, ticket, header và PII rồi quét kết quả, các file cùng tiền tố run id và stdout/stderr.

Crash report kiểm host/swarm 20/20. `test_team_workflow.py` và `test_team_safety.py` còn kiểm trực tiếp workflow ở `before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`: retry vẫn một effect và một audit committed. Approval thiếu/hỏng/sai claim không được ghi tiền, quote dương bị từ chối có audit host.

## Giới hạn

Public 100% không chứng minh hidden ≥ 0,75. Chưa có hidden grade/student drop. Số 0 phát hiện chỉ áp dụng test/public, không giả làm số đếm hidden.

MockLLM không phải model sản xuất; giá mô phỏng, latency `unavailable`. Trace steps là số event do từng shape ghi, không đồng nhất với số vòng ReAct hoặc thời gian chạy. So sánh bốn shape thay cả implementation và số lời gọi, nên không tách riêng tác động topology; ablation R4 chỉ thay một lời gọi.

## Tái lập

Chạy trong `src/`:

```powershell
python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
python -m lab8.crash_test --count 20 --out reports/crash.json
python -m lab8.benchmark --shapes swarm,swarm_no_peer --extra-shape swarm_no_peer=bonus.swarm_no_peer:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/research_ablation.json
python -m lab8.check_submission
```
