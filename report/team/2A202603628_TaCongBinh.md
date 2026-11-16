# Báo cáo cá nhân — 2A202603628_TaCongBinh

## 1. Thông tin thành viên

- Họ tên: Tạ Công Bình
- MSSV: 2A202603628
- Email: 26ai.binhtc@vinuni.edu.vn
- GitHub: https://github.com/BinhTa2004

## 2. Phần việc phụ trách

Tôi phụ trách shape A (workflow), test hồi quy cho workflow, phân công trong `TEAM.md` và tổng hợp báo cáo nhóm/ADR sau khi các thành viên bàn giao kết quả.

Workflow, single và orchestrator đã được tích hợp; benchmark chung đủ bốn shape và crash report đã có. Phần tổng hợp hoàn thiện chọn workflow, cập nhật TEAM/ADR/báo cáo nhóm và đối chiếu số liệu tái lập.

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
- Commit triển khai workflow và 10 test: `b4a73b2` (`update flow`).
- Commit `cba75ce`: dùng Codex bổ sung adapter `src/bonus/swarm_no_peer.py`, ba test `src/tests/test_research_ablation.py` và report `src/reports/research_ablation.json` để R4 có thí nghiệm bỏ riêng một lời gọi peer. Không sửa swarm chính thức; không đăng ký điểm bonus.
- Chốt mốc code/bằng chứng `cba75cea8dfab4bd26e5e22a6c852c49c9d65c3c`; hoàn thiện hồ sơ sau mốc này theo thứ tự nộp của đề bài.

## 4. Bằng chứng

Nguồn số liệu cuối: [`benchmark.json`](../../src/reports/benchmark.json), tạo bằng `lab8.benchmark`, đủ bốn shape, không sửa tay JSON. Workflow có 14 claim × seeds `11,22,33,44,55` = 70 trial; mỗi trial dùng SQLite mới, policy as-of `2026-11-15`. `workflow_selfcheck.json` là bằng chứng giai đoạn riêng workflow trước tích hợp, cùng số liệu workflow.

| Kiểm tra / metric | Kết quả thực tế |
| --- | --- |
| Test mặc định cuối, gồm test toàn nhóm và 3 test ablation | 160 passed, 248 deselected |
| Ma trận student toàn nhóm | 248 passed, 160 deselected; riêng workflow có 62 test |
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
python -m pytest -q -m student -o addopts= --import-mode=importlib -p no:cacheprovider
python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
python -m lab8.benchmark --shapes swarm,swarm_no_peer --extra-shape swarm_no_peer=bonus.swarm_no_peer:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/research_ablation.json
```

Máy kiểm tra dùng Python toàn cục có package `tests` trùng tên và nhiều plugin pytest ngoài lab. Tắt tự nạp plugin và dùng `--import-mode=importlib` để tránh xung đột môi trường; không sửa test, fixture hay thước đo. Lần chạy trong sandbox gặp lỗi quyền thư mục tạm SQLite; chạy kiểm chứng ngoài sandbox đã thành công.

## 5. Công cụ AI đã dùng

Công cụ sử dụng: ChatGPT/Codex. Trợ lý hỗ trợ đọc đề và contract, đề xuất phân công, triển khai workflow/test, chạy kiểm tra và soạn báo cáo này. Phần code và văn bản có hỗ trợ AI, không phải toàn bộ được viết thủ công.

Cách kiểm chứng trong phiên hỗ trợ: đối chiếu `docs/business_rules.md` và `docs/contracts.md`; chạy bộ test host và ma trận public; kiểm các phản ví dụ bằng test riêng; lấy số liệu từ JSON do benchmark tạo. Không gọi model thật, không dùng API key và không bịa commit, run id hoặc điểm hidden.

## 6. Tự đánh giá

Workflow đáp ứng public/test hồi quy mà không cần model quyết định nghiệp vụ. So với single và orchestrator, pass rate bằng nhau trên corpus đã chạy nhưng cost/success thấp nhất, nên ADR chọn workflow. Không suy ra pass rate hidden hoặc ưu thế trên mọi bài toán.

Benchmark cuối đã có đủ bốn shape, crash suite đạt 20/20. Bộ crash suite của đề kiểm host/swarm, còn test workflow và safety kiểm trực tiếp ba vị trí crash trên shape. Chưa có kết quả hidden 40 claim × 5 seed, không giả lập điểm hidden từ public.

Hồ sơ nhóm đã được cập nhật bằng commit/test/report thực tế. Ablation R4 cho thấy bỏ peer acknowledgement giảm chi phí khoảng 1,77% mà không sửa miss seed 55; kết luận giới hạn ở MockLLM và lời gọi cụ thể này.
