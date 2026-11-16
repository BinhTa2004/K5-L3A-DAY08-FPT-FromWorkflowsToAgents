# Báo cáo cá nhân — 2A202603628_TaCongBinh

## 1. Thông tin thành viên

- Họ tên: Tạ Công Bình
- MSSV: 2A202603628
- Email: 26ai.binhtc@vinuni.edu.vn
- GitHub: https://github.com/BinhTa2004

## 2. Phần việc phụ trách

Tôi phụ trách shape A (workflow), test hồi quy cho workflow, phân công trong `TEAM.md` và tổng hợp báo cáo nhóm/ADR sau khi các thành viên bàn giao kết quả.

Phần triển khai và kiểm chứng workflow đã hoàn thành trong bản làm việc này. Việc tích hợp single/orchestrator, benchmark bốn shape và chốt kiến trúc còn phụ thuộc bàn giao của nhóm; báo cáo không coi các phần đó là đã hoàn thành.

## 3. Đóng góp cụ thể

- Hoàn thiện `src/lab8/shapes/workflow.py`, giữ nguyên chữ ký `run_claim` và trả `RunResult` bằng `common.finish()`.
- Quy trình cố định: đọc `get_claim_view` → kiểm `order_id` → kiểm phạm vi sở hữu bằng `lookup_order` → gọi `compute_compensation` → chuyển quote dương cho host `durability.issue_refund` → ghi kết quả và trace. Claim không tồn tại trả `failed`; thiếu mã đơn trả `needs_info`; đơn không tồn tại hoặc sai principal trả `escalated`; quote bằng 0 trả `denied`.
- Không phân tích ticket để xác định mã đơn, số ngày trễ hay số tiền. Workflow không cần gọi MockLLM; model calls và token usage bằng 0. Chi phí ba tool đọc/tính được ghi trong `Budget`; việc gọi cổng ghi host tuân theo cách tính của swarm tham chiếu, không cộng thêm một tool call.
- Giữ nguyên quote đầy đủ trong `proposal_amount` và khi gọi host. Ví dụ C-014: quote 150.000 VND, đã hoàn 30.000 VND trước đó, host ghi thêm 120.000 VND. Shape không tự trừ trước.
- Để host kiểm approval, trần theo đơn, idempotency và ghi audit. Quote dương bị host từ chối vẫn giữ nguyên `proposal_amount`; conflict trả `failed` và không sửa dòng ledger cũ.
- Chuyển tiếp `crash_at` và để `InjectedCrash` truyền ra ngoài. Khối `finally` ghi trace an toàn và đóng kết nối SQLite cả khi crash. Retry dựa vào ledger của host.
- Trace chỉ ghi các event `claim`, `order_scope`, `quote`, `refund_request`, `refund_outcome`, `decision` theo nhánh chạy. Không ghi ticket, principal, nguyên claim/order, parent secret, header, phone, address, internal note hoặc item name.
- Thêm `src/tests/test_team_workflow.py` gồm 10 trường hợp kiểm tra: ticket injection/số ngày giả; mã đơn chỉ nằm trong ticket; quote đầy đủ khi hoàn phần chênh; audit khi thiếu approval; ba vị trí crash/resume; conflict khi entitlement đổi; secret/PII trong trace và stdout; claim không tồn tại.
- Tạo bằng công cụ `src/reports/workflow_selfcheck.json` cho riêng workflow, không thay thế `benchmark.json` chính thức do Long phụ trách.
- Commit triển khai: chưa tạo; code, test và báo cáo đang ở working tree. Cần ghi hash thật sau khi commit, không dùng hash commit nền làm bằng chứng triển khai.

## 4. Bằng chứng

Nguồn số liệu: [`workflow_selfcheck.json`](../../src/reports/workflow_selfcheck.json), tạo bằng `lab8.benchmark`, không sửa tay JSON. Corpus public gồm 14 claim, seed `11,22,33,44,55`, tổng 70 trial; mỗi trial dùng SQLite mới, policy as-of `2026-11-15` theo cấu hình đề bài.

