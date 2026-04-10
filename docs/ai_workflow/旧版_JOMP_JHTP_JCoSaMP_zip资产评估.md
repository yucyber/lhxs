# 旧版 JOMP / JHTP / JCoSaMP zip 资产评估

## 资产来源

- 原始压缩包：`D:\微信缓存\xwechat_files\wxid_121i9lp1zxp622_91ed\msg\file\2026-04\联合稀疏_第六七章实验代码与结果.zip`
- 临时解压目录：`_tmp_zip_review/`
- 解压内容：
  - `joint_sparse_ch6_ch7_code.py`
  - `joint_sparse_ch6_results/measurement_experiment.csv`
  - `joint_sparse_ch6_results/snr_experiment.csv`

## 核心内容

旧版代码已经包含三类导师点名算法：

- `joint_omp`：逐步选择与残差相关性最大的行支撑，并在当前支撑上最小二乘。
- `joint_htp`：执行梯度步 `X + A^T(Y-AX)`，再进行行硬阈值和支撑最小二乘。
- `joint_cosamp`：每轮用残差相关性选候选支撑，合并当前支撑，最小二乘后再剪枝到 `k` 行。

旧版实验包含两类：

- 测量数变化实验：比较 Gaussian / DCT 两类测量矩阵下，随 `m` 增加的成功率、NMSE、耗时。
- SNR 噪声实验：模拟块状稀疏信道，比较不同 `SNR` 下的成功率、NMSE、耗时。

## 对当前项目的参考价值

### 高价值部分

1. 三个主算法的最小可用版本已经存在，可作为当前项目回归导师主线的起点。
2. 测量数变化、Gaussian/DCT、SNR 鲁棒性三组实验与导师要求高度相关。
3. 输出指标包括 `success_rate`、`nmse`、`time_sec`，可以直接映射到论文实验章节。
4. 旧结果已经能说明一个基本趋势：测量数增加、SNR 提高时，三算法恢复性能提升。

### 中等价值部分

1. `sample_channel_problem` 可转化为“多通道压缩感知/稀疏信道”应用实验。
2. DCT 生成与列归一化逻辑可复用，但要与当前项目的 `matrix_ensembles.py` 统一。
3. 支撑精确恢复判据可保留为一个指标，但建议同时使用当前项目的 Frobenius 成功判据。

### 需要谨慎处理的问题

1. 代码是单文件脚本，不符合当前项目模块化结构。
2. `main()` 输出目录写死为 `/mnt/data/joint_sparse_ch6_results`，不适合 Windows 项目。
3. JCoSaMP 在部分低测量数 DCT/Gaussian 场景下 NMSE 异常大，需要检查最小二乘病态、停止准则和候选支撑更新。
4. 旧实验规模偏小，适合作为本科毕设主实验起点，但不能直接等同于严格论文复现。

## 建议迁移方式

### P0：马上迁移

- 新增 `src/joint_sparse_recovery/algorithms/joint_greedy.py`
  - `joint_omp`
  - `joint_htp`
  - `joint_cosamp`
- 接入当前统一结果对象 `SparseRecoveryResult`。
- 复用当前 `detect_support`、`hard_threshold_rows`、`nmse`、`support_recovery_rate`。

### P0：新增导师主线实验

- 新增 `configs/joint_greedy_baseline.yaml`
- 新增 `src/joint_sparse_recovery/experiments/joint_greedy_baseline.py`
- 新增 `scripts/run_joint_greedy_baseline.py`
- 输出：
  - `outputs/joint_greedy/tables/measurement_experiment.csv`
  - `outputs/joint_greedy/tables/snr_experiment.csv`
  - `outputs/joint_greedy/figures/measurement_success_nmse_time.png`
  - `outputs/joint_greedy/figures/snr_success_nmse_time.png`
  - `outputs/joint_greedy/reports/joint_greedy_summary.md`

### P1：补强实验

- 增加 `L=1,2,5,10` 的多测量向量数影响实验。
- 增加 `k` 变化实验，展示稀疏度变大时三算法退化趋势。
- 增加简化相变图，使用 JOMP/JHTP/JCoSaMP 而不是完全复刻目标论文算法。

### P2：应用化实验

- 将 `sample_channel_problem` 改造成“多通道压缩感知/稀疏信道恢复”实验。
- 后续可再补一个轻量“多任务特征选择”合成数据实验。

## 结论

这个 zip 对当前项目有明确参考价值，而且正好能把项目从“目标论文复现实验工程”拉回导师要求的“Joint OMP / Joint HTP / Joint CoSaMP 主线”。

建议不要直接把旧脚本原样放回项目，而是拆成模块、配置、脚本、报告四层，作为导师主线实验重新接入当前工程。
