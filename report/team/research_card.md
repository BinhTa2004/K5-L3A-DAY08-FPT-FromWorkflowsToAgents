# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R4 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* (thư viện tham khảo, slide 44, 59); bằng chứng loại benchmark. Nhóm chưa đọc toàn văn, chỉ dựa vào tóm tắt trong `docs/bonus_topics.md` (B4); URL cần bổ sung khi đối chiếu nguồn gốc |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Chênh lệch hiệu năng giữa các kiến trúc multi-agent có thể đến từ cách thiết kế benchmark chứ không phải từ topology; muốn so sánh phải giữ cố định runtime, model, tool và có baseline đơn giản |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Kết luận gốc nói về benchmark MAS của paper, không phải bài toán claim hoàn phí. Ở lab: MockLLM, 14 claim public, 5 seed, bảng giá mô phỏng, latency `unavailable` |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Giữ seed 55 và mọi thứ khác cố định, chỉ đổi shape từ swarm sang workflow (rồi single, orchestrator): lỗi duy nhất của swarm (C-002) biến mất, pass rate của seed 55 tăng từ 13/14 lên 14/14. Ngược lại, đổi seed mà giữ nguyên swarm thì lỗi chỉ xuất hiện ở seed chia hết cho 5 |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: MockLLM, tool manifest v1.1, 14 claim public, bảng giá `pricing.yaml`, evaluator `lab8.benchmark`, một SQLite mới cho mỗi trial. Biến duy nhất được thay đổi: shape (workflow / single / orchestrator / swarm). Đối chứng: cùng một shape swarm, chỉ đổi seed 11, 22, 33, 44, 55 |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: swarm tin số ngày trong ticket ở seed 55 nên C-002 trả `resolved` thay vì `denied`. Đo bằng pass rate theo (shape, seed), pass^5 và variance giữa các seed |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn), trong thư mục `src/`:

```text
python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
python -c "import json;d=json.load(open('reports/benchmark.json',encoding='utf-8'));[print(s,seed,sum(r['passed'] for r in d['trials'] if r['shape']==s and r['seed']==seed),'/14') for s in d['by_shape'] for seed in d['controlled_variables']['seeds']]"
```

- Run id / file report: `src/reports/benchmark.json` (280 trial = 4 shape × 14 claim × 5 seed; run id dạng `R-<shape>-<claim>-s<seed>`, ví dụ `R-swarm-C-002-s55`).
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **đúng, trên 4 shape.**

| Shape | Seed 11 | 22 | 33 | 44 | 55 | pass rate | pass^5 | variance |
| --- | --: | --: | --: | --: | --: | --: | --: | --: |
| workflow | 14/14 | 14/14 | 14/14 | 14/14 | 14/14 | 1.000 | 1.000 | 0.000000 |
| single | 14/14 | 14/14 | 14/14 | 14/14 | 14/14 | 1.000 | 1.000 | 0.000000 |
| orchestrator | 14/14 | 14/14 | 14/14 | 14/14 | 14/14 | 1.000 | 1.000 | 0.000000 |
| swarm | 14/14 | 14/14 | 14/14 | 14/14 | **13/14** | 0.986 | 0.929 | 0.000816 |

  - Chỉ đổi shape ở seed 55: swarm fail C-002, workflow, single và orchestrator pass cả 14/14.
  - Chỉ đổi seed với swarm: bốn seed 11, 22, 33, 44 đều 14/14; lỗi xuất hiện đúng một lần, C-002 ở seed 55.
  - Kết luận không vượt quá dữ liệu: lỗi cần cả hai điều kiện (shape swarm và seed chia hết cho 5), nên không thể quy riêng cho topology. Một benchmark chỉ chạy một seed sẽ bỏ sót hoặc phóng đại chênh lệch này, đúng tinh thần của CLAIM.
  - Chi phí mô phỏng mỗi lần thành công: workflow 27,86; single 38,43; orchestrator 46,43; swarm 49,57 VND. Ba shape cùng pass rate 1.000 nhưng workflow rẻ nhất (rẻ hơn single khoảng 27% và orchestrator khoảng 40%), nên trên bộ public thêm tự chủ không mua được thêm độ đúng.
  - Giới hạn: 14 claim public chỉ có một điểm yếu đã biết, nên pass rate 1.000 của ba shape chưa chứng minh chúng đúng trên bộ hidden.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
