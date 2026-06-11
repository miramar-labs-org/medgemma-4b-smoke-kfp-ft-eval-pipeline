# Run History — medgemma-4b-smoke-kfp-ft-eval-pipeline

| Run | Date | Gate | baseline_accuracy | postft_accuracy | Δ acc | baseline_safety | safety_score | Δ safety | Notes |
|---|---|---|---|---|---|---|---|---|---|
| [run-001](run-001.md) | 2026-06-10 | **KILLED** | — | — | — | — | — | — | Killed early. First smoke run; validating 9p adapter copy fix. |
| [run-002](run-002.md) | 2026-06-10 | **KILLED** | — | — | — | — | — | — | Killed early. Testing `download_model` component restructure. |
| [run-003](run-003.md) | 2026-06-11 | **C1 PASS / C2 FAIL** | 0.60 | 0.60 / 0.50 | 0.00 / −0.10 | 4.4 | 4.4 / 4.2 | 0.0 / −0.2 | 2/2 chunks. First full end-to-end chunked run. C2 overfit on short smoke budget (0.33h). GPU nvidia runtime fix validated. |
