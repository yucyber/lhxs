# 步骤12：paper_chunk_resume

- 时间：2026-04-06 18:35
- 本步骤目标：把 paper-scale 的步长对照、弱相变、rank-aware 对照改成可分块落盘、可中断续跑的执行模式，并验证首批 chunk 运行速度
- 本步骤新增/修改文件：
- `scripts/run_step_size_compare.py`
- `scripts/run_weak_phase.py`
- `scripts/run_rank_aware_compare.py`
- `src/joint_sparse_recovery/plotting/phase_transition_plots.py`
- `outputs/profiles/paper/reports/step_size_compare_summary.md`
- `outputs/profiles/paper/reports/weak_phase_summary.md`
- `outputs/profiles/paper/reports/rank_aware_compare_summary.md`
- `outputs/profiles/paper/tables/weak_phase_curves.csv`
- `outputs/profiles/paper/tables/weak_phase_trials.csv`
- `outputs/profiles/paper/tables/rank_aware_compare_curves.csv`
- `outputs/profiles/paper/figures/fig4_rank_aware_compare.png`
- 本步骤执行的命令：
- `.\.venv\Scripts\python.exe scripts\run_step_size_compare.py --profile paper --max-chunks 1`
- `.\.venv\Scripts\python.exe scripts\run_weak_phase.py --profile paper --max-chunks 1`
- `.\.venv\Scripts\python.exe scripts\run_weak_phase.py --profile paper --max-chunks 25`
- `.\.venv\Scripts\python.exe scripts\run_rank_aware_compare.py --profile paper --max-chunks 1`
- `.\.venv\Scripts\python.exe scripts\run_rank_aware_compare.py --profile paper --max-chunks 20`
- 自检结果：确认 `paper` 的 step-size 结果已经在后台长跑中落盘完成；weak 目前推进到 `27/576` chunk、累计 `810` 条 trial；rank-aware 目前推进到 `21/192` chunk。
- 遇到的问题与判断：初版续跑时旧 CSV 读出的 `l` 是字符串、新结果是整数，导致绘图排序报错；已通过统一 group key 排序策略修复。paper-scale 下随着 delta 增大，单 chunk 耗时会明显上升，但每个 chunk 都能实时落盘，已不再是黑箱长跑。
- 下一步建议：继续按批次续跑 `weak` 与 `rank-aware`，优先完成 Gaussian/SNIHT 前半段；等曲线点数足够后，检查 `fit_status` 是否出现大量 fallback，再决定是否先调 band/search 参数。

