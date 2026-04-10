# Weak Phase Summary

- 配置 profile：`paper`
- 曲线表：`outputs/profiles/paper/tables/weak_phase_curves.csv`
- trial 表：`outputs/profiles/paper/tables/weak_phase_trials.csv`
- 已完成 chunk：`210/576`
- 本次运行新增 chunk：`3`
- 当前累计曲线点：`210`
- 当前累计 trial 记录数：`6280`
- 运行模式：paper-scale 下采用逐点分块落盘，可中断后直接重跑续跑。
- 下一个待跑 chunk：
  - algorithm=`SNHTP`
  - ensemble=`gaussian`
  - l=`1`
  - delta=`0.75`
- 真实性边界：`paper` profile 更接近论文规模，但 strong phase exact ARIP 公式仍需单独补齐；若 fit_status 出现大量 fallback，应先回查 band/search 参数。
