# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Nhóm: FPT, lớp L3A; thành viên và đóng góp: `TEAM.md`.
- Commit code/bằng chứng: `cba75cea8dfab4bd26e5e22a6c852c49c9d65c3c`, trùng ADR.
- Shape chọn: `workflow`. Số liệu lấy từ report công cụ sinh, không sửa tay JSON.

## 2. Mục tiêu và cách tiếp cận

Nhóm triển khai cùng task claim hoàn phí bằng workflow, single ReAct và orchestrator, rồi so với swarm tham chiếu để chọn mức tự chủ thấp nhất vẫn đáp ứng nghiệp vụ và an toàn.

Bình làm workflow/tích hợp, Dũng làm single, Minh làm orchestrator/handoff, Long làm test/crash/benchmark/nghiên cứu. Mỗi người sửa shape/test riêng; sau tích hợp kiểm toàn bộ public, đối chiếu khả năng tái lập và chốt ADR.

## 3. Giải pháp

### Workflow

Đọc `get_claim_view` → kiểm mã đơn → kiểm quyền sở hữu bằng `lookup_order` → tính `compute_compensation` → gọi host khi quote dương → trả `common.finish()`. Không lấy mã đơn/số ngày từ ticket, không cần MockLLM.

Host kiểm approval, trần theo đơn và idempotency, ghi ledger/audit trong transaction. Shape truyền quote đầy đủ: C-014 quote 150.000 VND, đã hoàn 30.000 VND, host chỉ ghi thêm 120.000 VND. Quote 0 không gọi ghi; quote dương bị host chặn vẫn giữ proposal và có audit `policy_denied`.

### Single ReAct

Dùng `run_react(max_steps=8, worker=True)`. Hàm quyết định giữ facts qua các lượt và chọn tool đọc claim, order, lịch sử hoàn, tính quote. MockLLM được gọi và tính đủ token/cost cho từng lượt; lựa chọn tool hiện được code điều khiển, không chứng minh khả năng tự lập kế hoạch của model thật.

Sau vòng lặp, code nhận quote và gọi host. Worker không có tool ghi; chạm step cap trả `failed`, không refund. Trace ghi tên action/trạng thái, không dump observation có ticket.

### Orchestrator và handoff

`make_handoff` tạo task, claim id, facts rỗng và tool đọc `lookup_order`, `lookup_policy`, `compute_compensation`. Investigator chạy registry read-only; orchestrator dùng quote rồi gọi host ghi tiền.

Handoff qua allowlist, không chuyển parent context/secret/header. Trace ghi handoff đã sanitize và order view đã lọc PII. Bản này điều phối xác định bằng code và không gọi MockLLM; đây là giới hạn phép so sánh trong starter.

### Durability và trace

Ba shape chuyển tiếp `crash_at` và để injected crash truyền ra. Workflow/single flush trace, đóng DB trong `finally`; orchestrator flush rồi ném lại lỗi. Retry dựa vào ledger với khóa `refund:{claim_id}`, không chỉ checkpoint.

Thiếu mã đơn trả `needs_info`; đơn không có/sai principal trả `escalated`; quote 0 hoặc host chặn trả `denied`; thành công trả `resolved`; unknown claim hoặc amount conflict trả `failed`. Mọi nhánh trả có trace đúng run id; không ghi ticket, secret, header hoặc PII vào trace/stdout.

## 4. Kết quả

`src/reports/benchmark.json`: 4 shape × 14 claim × 5 seed = 280 trial; cùng seeds `11,22,33,44,55`, policy as-of `2026-11-15`, giá/evaluator, SQLite mới mỗi trial.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success, VND mô phỏng | Mean/p95 trace steps |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| workflow | 1,000000 | 1,000000 | 1,000000–1,000000 | 0 | 27,857143 | 5,071429 / 6 |
| single | 1,000000 | 1,000000 | 1,000000–1,000000 | 0 | 38,427143 | 7,785714 / 9 |
| orchestrator | 1,000000 | 1,000000 | 1,000000–1,000000 | 0 | 46,428571 | 3,714286 / 4 |
| swarm | 0,985714 | 0,928571 | 0,928571–1,000000 | 0,000816327 | 49,566957 | 2,8 / 3 |

