# Team

## Thông tin nhóm

- Tên nhóm: FPT
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-FPT-FromWorkflowsToAgents`
- URL repo, nhánh nộp, commit chốt: https://github.com/BinhTa2004/K5-L3A-DAY08-FPT-FromWorkflowsToAgents ; `main`; commit code/bằng chứng `cba75cea8dfab4bd26e5e22a6c852c49c9d65c3c`.
- Hồ sơ được commit sau mốc code trên theo thứ tự trong `SUBMISSION.md`.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Tạ Công Bình | 2A202603628 | 26ai.binhtc@vinuni.edu.vn | BinhTa2004 | Workflow, tích hợp và hoàn thiện hồ sơ |
| 2 | Nguyễn Tuấn Dũng | 2A202603608 | dzung.apr6th@gmail.com | dzungapr6th99 | Single agent ReAct |
| 3 | Khuất Tiến Minh | 2A202603616 | Minhktm02@gmail.com | Minhktm02 | Orchestrator, handoff và bảo mật trace |
| 4 | Hoàng Hải Long | 2A202603670 | 26ai.longhh@vinuni.edu.vn | hwangron | Kiểm thử an toàn, crash, benchmark và nghiên cứu |

## Phân công và kết quả

Bình viết workflow và tổng hợp hồ sơ; Dũng viết single; Minh viết orchestrator; Long kiểm thử và đo số liệu. Ba shape và test riêng tách file để tránh conflict. Cả ba shape đã tích hợp, mỗi shape qua 62 test student. Bình dùng Codex bổ sung ablation R4, không sửa swarm mẫu.

## Bảng đóng góp

Mỗi dòng ghi commit kỹ thuật và test thực tế, không dùng commit tạo báo cáo thay bằng chứng code.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Tạ Công Bình | Workflow, tích hợp và hồ sơ | `b4a73b2` (workflow/test), `cba75ce` (ablation/test) | `src/tests/test_team_workflow.py` (10 trường hợp), `src/tests/test_research_ablation.py` (3 trường hợp) |
| Nguyễn Tuấn Dũng | Single ReAct | `1d4738c` | `src/tests/test_team_single.py`: 6 trường hợp về step cap, injection, crash, unknown claim |
| Khuất Tiến Minh | Orchestrator và handoff | `9b07572` | `src/tests/test_team_orchestrator.py`: 11 test về allowlist, quyền tool, scope, approval, crash, order cap |
| Hoàng Hải Long | Kiểm thử và evaluation | `def285d` (test), `cf9dafc`, `6fe14b9` (report) | `src/tests/test_team_safety.py`: 76 trường hợp trên 4 shape về approval, idempotency, crash, leak |

## Kiểm chứng chung

- Smoke pass; bộ mặc định 160 passed, bộ student 248 passed.
- `src/reports/benchmark.json`: 4 shape × 14 claim × 5 seed; workflow/single/orchestrator 70/70, swarm 69/70.
- `src/reports/crash.json`: 20/20; test nhóm còn kiểm trực tiếp cả bốn shape ở ba vị trí crash.
- Chọn `workflow`; số liệu và giới hạn ở `report/team/decision_adr.md`.
- `src/reports/research_ablation.json`: ablation phục vụ R4, không đăng ký điểm bonus.
- Không có kết quả hidden chính thức; không dùng kết quả public thay điểm hidden.

## Báo cáo cá nhân và nộp bài

- `report/team/2A202603628_TaCongBinh.md`
- `report/team/2A202603608_NguyenTuanDung.md`
- `report/team/2A202603616_KhuatTienMinh.md`
- `report/team/2A202603670_HoangHaiLong.md`

Hồ sơ được tổng hợp với Codex từ code, commit và report thực tế. Mỗi thành viên đọc lại và chịu trách nhiệm giải thích phần mình. Giữ nguyên file mẫu `MSSV_HoTen.md`.

Mỗi người tự nộp cùng link repo trên LMS. Trạng thái nộp LMS và quyền truy cập của giảng viên không được xác nhận bằng kiểm tra local.
