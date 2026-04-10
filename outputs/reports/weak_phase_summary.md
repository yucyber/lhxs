# Weak Phase Summary

- 配置 profile：`quick`
- 曲线表：`outputs/tables/weak_phase_curves.csv`
- trial 表：`outputs/tables/weak_phase_trials.csv`
- 曲线点数：120
- trial 记录数：1404
- 拟合状态分布：
- `all_failure_fallback`: 1
- `all_success_fallback`: 7
- `logistic_fit`: 112
- 矩阵选项：
- `dct`: `{'normalize_columns': True}`
- `gaussian`: `{}`
- 真实性边界：若使用 `paper` profile，弱相变配置会切到 n=1024 和更接近论文的 band/trial 设置；强相变 exact ARIP 公式仍需补齐。
