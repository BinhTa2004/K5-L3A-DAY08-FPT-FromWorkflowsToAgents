# Team

## Thông tin nhóm

- Tên nhóm: FPT
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-FPT-FromWorkflowsToAgents`
- URL repo, nhánh nộp, commit chốt: https://github.com/BinhTa2004/K5-L3A-DAY08-FPT-FromWorkflowsToAgents ; nhánh nộp và commit chốt bổ sung khi hoàn tất.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Tạ Công Bình | 2A202603628 | 26ai.binhtc@vinuni.edu.vn | BinhTa2004 | Workflow, tích hợp và chốt bài nộp |
| 2 | Nguyễn Tuấn Dũng | 2A202603608 | dzung.apr6th@gmail.com | dzungapr6th99 | Single agent ReAct |
| 3 | Khuất Tiến Minh | 2A202603616 | Minhktm02@gmail.com | Minhktm02 | Orchestrator, handoff và bảo mật trace |
| 4 | Hoàng Hải Long | 2A202603670 | Chưa bổ sung | Chưa bổ sung | Kiểm thử, crash, benchmark và nghiên cứu |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Phân công thực hiện

Đây là kế hoạch công việc. Commit, kết quả đo và đóng góp đã hoàn thành chỉ ghi sau khi có bằng chứng thực tế.

| Người | File phụ trách | Công việc | Tiêu chí hoàn thành |
| --- | --- | --- | --- |
| Tạ Công Bình | `src/lab8/shapes/workflow.py`, `src/tests/test_team_workflow.py` (thêm mới), `TEAM.md`, `report/team/group_report.md`, `report/team/decision_adr.md` | Viết workflow cố định; dùng order/policy làm nguồn sự thật; gọi host bằng quote đầy đủ; tích hợp bài, tổng hợp báo cáo và ADR từ kết quả đo | 62 test student workflow xanh; có test tự thêm về nguồn dữ kiện hoặc trần theo đơn; kiểm tra toàn bộ bài và chốt commit/run id sau benchmark |
| Nguyễn Tuấn Dũng | `src/lab8/shapes/single.py`, `src/tests/test_team_single.py` (thêm mới) | Viết `run_react` tối đa 8 bước; agent chỉ chọn tool đọc; đếm chi phí model/tool; code gọi host; viết phần mô tả single và gửi Bình tổng hợp | 62 test student single xanh; có test tự thêm về giới hạn bước hoặc không tin ticket; trace và retry/crash đúng contract |
| Khuất Tiến Minh | `src/lab8/shapes/orchestrator.py`, `src/tests/test_team_orchestrator.py` (thêm mới) | Dùng `make_handoff` và investigator chỉ đọc; lọc dữ liệu theo allowlist; orchestrator gọi host; viết phần mô tả handoff/trace và gửi Bình tổng hợp | 62 test student orchestrator xanh; có test tự thêm về handoff/trace hoặc quyền tool; không đưa secret/PII vào trace |
| Hoàng Hải Long | `src/tests/test_team_safety.py` (thêm mới), `src/reports/benchmark.json` và `src/reports/crash.json` (công cụ sinh), `report/team/research_card.md` | Viết test an toàn trên các shape; kiểm approval, idempotency và crash/resume; chạy benchmark cuối sau khi tích hợp đủ ba shape; thực hiện một ablation R1–R4; gửi số liệu và phân tích cho Bình | Có test kỹ thuật tự thêm; host xanh, toàn bộ 248 test student xanh; crash suite 20/20; benchmark đủ 4 shape và 5 seed; research card có phương pháp, lệnh và số liệu thật |

### Thứ tự phối hợp

1. Cả nhóm cập nhật từ cùng phiên bản `main`, tạo nhánh riêng và đọc `docs/business_rules.md`, `docs/contracts.md` trước khi viết code.
2. Bình, Dũng, Minh triển khai song song ba file shape; Long chuẩn bị test an toàn và kế hoạch ablation. Mỗi người chỉ sửa file mình phụ trách, gửi phần mô tả cho Bình tổng hợp.
3. Mỗi shape qua 62 test student tương ứng rồi tích hợp. Cả ba shape truyền `crash_at` vào `durability.issue_refund`, không nuốt `InjectedCrash`, trả kết quả bằng `common.finish()`.
4. Sau tích hợp, Long chạy host, toàn bộ student, crash suite và benchmark; người phụ trách shape sửa lỗi thuộc shape đó. Không sửa `durability.py`, `policy.py`, `metrics.py`, config, dữ liệu hoặc swarm mẫu.
5. Long điền research card từ thí nghiệm thật; Bình tổng hợp báo cáo nhóm và ADR từ report do công cụ sinh. Chỉ chốt shape sau khi so sánh số liệu.
6. Mỗi người hoàn thiện báo cáo cá nhân, có commit kỹ thuật và ít nhất một test đã thêm hoặc sửa. Ghi commit/test thực tế vào bảng đóng góp; không chỉ dùng commit tạo file báo cáo làm bằng chứng kỹ thuật.
7. Bình kiểm `python -m lab8.check_submission` đạt `0 FAIL`, chốt bài và push. Mỗi thành viên tự nộp link repo nhóm trên LMS.

### Thông tin cần bổ sung

- Hoàng Hải Long bổ sung email và GitHub trong bảng thành viên và báo cáo cá nhân.
- Các báo cáo cá nhân của Dũng, Minh và Long đổi tiêu đề còn là `MSSV_HoTen` thành MSSV/họ tên thực tế.
- Cả bốn báo cáo cá nhân hiện còn phần nội dung mẫu; điền phần việc, đóng góp, bằng chứng, công cụ AI và tự đánh giá sau khi thực hiện.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| | | | |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