Swarm fail C-002 seed 55: ticket nói 5 ngày, order 2 ngày; điểm yếu cố ý tin ticket. Student test nhận diện miss này, nên 248 test xanh không có nghĩa mọi trial benchmark đều pass.

Smoke pass; bộ mặc định 160 passed (gồm 3 test ablation bổ sung); student 248 passed. `crash.json` đạt 20/20. Test nhóm kiểm cả 4 shape về approval, scope, order cap, retry, ba vị trí crash, secret/PII. Benchmark/crash được chạy lại và khớp JSON đã commit trước khi hoàn thiện hồ sơ.

Chọn workflow: cùng 70/70 trial với single/orchestrator nhưng cost/success thấp hơn khoảng 27,5% và 40,0%. Run id dẫn chứng: `R-workflow-C-001-s11`, `R-workflow-C-014-s11`. Xem ADR.

Ablation R4 (`research_ablation.json`) chỉ bỏ peer acknowledgement của swarm: mean model calls 3 → 2, cost/success 49,566957 → 48,691594; pass rate/pass^5 và miss C-002 seed 55 không đổi. Không suy ra trao đổi agent luôn thừa. Thí nghiệm phục vụ research card, không đăng ký điểm bonus.

## 5. Khó khăn và cách xử lý

Python toàn cục có package `tests` trùng tên và plugin ngoài lab, gây import nhầm `tests.conftest`. Tắt tự nạp plugin, dùng import mode `importlib`; không sửa test đề. Sandbox Windows có lỗi quyền SQLite/thư mục tạm; kiểm chứng ngoài sandbox thành công. Terminal trực tiếp cần UTF-8 khi in tiếng Việt.

Lệnh test đã dùng trong `src/`, Python 3.12.9:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
python -m lab8.smoke
python -m pytest -q --import-mode=importlib -p no:cacheprovider
python -m pytest -q -m student -o addopts= --import-mode=importlib -p no:cacheprovider
python -m lab8.check_submission
```

Lệnh benchmark/crash/ablation ở ADR và research card. Không commit trace/SQLite; không sửa metrics, durability, policy, config hoặc data.

## 6. Tổng hợp đóng góp

| Thành viên | Bằng chứng |
| --- | --- |
| Bình | `b4a73b2`: workflow + 10 test; `cba75ce`: adapter ablation + 3 test/report; hoàn thiện hồ sơ bằng Codex |
| Dũng | `1d4738c`: single + 6 trường hợp test |
| Minh | `9b07572`: orchestrator + 11 test |
| Long | `def285d`: 76 trường hợp safety; `cf9dafc`, `6fe14b9`: crash, benchmark, research card |

Chi tiết AI và giới hạn trong báo cáo cá nhân. Codex tổng hợp văn bản từ artifact thực tế; không giả định công cụ viết code ban đầu khi chưa có thông tin.

## 7. Hạn chế và hướng cải thiện

Chưa có hidden grade/student drop, chưa xác nhận ngưỡng hidden ≥ 0,75 hoặc số đếm secret/approval chính thức. Public chỉ 14 claim với một miss đã biết. MockLLM không phải model sản xuất; giá mô phỏng, latency `unavailable`.

Các shape khác cả implementation/số lời gọi, không chứng minh tác động thuần topology. Trace steps là event, không phải latency/số vòng ReAct. Adapter ablation chỉ dùng đồng bộ, không chạy đa luồng chung process. Cần corpus rộng và model/runtime thực trước kết luận sản xuất.

## 8. Tài liệu tham khảo

- `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`: luật, contract, metric.
- `src/reports/benchmark.json`, `crash.json`, `research_ablation.json`: số liệu công cụ sinh.
- Zhang và cộng sự (2026), [Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems](https://arxiv.org/abs/2609.05933); nguồn R4, phạm vi trích dẫn ở research card.