| Kiểm tra / metric | Kết quả thực tế |
| --- | --- |
| Test mặc định của repo, gồm 10 test workflow mới | 64 passed, 248 deselected |
| Ma trận student riêng workflow | 62 passed, 250 deselected |
| Workflow public benchmark | 70/70 trial pass |
| Pass rate / pass^5 | 1,0 / 1,0 |
| Seed min–max / variance | 1,0–1,0 / 0,0 |
| Cost/success | 27,857142857 VND mô phỏng |
| Tổng chi phí | 1.950 VND mô phỏng |
| Mean / p95 trace steps | 5,071428571 / 6 |
| Mean model calls / tool calls | 0 / 2,785714286 |
| Latency | `unavailable` |

Run id ví dụ có trong report: `R-workflow-C-001-s11`, `R-workflow-C-002-s55`, `R-workflow-C-014-s11`. Trace được công cụ tạo lại trong `src/traces/`, không commit theo quy định.

Các test tiêu biểu trong `src/tests/test_team_workflow.py`:

- `test_workflow_ignores_ticket_injection_and_overstated_delay`.
- `test_workflow_full_quote_is_preserved_on_partial_order_refund`.
- `test_workflow_crash_resume_keeps_one_effect_and_audit` (ba tham số crash).
- `test_workflow_changed_entitlement_does_not_overwrite_committed_refund`.
- `test_workflow_omits_secrets_pii_and_ticket_from_trace_and_stdout`.

Lệnh kiểm chứng đã chạy trong `src/`, bằng Python 3.12.9 trên Windows:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest -q --import-mode=importlib -p no:cacheprovider
python -m pytest -q -m student -o addopts= -k workflow --import-mode=importlib -p no:cacheprovider
python -m lab8.benchmark --shapes workflow --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/workflow_selfcheck.json
```

Máy kiểm tra dùng Python toàn cục có package `tests` trùng tên và nhiều plugin pytest ngoài lab. Tắt tự nạp plugin và dùng `--import-mode=importlib` để tránh xung đột môi trường; không sửa test, fixture hay thước đo. Lần chạy trong sandbox gặp lỗi quyền thư mục tạm SQLite; chạy kiểm chứng ngoài sandbox đã thành công.

## 5. Công cụ AI đã dùng

Công cụ sử dụng: ChatGPT/Codex. Trợ lý hỗ trợ đọc đề và contract, đề xuất phân công, triển khai workflow/test, chạy kiểm tra và soạn báo cáo này. Phần code và văn bản có hỗ trợ AI, không phải toàn bộ được viết thủ công.

Cách kiểm chứng trong phiên hỗ trợ: đối chiếu `docs/business_rules.md` và `docs/contracts.md`; chạy bộ test host và ma trận public; kiểm các phản ví dụ bằng test riêng; lấy số liệu từ JSON do benchmark tạo. Không gọi model thật, không dùng API key và không bịa commit, run id hoặc điểm hidden.

Trước khi nộp, người phụ trách cần tự đọc lại code và giải thích được vì sao truyền quote đầy đủ, vì sao ticket không có quyền thay đổi dữ kiện, và vì sao retry phải dựa vào ledger.

## 6. Tự đánh giá

Phần workflow đáp ứng bộ public hiện có và các test hồi quy bổ sung, không cần model để quyết định nghiệp vụ có cấu trúc. Kết quả public 100% chỉ chứng minh phạm vi corpus đã chạy; không suy ra pass rate hidden hoặc ưu thế trước các shape chưa benchmark.

Chưa có kết quả hidden 40 claim × 5 seed; chưa có benchmark cuối đủ bốn shape và quyết định kiến trúc chính thức. Bộ crash suite 20 điểm của đề kiểm host/swarm, còn test mới của tôi kiểm trực tiếp workflow ở ba vị trí crash. Hai loại bằng chứng này không thay thế nhau.

Sau khi Dũng, Minh và Long bàn giao, phần tổng hợp của tôi cần cập nhật báo cáo nhóm/ADR bằng report chung, ghi commit kỹ thuật thực tế, kiểm `check_submission` đạt `0 FAIL` và chốt bài nộp. Không tự ghi các công việc phụ thuộc này là đã hoàn tất.
