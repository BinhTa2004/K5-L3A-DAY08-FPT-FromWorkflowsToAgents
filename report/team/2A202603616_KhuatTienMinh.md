# Báo cáo cá nhân — 2A202603616_KhuatTienMinh

## 1. Thông tin thành viên

- Họ tên: Khuất Tiến Minh
- MSSV: 2A202603616
- Email: Minhktm02@gmail.com
- GitHub: https://github.com/Minhktm02

## 2. Phần việc phụ trách

Phụ trách shape C `src/lab8/shapes/orchestrator.py` và `src/tests/test_team_orchestrator.py`: điều phối investigator chỉ đọc, handoff allowlist, trace an toàn, gọi host đúng quote và hỗ trợ crash/resume.

## 3. Đóng góp cụ thể

Commit kỹ thuật: `9b07572` (`feat: implement orchestrator and investigator`), thêm implementation và 11 test; được tích hợp qua nhánh nhóm.

- Đọc claim bằng `get_claim_view`; unknown claim trả `failed`, thiếu mã đơn trả `needs_info`, sai scope/không tìm thấy đơn trả `escalated`.
- Dùng `make_handoff` với task, claim id, facts rỗng và tool đọc `lookup_order`, `lookup_policy`, `compute_compensation`. Không chuyển nguyên claim hoặc parent secret/header.
- Dùng `run_readonly_investigators`; runtime từ chối write tool cho worker. Trace chỉ ghi handoff đã sanitize và order view đã lọc PII.
- Orchestrator gọi host bằng quote đầy đủ. Quote dương bị host chặn giữ proposal và audit từ chối; conflict trả `failed`; thành công dùng `finish()` lấy effect/audit từ DB.
- Truyền `crash_at`, ghi trace rồi ném lại `InjectedCrash`; đóng kết nối trong `finally`. Retry không tạo refund/audit committed trùng.
- Thêm test về allowlist, quyền tool, secret/PII, thiếu claim/order, principal scope, approval, prompt injection, crash và trần theo đơn.

## 4. Bằng chứng

Test tiêu biểu trong `src/tests/test_team_orchestrator.py`:

- `test_handoff_strictly_complies_with_allowlist`.
- `test_investigator_refuses_write_tools`, `test_investigator_dispatch_blocks_write_tools`.
- `test_trace_and_result_omit_secrets_and_pii`.
- `test_orchestrator_resists_prompt_injection`.
- `test_orchestrator_crash_before_effect`, `test_orchestrator_crash_after_effect_and_resume`.
- `test_orchestrator_order_cap_and_difference_topup`.

`src/reports/benchmark.json`: 70/70 trial orchestrator pass; pass rate/pass^5 = 1,0/1,0; seed min–max = 1,0–1,0; variance = 0; cost/success = 46,428571429 VND mô phỏng; mean/p95 trace steps = 3,714286 / 4. Run id: `R-orchestrator-C-001-s11`, `R-orchestrator-C-014-s11`.

11 test riêng và 62 test student của shape xanh trong kiểm tra tích hợp. Bộ mặc định cuối 160 passed, toàn bộ student 248 passed. Test an toàn chung còn kiểm ba vị trí crash trên cả bốn shape.

Lệnh tái lập trong `src/`:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
python -m pytest -q tests/test_team_orchestrator.py --import-mode=importlib -p no:cacheprovider
python -m pytest -q -m student -o addopts= -k orchestrator --import-mode=importlib -p no:cacheprovider
```

## 5. Công cụ AI đã dùng

ChatGPT/Codex hỗ trợ tổng hợp báo cáo này từ code/commit thật và kiểm tra lại toàn nhóm. Repo không ghi công cụ AI dùng khi viết implementation ban đầu; không tự gán công cụ/model chưa được thành viên xác nhận.

Kiểm chứng bằng test allowlist/worker permissions, thử canary/PII trong dữ liệu, đối chiếu ledger/audit sau crash/retry và đọc report do benchmark sinh. Thành viên cần đọc lại và tự giải thích vì sao tóm tắt bằng LLM không thay thế sanitizer theo allowlist.

## 6. Tự đánh giá

Handoff và investigator giữ ranh giới đọc/ghi; host vẫn là nơi kiểm approval và ghi tiền. Public/test cho thấy quote đầy đủ và retry đúng, nhưng không chứng minh độ đúng trên hidden.

Orchestrator hiện là điều phối Python xác định, không gọi MockLLM. Ít trace event hơn workflow không đồng nghĩa nhanh hơn vì event granularity khác nhau và latency không được đo. Chi phí public cao hơn workflow mà pass rate không tăng, nên nhóm chọn workflow.
