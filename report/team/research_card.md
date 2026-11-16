# Research card

## Câu nghiên cứu

Chọn **R4 — Evaluation confounders**. Giữ model, tools, seeds, corpus, giá và evaluator; chỉ bỏ một lời gọi peer để kiểm phần chi phí có đến từ một thành phần không tác động kết quả hay không.

## Phiếu của nhóm

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R4 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Jiamu Zhang và cộng sự, 2026, [Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems](https://arxiv.org/abs/2609.05933), arXiv:2609.05933v1; bài benchmark, trang arXiv ghi EMNLP 2026. Tên đầy đủ thay cho tên rút gọn trong đề |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Hiệu quả pruning có thể phụ thuộc setup; ở một số bài, baseline đơn giản vẫn giữ độ đúng. Nguồn cố định model/runtime để kiểm ảnh hưởng cấu trúc; không kết luận mọi MAS kém |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | [Mục 4.1 và phụ lục C](https://arxiv.org/html/2609.05933v1): pruning trên GSM8K, MMLU, HumanEval, LiveCodeBench, với backbone cố định theo task. Không phải dữ liệu claim/MockLLM của lab |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Trong swarm tham chiếu, bỏ riêng peer acknowledgement làm mean model calls giảm 3 xuống 2, cost/success giảm, nhưng pass rate/pass^5 và miss C-002 seed 55 giữ nguyên vì output peer không tham gia quote |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ nguyên MockLLM, tools, host, policy, 14 claim, seeds 11/22/33/44/55, giá và evaluator. Chỉ bỏ complete(purpose=peer); vẫn parse/draft, giữ nguyên điểm yếu tin ticket. Adapter src/bonus/swarm_no_peer.py gọi lại swarm chính thức, patch trong một lần chạy rồi khôi phục |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Đo paired trial theo claim/seed: status, proposal, effect, audit, pass rate, pass^5, variance, cost/success, model/tool calls. Rủi ro là vô tình sửa cả luật nghiệp vụ; 3 test kiểm outcome giống nhau, giữ miss đã biết và khôi phục hàm gốc |

## Kết quả ablation

Lệnh đã chạy trong `src/`:

```powershell
python -m lab8.benchmark --shapes swarm,swarm_no_peer --extra-shape swarm_no_peer=bonus.swarm_no_peer:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/research_ablation.json
```

- Code/test/report: commit `cba75ce`; `src/bonus/swarm_no_peer.py`, `src/tests/test_research_ablation.py`, `src/reports/research_ablation.json`.
- 140 trial = 2 biến thể × 14 claim × 5 seed; SQLite mới mỗi trial.
- Run id: `R-swarm-C-002-s55`, `R-swarm_no_peer-C-002-s55`. Tiền tố riêng giúp giữ hai trace để đối chiếu.
- Ba trường hợp test đã chạy: claim được hoàn tiền, claim miss seed 55, claim thiếu mã đơn. Baseline/variant có cùng status/proposal/effect/audit, tool calls giữ nguyên, bớt đúng một model call, chi phí giảm; hàm gốc được khôi phục sau chạy.

| Biến thể | Pass | Pass rate | Pass^5 | Variance | Mean model calls | Cost/success, VND mô phỏng | Tổng chi phí |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| swarm | 69/70 | 0,985714 | 0,928571 | 0,000816327 | 3 | 49,566957 | 3420,12 |
| swarm_no_peer | 69/70 | 0,985714 | 0,928571 | 0,000816327 | 2 | 48,691594 | 3359,72 |

Hypothesis được ủng hộ trong phạm vi này: cost giảm 60,40 VND mô phỏng tổng cộng, khoảng 1,77%; độ đúng không đổi. Lỗi duy nhất của cả hai vẫn là C-002 seed 55. Bớt peer không sửa lỗi nguồn dữ kiện.

## Liên hệ benchmark bốn shape

`src/reports/benchmark.json` (280 trial) cho workflow/single/orchestrator 70/70, swarm 69/70; cost/success tương ứng 27,857143 / 38,427143 / 46,428571 / 49,566957. Đây là so sánh implementation, không phải ablation thuần topology vì số lời gọi và logic dữ kiện cũng khác nhau. Không quy riêng chênh lệch accuracy cho topology.

Lệnh đã dùng:

```powershell
python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
```

## Giới hạn

Đây là áp dụng cách thiết kế thí nghiệm vào lab, không tái lập số liệu paper. MockLLM không phải model sản xuất, latency `unavailable`; chỉ có 14 claim public, chưa có hidden. Peer trong starter chỉ acknowledgement không được dùng ở bước quote, nên không suy ra peer reasoning thật cũng vô ích.

Adapter patch module trong một lần chạy đồng bộ, không dùng đồng thời nhiều thread chung process. Không sửa swarm tham chiếu hoặc JSON bằng tay. Thí nghiệm phục vụ research card bắt buộc, không đăng ký điểm bonus.
