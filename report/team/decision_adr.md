# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn:
- Commit hash:
- Run id dẫn chứng:
- Pass rate / pass^5 / seed min-max / variance:
- Cost per success (mô phỏng, VND):
- Crash safety:
- Secret leak / approval bypass:

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Chưa chốt shape và các nhãn số liệu ở trên: cần chờ benchmark chung đủ bốn shape cùng corpus/seed/giá. Không dùng kết quả một shape để tuyên bố đã so sánh toàn bộ kiến trúc.

Workflow là ứng viên đã triển khai: `src/reports/workflow_selfcheck.json` ghi 70/70 trial public pass trên 14 claim × 5 seed, pass rate/pass^5 = 1,0/1,0; seed min–max = 1,0–1,0, variance = 0; cost/success = 27,857142857 VND mô phỏng. Run id ví dụ: `R-workflow-C-001-s11`, `R-workflow-C-014-s11`. Đây là bằng chứng tạm thời cho workflow, không phải benchmark so sánh cuối hoặc điểm hidden.

## Có đáng đổi lấy multi-agent không

Ưu tiên shape ít tự chủ nhất đáp ứng nghiệp vụ và các cổng an toàn. Chỉ đổi sang single/orchestrator/swarm nếu số đo chung cho thấy lợi ích đủ rõ và nhóm giải thích được chi phí, variance cùng giới hạn. Hiện chưa có dữ liệu so sánh để chốt đánh đổi này.

## Trace và bằng chứng

Workflow ghi các event `claim`, `order_scope`, `quote`, `refund_request`, `refund_outcome`, `decision` theo nhánh chạy. Event claim chỉ ghi `found` và `has_order_id`; kiểm scope chỉ ghi `visible` và `reason`. Không ghi ticket, principal, nguyên claim/order, `parent_secret`, header, SĐT, địa chỉ, ghi chú nội bộ hoặc tên hàng.

Trace dùng `Trace(make_run_id(...))`, được ghi cả nhánh trả sớm và khi crash; `finish()` lấy effect/audit thật từ ledger. Shape không tạo debug log ngoài thư mục trace. Test `test_workflow_omits_secrets_pii_and_ticket_from_trace_and_stdout` đặt canary trong ticket, secret, header và PII rồi quét `RunResult`, các file cùng tiền tố run id và stdout/stderr.

Test workflow có ba vị trí crash/resume và kiểm đúng một effect/audit; crash suite `20/20` chính thức và bằng chứng handoff của orchestrator chờ nhóm bổ sung. Chưa có kết quả secret leak/approval bypass của hidden.

## Giới hạn

MockLLM không phải model sản xuất. Latency để `unavailable`. Không sửa JSON cho đủ 0.75.
