# Báo cáo cá nhân — 2A202603608_NguyenTuanDung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tuấn Dũng
- MSSV: 2A202603608
- Email: dzung.apr6th@gmail.com
- GitHub: https://github.com/dzungapr6th99

## 2. Phần việc phụ trách

Phụ trách shape B single agent ReAct trong `src/lab8/shapes/single.py` và test riêng `src/tests/test_team_single.py`. Phần này đã được tích hợp vào nhánh nhóm; không phụ trách ghi trực tiếp ledger hoặc thay host/policy.

## 3. Đóng góp cụ thể

Commit kỹ thuật: [1d4738c](https://github.com/BinhTa2004/K5-L3A-DAY08-FPT-FromWorkflowsToAgents/commit/1d4738cf95a7fdfc5cfb37d05a521bf20169cfec), thêm implementation single và test.

- Giữ nguyên chữ ký `run_claim`, dùng `run_react(max_steps=8, worker=True)`, giữ facts từ observation giữa các lượt.
- Chọn lần lượt các tool đọc claim, order, lịch sử refund, tính quote. Ticket không có quyền thay đổi dữ kiện order hoặc cấp approval.
- Gọi MockLLM cho lượt quyết định, tính model calls/token/cost qua Budget. Trong bản lab này, code chọn action; output MockLLM không phải kế hoạch tự sinh được thực thi.
- Sau vòng lặp, code gọi host bằng quote đầy đủ, giữ nguyên `proposal_amount` kể cả khi effect bị cap hoặc host từ chối. Model/worker không được gọi tool ghi.
- Trả kết quả qua `finish()`; trace chỉ ghi tên action, quote và trạng thái host; không dump observation/ticket. Chuyển tiếp crash injection, flush trace và đóng DB khi thoát.
- Thêm 6 trường hợp test: chạm step cap không ghi tiền, ticket injection có secret, ba vị trí crash/resume, unknown claim có trace.

## 4. Bằng chứng

- `test_single_step_cap_never_writes_refund`.
- `test_single_ignores_ticket_injection_and_hides_it`.
- `test_single_crash_windows_resume_once` (3 tham số).
- `test_single_unknown_claim_writes_fresh_trace`.

Kết quả từ `src/reports/benchmark.json`: 70/70 trial single pass; pass rate/pass^5 = 1,0/1,0; seed min–max = 1,0–1,0; variance = 0; cost/success = 38,427142857 VND mô phỏng; mean/p95 trace steps = 7,785714 / 9. Run id dẫn chứng: `R-single-C-001-s11`, `R-single-C-002-s55`.

Ma trận student single có 62 test xanh trong tổng 248 test student. Bộ mặc định cuối có 160 passed, gồm test các thành viên và ablation; không quy toàn bộ số test đó cho riêng single.

Lệnh kiểm chứng trong `src/` trên môi trường nhóm:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
python -m pytest -q tests/test_team_single.py --import-mode=importlib -p no:cacheprovider
python -m pytest -q -m student -o addopts= -k single --import-mode=importlib -p no:cacheprovider
```

## 5. Công cụ AI đã dùng

ChatGPT/Codex hỗ trợ hoàn thiện báo cáo này từ source, commit và report có sẵn, đồng thời chạy lại kiểm tra tích hợp. Kho repo không ghi công cụ AI dùng khi viết code ban đầu; báo cáo không tự quy công cụ/model chưa được thành viên xác nhận.

Cách kiểm chứng đã có bằng chứng trong phiên hỗ trợ: đọc code để kiểm giới hạn 8 bước và quyền tool, chạy test mặc định/student, đối chiếu số liệu benchmark. Không gọi model thật hoặc dùng API key. Thành viên cần tự đọc lại code và giải thích ranh giới model/code khi nộp.

## 6. Tự đánh giá

Single đáp ứng public và test hồi quy: có giới hạn bước, worker chỉ đọc, host quyết định ghi tiền. So với workflow, độ đúng public bằng nhau nhưng cost/success cao hơn; chưa có bằng chứng cần thêm mức tự chủ này cho task hiện tại.

MockLLM và hàm chọn action xác định không đại diện agent sản xuất. Không coi p95 trace steps 9 là vượt 8 vòng ReAct: steps ở metric là số event trace, khác số lượt vòng lặp. Chưa có hidden grade nên không khẳng định kết quả hidden.
