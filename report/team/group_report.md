# Báo cáo nhóm — Lab 8 LogiX-VN

Bản tổng hợp hiện tại ghi nhận phần workflow đã triển khai và tự kiểm. Chưa phải báo cáo chốt bài: cần bổ sung single, orchestrator và số liệu so sánh do các thành viên bàn giao. Số liệu lấy từ file trong `src/reports/`, không sửa tay JSON.

## 1. Thông tin nhóm

- Tên nhóm: FPT
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): chưa chốt; phần triển khai workflow hiện chưa commit.

## 2. Mục tiêu và cách tiếp cận

Nhóm xử lý claim hoàn phí LogiX-VN bằng các mức tự chủ khác nhau trên cùng dữ liệu và policy. Mục tiêu là chọn kiến trúc ít tự chủ nhất vẫn đáp ứng nghiệp vụ, approval, chống ghi trùng và bảo mật trace.

Bình phụ trách workflow và tích hợp; Dũng làm single ReAct; Minh làm orchestrator/handoff; Long phụ trách test an toàn, crash, benchmark và research card. Ba shape được viết ở ba file riêng; test nhóm cũng tách file theo người. Bình tổng hợp báo cáo sau khi nhận mô tả và số liệu thật.

## 3. Giải pháp

### Workflow — đã triển khai

Workflow đọc claim bằng `get_claim_view`, từ chối suy ra mã đơn từ ticket, kiểm phạm vi sở hữu bằng `lookup_order`, tính quote bằng `compute_compensation` rồi gọi `durability.issue_refund` nếu quote dương. Mỗi nhánh trả kết quả bằng `common.finish()` để ledger và audit là nguồn sự thật cho `RunResult`.

Model không quyết định nghiệp vụ hoặc số tiền; workflow hiện không cần gọi MockLLM. Host kiểm approval, trần theo đơn, idempotency và ghi audit. Shape truyền quote đầy đủ: C-014 có entitlement 150.000 VND nhưng effect chỉ 120.000 VND vì đã hoàn 30.000 VND trước đó.

`crash_at` được chuyển tiếp, `InjectedCrash` không bị nuốt. Kết nối được đóng và trace được ghi trong `finally`; retry để host đối chiếu ledger thay vì tin checkpoint đơn lẻ. Trace chỉ ghi trạng thái đọc claim, kiểm scope, quote, yêu cầu/kết quả host và quyết định cuối; không ghi ticket, dữ liệu cá nhân hay nguyên claim/order.

### Single và orchestrator — chờ bàn giao

Dũng bổ sung mô tả vòng ReAct, giới hạn bước và cách tính budget; Minh bổ sung mô tả handoff allowlist, investigator chỉ đọc và trace đã sanitize. Không coi việc hai file còn stub là implementation hoàn chỉnh.

## 4. Kết quả

Tự kiểm workflow từ `src/reports/workflow_selfcheck.json`: 14 claim × 5 seed (`11,22,33,44,55`), 70 trial, SQLite mới cho mỗi trial.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success, VND mô phỏng | Mean/p95 steps |
| --- | --- | --- | --- | --- | --- | --- |
| workflow | 1,0 | 1,0 | 1,0–1,0 | 0 | 27,857143 | 5,071429 / 6 |
| single | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo |
| orchestrator | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo |
| swarm | Chờ benchmark chung | Chờ benchmark chung | Chờ benchmark chung | Chờ benchmark chung | Chờ benchmark chung | Chờ benchmark chung |

Bộ mặc định sau khi thêm test workflow: 64 passed; student riêng workflow: 62 passed. Mười trường hợp test mới kiểm ticket giả, thiếu mã đơn có cấu trúc, quote đầy đủ, approval, conflict, ba cửa sổ crash và secret/PII trong trace/stdout.

Các số liệu trên chỉ là tự kiểm một shape; chưa thay thế `src/reports/benchmark.json` đủ bốn shape, `src/reports/crash.json` 20/20 hoặc hidden chính thức. Run id dẫn chứng: `R-workflow-C-001-s11`, `R-workflow-C-014-s11`. Chưa có `student_drop/` để tự kiểm hidden.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Lần kiểm tra bằng Python toàn cục gặp `ImportError: cannot import name 'CLAIMS' from 'tests.conftest'` vì import nhầm package trong `site-packages`. Lần chạy trong sandbox còn gặp `sqlite3.OperationalError: unable to open database file` và lỗi quyền thư mục tạm Windows.

Kiểm chứng thành công với Python 3.12.9 ngoài sandbox, tắt tự nạp plugin pytest và dùng import mode `importlib`; không sửa host hoặc thước đo. Lệnh tái lập từ `src/`:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest -q --import-mode=importlib -p no:cacheprovider
python -m pytest -q -m student -o addopts= -k workflow --import-mode=importlib -p no:cacheprovider
python -m lab8.benchmark --shapes workflow --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/workflow_selfcheck.json
```

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`, giá là mô phỏng. Kết quả public workflow không chứng minh ngưỡng hidden hoặc ưu thế so với các shape chưa đo. Test crash trực tiếp workflow ở ba vị trí không thay thế crash suite 20 điểm của đề.

Chỉ chốt kiến trúc sau benchmark chung cùng corpus/seed/giá và kiểm tra must-pass. Cần hoàn thiện hai shape còn lại, nhận research card/ablation và crash report của Long, sau đó ghi commit thật và chạy `check_submission` đến `0 FAIL`.

## 8. Tài liệu tham khảo

- `docs/business_rules.md`: luật nghiệp vụ, approval và trần theo đơn.
- `docs/contracts.md`: `RunResult` và trace contract v1.
- `docs/metrics.md`: công thức metric.
- `src/reports/workflow_selfcheck.json`: số liệu workflow do công cụ sinh.
- `src/tests/test_team_workflow.py`: test hồi quy phần workflow.
