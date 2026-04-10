# Fixed Step Size vs Normalized Step Size

- 配置 profile：`paper`
- 曲线表：`outputs/profiles/paper/tables/step_size_compare_curves.csv`
- 对照图：`outputs/profiles/paper/figures/fig2_fig6_step_size_compare.png`
- 已完成 chunk：`192/192`
- 本次运行新增 chunk：`0`
- 当前累计曲线点：`384`
- 解读提示：同一 `ensemble/l` 下，比较 SIHT vs SNIHT、SHTP vs SNHTP 的 `rho_w(delta)` 曲线高低。
- 运行模式：paper-scale 下采用逐 delta 分块落盘，可中断后直接重跑续跑。
- 当前所有 chunk 已完成。
- 真实性边界：当前默认 run 配置是快速实验尺度；`paper` profile 更接近论文规模，但 strong phase exact ARIP 公式仍需单独补齐。
