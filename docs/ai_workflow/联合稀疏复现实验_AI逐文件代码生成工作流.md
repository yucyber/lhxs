# 联合稀疏复现实验 AI 逐文件代码生成工作流

这份文档的用途不是解释论文，而是直接作为 **AI 写代码的工作流编排书**。

目标是让 AI 每完成一个步骤都知道：

- 这一阶段该生成哪些文件
- 每个 `py` 文件负责什么
- 哪些文件暂时不要碰
- 怎么自检算“本步骤完成”
- 切到下一步前，如何把本阶段操作写入 `日志/`
- 下一步应该执行哪个 prompt

## 0. 总约束

### 0.1 主线约束

代码主线只围绕目标论文：

- SIHT
- SNIHT
- SHTP
- SNHTP
- SCoSaMP
- strong phase transition
- weak phase transition
- fixed step size vs normalized step size
- RA-SOMP+MUSIC 对比

不要再把已删除的 JOMP / JHTP / JCoSaMP 旧基线当作主实现入口。

### 0.2 工程约束

- 语言栈：Python + NumPy + SciPy + Matplotlib
- 优先写成清晰科研复现代码，不追求复杂工程技巧
- 所有算法共享同一套数据生成、支撑检测、停止准则、评价指标
- 每个脚本必须能从 `configs/` 读取参数，并把结果写入 `outputs/`
- 每次完成一个 STEP，必须先写 `日志/步骤XX_*.md`，再进入下一 STEP

### 0.3 日志约束

日志目录固定使用中文文件夹：`日志/`

每次步骤切换时，新建一份日志文件，命名格式：

```text
日志/步骤XX_YYYYMMDD_HHMM_步骤名.md
```

每份日志至少包含这 7 项：

```text
# 步骤XX：步骤名

- 时间：
- 本步骤目标：
- 本步骤新增/修改文件：
- 本步骤执行的命令：
- 自检结果：
- 遇到的问题与判断：
- 下一步建议：
```

如果某一步失败，不要直接重写一大堆代码；先读最近 2~3 份日志，再定位是“协议错了 / 算法公式错了 / 统计流程错了 / 作图错了”。

---

## 1. AI 最终要生成的代码目录树

下面这棵树是 **目标结构**，不是要求一步全部生成。

```text
.
├── README.md
├── configs/
│   ├── algorithms.yaml
│   ├── strong_phase.yaml
│   ├── weak_phase.yaml
│   ├── step_size_compare.yaml
│   └── rank_aware_compare.yaml
├── docs/
│   ├── ai_workflow/
│   │   └── 联合稀疏复现实验_AI逐文件代码生成工作流.md
│   ├── reference_paper/
│   └── thesis_draft/
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── scripts/
│   ├── run_strong_phase.py
│   ├── run_weak_phase.py
│   ├── run_step_size_compare.py
│   ├── run_rank_aware_compare.py
│   └── run_all_experiments.py
├── src/
│   └── joint_sparse_recovery/
│       ├── __init__.py
│       ├── logging_utils.py
│       ├── algorithms/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── siht.py
│       │   ├── shtp.py
│       │   ├── scosamp.py
│       │   └── ra_somp_music.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── support_ops.py
│       │   ├── projections.py
│       │   ├── stopping.py
│       │   └── metrics.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── matrix_ensembles.py
│       │   └── signal_models.py
│       ├── experiments/
│       │   ├── __init__.py
│       │   ├── strong_phase.py
│       │   ├── weak_phase.py
│       │   ├── step_size_compare.py
│       │   └── rank_aware_compare.py
│       ├── plotting/
│       │   ├── __init__.py
│       │   └── phase_transition_plots.py
│       └── theory/
│           ├── __init__.py
│           ├── arip_bounds.py
│           └── strong_transition.py
├── tests/
│   ├── test_support_ops.py
│   ├── test_matrix_ensembles.py
│   ├── test_algorithms_smoke.py
│   ├── test_stopping_and_metrics.py
│   └── test_weak_phase_pipeline.py
├── skills/
├── .github/
└── 日志/
    ├── 日志记录规范.md
    └── 步骤00_20260404_项目清理与工作流方案.md
```

---

## 2. 每个 Python 文件职责与完成标准

### 2.1 顶层脚本

| 文件 | 职责 | 完成标准 |
| --- | --- | --- |
| `scripts/run_strong_phase.py` | 读取 `configs/strong_phase.yaml`，计算 Fig.1 理论强相变曲线并出图/表 | 能生成 `outputs/figures/fig1_strong_phase.png` 和对应 csv |
| `scripts/run_weak_phase.py` | 读取 `configs/weak_phase.yaml`，跑 Fig.3/Fig.7/Fig.8 弱相变实验 | 能输出每个算法、每个 `l`、每个矩阵系综的 `rho_W(delta)` |
| `scripts/run_step_size_compare.py` | 复现 Fig.2/Fig.6，比较 SIHT vs SNIHT、SHTP vs SNHTP | 能按 Gaussian/DCT 和 `l=1,10` 出对比图 |
| `scripts/run_rank_aware_compare.py` | 复现 Fig.4，与 RA-SOMP+MUSIC 对比 | 至少能在 Gaussian、`l=1,10` 下出对比曲线 |
| `scripts/run_all_experiments.py` | 串行调度以上脚本，并统一写运行摘要 | 一条命令能跑完整主线，失败时能指出停在哪个实验 |

### 2.2 算法层

| 文件 | 职责 | 核心函数建议 | 完成标准 |
| --- | --- | --- | --- |
| `src/joint_sparse_recovery/algorithms/base.py` | 定义算法统一接口、返回结果结构、公共输入检查 | `SparseRecoveryResult`, `BaseJointSparseSolver` | 所有算法输出字段一致，便于实验层复用 |
| `src/joint_sparse_recovery/algorithms/siht.py` | 实现 SIHT 与 SNIHT | `siht(...)`, `sniht(...)`, `_normalized_step_size(...)` | 小规模无噪声 MMV 上能稳定恢复随机行稀疏信号 |
| `src/joint_sparse_recovery/algorithms/shtp.py` | 实现 SHTP 与 SNHTP | `shtp(...)`, `snhtp(...)` | 支撑更新 + 受限最小二乘流程与论文算法一致 |
| `src/joint_sparse_recovery/algorithms/scosamp.py` | 实现 SCoSaMP | `scosamp(...)` | 按行支撑合并、剪枝、投影、残差更新流程正确 |
| `src/joint_sparse_recovery/algorithms/ra_somp_music.py` | 实现 RA-SOMP+MUSIC 基线 | `ra_somp_music(...)` | 至少能支持 Fig.4 对比；若 MUSIC 先难完整实现，必须在日志中明确缺口 |

### 2.3 公共核心层

| 文件 | 职责 | 核心函数建议 | 完成标准 |
| --- | --- | --- | --- |
| `src/joint_sparse_recovery/core/support_ops.py` | 行支撑检测、行硬阈值、Top-k 行筛选 | `row_l2_norms(...)`, `detect_support(...)`, `hard_threshold_rows(...)` | 对 ties、`k>=n`、空输入有清晰处理 |
| `src/joint_sparse_recovery/core/projections.py` | 支撑集上的最小二乘投影、可选受限 CG 投影 | `least_squares_on_support(...)`, `restricted_cg_projection(...)` | `SHTP/SNHTP/SCoSaMP` 都只通过这里做投影 |
| `src/joint_sparse_recovery/core/stopping.py` | 论文弱相变实验的 5 条停止准则统一实现 | `should_stop(...)`, `ResidualHistory` | 停止原因可返回字符串，方便写日志和调试 |
| `src/joint_sparse_recovery/core/metrics.py` | 成功判据、NMSE、支撑准确率、恢复区域面积 | `is_exact_recovery(...)`, `nmse(...)`, `support_recovery_rate(...)`, `recovery_area_ratio(...)` | 成功阈值默认和论文一致：`||X_hat-X||_F <= 1e-3` |

### 2.4 数据与理论层

| 文件 | 职责 | 核心函数建议 | 完成标准 |
| --- | --- | --- | --- |
| `src/joint_sparse_recovery/data/matrix_ensembles.py` | Gaussian 与 DCT 测量矩阵生成 | `gaussian_matrix(...)`, `dct_subsample_matrix(...)`, `normalize_columns(...)` | Gaussian 方差按论文用 `N(0, 1/m)`；DCT 为随机行采样 |
| `src/joint_sparse_recovery/data/signal_models.py` | 生成行稀疏 MMV 信号与测量 | `sample_row_sparse_support(...)`, `sample_joint_sparse_matrix(...)`, `sample_problem_instance(...)` | 非零值默认从 `{-1,1}` 等概率采样，和论文弱相变实验一致 |
| `src/joint_sparse_recovery/theory/arip_bounds.py` | 封装论文中 ARIP/强相变所需边界函数 | `lower_arip_bound(...)`, `upper_arip_bound(...)`, `mu_siht(...)`, `mu_sniht(...)`, `mu_shtp(...)`, `mu_snhtp(...)`, `mu_scosamp(...)` | 明确哪些公式来自原论文正文，哪些来自附录/参考文献 |
| `src/joint_sparse_recovery/theory/strong_transition.py` | 解 `mu_alg(delta,rho)=1` 得到强相变曲线 | `solve_strong_transition_curve(...)` | 能在一组 `delta` 网格上输出单调合理的 `rho_S(delta)` |

### 2.5 实验与绘图层

| 文件 | 职责 | 核心函数建议 | 完成标准 |
| --- | --- | --- | --- |
| `src/joint_sparse_recovery/experiments/strong_phase.py` | 强相变实验调度与结果落盘 | `run_strong_phase_experiment(...)` | 输出 tidy csv，字段至少包含 `algorithm,delta,rho,strong_mu` |
| `src/joint_sparse_recovery/experiments/weak_phase.py` | 弱相变实验主流程、二分搜索、logistic regression | `binary_search_k_interval(...)`, `sample_transition_band(...)`, `fit_weak_transition_curve(...)`, `run_weak_phase_experiment(...)` | 严格复现论文采样流程：先找 `[kmin,kmax]`，再采 50 个 k，每个 k 跑 10 次 |
| `src/joint_sparse_recovery/experiments/step_size_compare.py` | 固定步长 vs normalized 对照实验 | `run_step_size_comparison(...)` | 统一复用 `weak_phase.py` 的转移曲线估计逻辑 |
| `src/joint_sparse_recovery/experiments/rank_aware_compare.py` | SNIHT/SNHTP/SCoSaMP 与 RA-SOMP+MUSIC 对比 | `run_rank_aware_comparison(...)` | 至少输出 Fig.4 需要的曲线数据 |
| `src/joint_sparse_recovery/plotting/phase_transition_plots.py` | 画 Fig.1/Fig.2/Fig.3/Fig.4/Fig.6/Fig.7/Fig.8 风格图 | `plot_strong_phase(...)`, `plot_weak_phase_family(...)`, `plot_step_size_compare(...)`, `plot_rank_aware_compare(...)` | 所有图的横轴固定 `delta=m/n`，纵轴固定 `rho=k/m`，图注清楚标 `l` 和矩阵系综 |
| `src/joint_sparse_recovery/logging_utils.py` | 生成中文步骤日志、记录命令与产物路径 | `write_step_log(...)`, `append_step_log(...)` | 每个实验脚本结束时能自动写一条 `日志/步骤XX_*.md` |

### 2.6 测试层

| 文件 | 职责 | 完成标准 |
| --- | --- | --- |
| `tests/test_support_ops.py` | 检查行支撑检测、硬阈值 | 覆盖 `k=0`、`k>=n`、重复范数、已知小矩阵 |
| `tests/test_matrix_ensembles.py` | 检查矩阵尺寸、归一化、DCT 行采样合法性 | 不要求统计严格证明，但基本形状和列范数要对 |
| `tests/test_stopping_and_metrics.py` | 检查停止准则与成功判据 | 人工构造 residual history 验证每条停止规则 |
| `tests/test_algorithms_smoke.py` | 检查 5 个主算法在小规模无噪声问题上能跑通 | 先做 smoke test，不要求一开始就追论文大图 |
| `tests/test_weak_phase_pipeline.py` | 检查弱相变二分搜索、采样、拟合输出格式 | 先用很小的 `n` 和很少 trial 做流程测试 |

---

## 3. 工作流编排：AI 按步骤执行，不要跳步

下面每个 STEP 都给了 **可直接复制给 AI 的 prompt**。

### STEP 0：建骨架 + 建日志机制

#### 目标

先只创建目录骨架、空包文件、日志规范，不实现算法细节。

#### 允许修改

- `configs/`
- `scripts/`
- `src/`
- `tests/`
- `outputs/`
- `日志/`
- `README.md`

#### 禁止修改

- `docs/reference_paper/`
- `docs/thesis_draft/`
- `skills/`
- `.github/`

#### 执行 Prompt

```text
你现在执行 STEP 0：建立联合稀疏复现实验代码骨架和中文日志机制。

请只做这几件事：
1. 按 docs/ai_workflow/联合稀疏复现实验_AI逐文件代码生成工作流.md 第 1 节创建目录骨架。
2. 给 src/ 下每个包补最小 __init__.py。
3. 先创建 src/joint_sparse_recovery/logging_utils.py，只实现 write_step_log / append_step_log 两个最小函数，用于往“日志/”写 Markdown 记录。
4. 创建 日志/日志记录规范.md，写清楚每次切换步骤必须记录哪些字段。
5. 创建 日志/步骤00_*.md，记录本步骤创建了哪些目录和文件。

要求：
- 这一阶段不要实现 SIHT/SHTP/SCoSaMP 算法细节。
- 不要改 docs/reference_paper、docs/thesis_draft、skills、.github。
- 完成后告诉我：STEP 0 已完成、生成了哪些文件、下一步进入 STEP 1。
```

#### 完成标准

- 目录骨架存在
- `logging_utils.py` 能写中文日志
- `日志/` 至少有规范文件和 STEP 0 日志

#### 下一步

进入 **STEP 1：固化实验协议配置**。

---

### STEP 1：把原论文实验协议固化成配置文件

#### 目标

先把实验参数和流程冻结到 `configs/*.yaml`，避免后面一边写算法一边猜参数。

#### 允许修改

- `configs/`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 1：从 docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_clean.md 抽取原论文实验协议，并固化到 configs/*.yaml。

请生成这 5 个配置文件：
1. configs/algorithms.yaml
2. configs/strong_phase.yaml
3. configs/weak_phase.yaml
4. configs/step_size_compare.yaml
5. configs/rank_aware_compare.yaml

必须写入的已知原文设置：
- weak phase: n=1024
- l ∈ {1,2,5,10}
- m = ceil(delta*n)
- delta 网格按原文 15 个基础值 + 0.1 到 0.99 间 8 个线性插值值组织
- 先二分搜索 [kmin,kmax]，要求 kmin 处 10 次试验中至少 8 次成功，kmax 处至多 2 次成功
- 再在 [kmin,kmax] 上取 50 个线性间隔 k，若区间长度 <=50 则枚举所有 k
- 每个 k 做 10 次独立试验
- 成功判据：||X_hat - X||_F <= 0.001
- Gaussian 矩阵：A_ij ~ N(0, 1/m)
- DCT 矩阵：从 n×n DCT 矩阵随机选 m 行
- MMV 非零元素：从 {-1,1} 等概率采样
- stopping criteria 按原文 5 条规则逐条写进配置
- SIHT 固定步长 omega=0.65
- SHTP 固定步长 omega=1.0

如果某个参数原文没有完全写死：
- 不要编造
- 配置里写 null 或 unknown
- 旁边用 comment 字段解释“为什么暂缺、建议默认值是什么、后续在哪一步验证”

完成后：
- 写 日志/步骤01_*.md，说明每个配置文件对应原文哪一段、哪些字段仍是 unknown。
- 输出“STEP 1 已完成，下一步进入 STEP 2 公共核心模块”。
```

#### 完成标准

- 5 个 YAML 文件都存在
- 每个配置能被后续脚本直接读取
- unknown 项被显式标出，没有偷偷编数字

#### 下一步

进入 **STEP 2：公共核心模块**。

---

### STEP 2：实现公共核心模块

#### 目标

先写所有算法共享的支撑检测、投影、停止准则、指标函数。

#### 允许修改

- `src/joint_sparse_recovery/core/`
- `src/joint_sparse_recovery/logging_utils.py`
- `tests/test_support_ops.py`
- `tests/test_stopping_and_metrics.py`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 2：实现联合稀疏恢复的公共核心模块。

请逐文件生成并自测：
1. src/joint_sparse_recovery/core/support_ops.py
   - row_l2_norms(X)
   - detect_support(X, k)
   - hard_threshold_rows(X, k)
2. src/joint_sparse_recovery/core/projections.py
   - least_squares_on_support(A, Y, support, n_rows)
   - restricted_cg_projection(A, Y, support, x0=None, max_iter=None, tol=None)
3. src/joint_sparse_recovery/core/stopping.py
   - ResidualHistory
   - should_stop(...)
   - 必须覆盖原论文弱相变实验 5 条停止准则，并返回 stop_reason
4. src/joint_sparse_recovery/core/metrics.py
   - is_exact_recovery(X_hat, X_true, tol=1e-3)
   - nmse(X_hat, X_true)
   - support_recovery_rate(...)
   - recovery_area_ratio(...)

同时补两个测试文件：
- tests/test_support_ops.py
- tests/test_stopping_and_metrics.py

要求：
- 所有函数写 docstring，明确矩阵维度约定。
- detect_support 和 hard_threshold_rows 必须按“行 l2 范数”选支撑。
- restricted_cg_projection 如果暂时先用 least squares 代替，必须在日志里诚实标注，不要假装已经完整复现 CG 版本。
- 本步骤结束前，至少运行这两个测试文件对应的 pytest；如果当前环境没有 pytest，也要在日志里记录“未执行原因”和替代检查方式。

完成后写 日志/步骤02_*.md，并明确下一步进入 STEP 3。
```

#### 完成标准

- 公共核心函数可被算法层直接复用
- 支撑检测逻辑、停止准则、成功判据都有测试覆盖

#### 下一步

进入 **STEP 3：数据生成与矩阵系综模块**。

---

### STEP 3：实现 Gaussian/DCT 矩阵与 MMV 行稀疏信号生成

#### 允许修改

- `src/joint_sparse_recovery/data/`
- `tests/test_matrix_ensembles.py`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 3：实现原论文实验所需的数据生成模块。

请逐文件生成：
1. src/joint_sparse_recovery/data/matrix_ensembles.py
   - normalize_columns(A)
   - gaussian_matrix(m, n, rng)
   - dct_subsample_matrix(m, n, rng)
2. src/joint_sparse_recovery/data/signal_models.py
   - sample_row_support(n, k, rng)
   - sample_joint_sparse_matrix(n, l, support, rng, value_ensemble="rademacher")
   - sample_problem_instance(m, n, k, l, matrix_ensemble, rng)

同时补 tests/test_matrix_ensembles.py。

要求：
- Gaussian 矩阵按原论文用 N(0, 1/m)，不要误写成 N(0,1) 后再随意缩放，除非你在代码和日志中明确说明等价归一化关系。
- DCT 矩阵必须从 n×n DCT 正交矩阵随机抽 m 行，再按需要做列归一化；如果实现里对 SciPy dct 的 axis/norm 有选择，必须写清楚理由。
- MMV 非零元素默认用 {-1,+1} 等概率采样。
- sample_problem_instance 返回值至少包含 A, X_true, Y, support_true。

完成后写 日志/步骤03_*.md，明确下一步进入 STEP 4。
```

#### 下一步

进入 **STEP 4：算法实现层**。

---

### STEP 4：实现 SIHT/SNIHT/SHTP/SNHTP/SCoSaMP/RA-SOMP+MUSIC

#### 允许修改

- `src/joint_sparse_recovery/algorithms/`
- `tests/test_algorithms_smoke.py`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 4：实现目标论文主线算法。

请按这个顺序逐文件写代码，不要反过来：
1. src/joint_sparse_recovery/algorithms/base.py
2. src/joint_sparse_recovery/algorithms/siht.py
3. src/joint_sparse_recovery/algorithms/shtp.py
4. src/joint_sparse_recovery/algorithms/scosamp.py
5. src/joint_sparse_recovery/algorithms/ra_somp_music.py
6. tests/test_algorithms_smoke.py

接口要求：
- 每个算法函数统一接收 A, Y, k 和必要超参数，返回 SparseRecoveryResult。
- SparseRecoveryResult 至少包含 x_hat, support_hat, n_iter, residual_norm, stop_reason。
- SIHT/SHTP 固定步长版本和 SNIHT/SNHTP normalized 版本必须分开实现或通过 mode 参数显式区分，不能混在一起写得看不出来。
- SCoSaMP 默认按原文经验设置：Step 2 的 Sj 先用 k 个候选行，而不是机械照 SMV CoSaMP 的 2k；如果保留可配置项，也要让默认值贴近原文实验。
- RA-SOMP+MUSIC 如果一次难完整写完，先实现 RA-SOMP 主流程并把 MUSIC refinement 单独留函数接口，但必须在日志中明确“当前 Fig.4 对比是否已真正可跑”。

验证要求：
- 用小规模无噪声问题做 smoke test，例如 n=64, m=32, k=4, l=3。
- 每个主算法至少验证“能运行、输出维度正确、支撑大小不超过 k、残差非 NaN”。
- 如果某算法恢复率偏低，不要在本步骤临时调参掩盖问题，先在 日志/步骤04_*.md 记录异常现象，下一步再诊断。

完成后输出“STEP 4 已完成，下一步进入 STEP 5 强相变理论曲线”。
```

---

### STEP 5：实现 strong phase transition 理论曲线

#### 允许修改

- `src/joint_sparse_recovery/theory/`
- `src/joint_sparse_recovery/experiments/strong_phase.py`
- `src/joint_sparse_recovery/plotting/phase_transition_plots.py`
- `scripts/run_strong_phase.py`
- `configs/strong_phase.yaml`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 5：实现原论文 Fig.1 的 strong phase transition 理论曲线计算与绘图。

请逐文件生成：
1. src/joint_sparse_recovery/theory/arip_bounds.py
2. src/joint_sparse_recovery/theory/strong_transition.py
3. src/joint_sparse_recovery/experiments/strong_phase.py
4. src/joint_sparse_recovery/plotting/phase_transition_plots.py 中的 plot_strong_phase(...)
5. scripts/run_strong_phase.py

要求：
- 先从 docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_clean.md 中把 Table I / µ_alg(δ,ρ) / strong phase transition 定义对应段落标注到代码注释或 docstring。
- strong transition 曲线通过解 µ_alg(δ,ρ)=1 得到 rho_S(delta)，每个算法都输出一条曲线。
- 只要某个公式来自附录或参考文献推导、当前还没完全落细，就先把函数接口和 TODO 留清楚，并在日志中标“本步理论实现缺口”，不要伪装成已经严格复现。
- 输出 csv 到 outputs/tables/，图到 outputs/figures/。

完成后写 日志/步骤05_*.md，记录哪些算法曲线已实现、哪些公式仍需二次核对，并进入 STEP 6。
```

---

### STEP 6：实现 weak phase transition 实验引擎

#### 允许修改

- `src/joint_sparse_recovery/experiments/weak_phase.py`
- `src/joint_sparse_recovery/plotting/phase_transition_plots.py`
- `scripts/run_weak_phase.py`
- `configs/weak_phase.yaml`
- `tests/test_weak_phase_pipeline.py`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 6：实现原论文 weak phase transition 实验引擎。

请逐文件生成：
1. src/joint_sparse_recovery/experiments/weak_phase.py
2. scripts/run_weak_phase.py
3. tests/test_weak_phase_pipeline.py
4. 补充 src/joint_sparse_recovery/plotting/phase_transition_plots.py 中的 plot_weak_phase_family(...)

弱相变流程必须按原文组织：
- 对每个 delta 计算 m=ceil(delta*n)
- 对每个算法、每个 l、每个矩阵系综，先二分搜索 k 区间 [kmin,kmax]
- kmin 附近要求 10 次中 >=8 次成功，kmax 附近要求 10 次中 <=2 次成功
- 再在线性网格上采 50 个 k，或区间短时枚举全部 k
- 每个 k 做 10 次独立试验
- 以 ||X_hat - X||_F <= 1e-3 判成功
- 对二分类结果做 logistic regression，提取 50% success 对应的 rho_W(delta)

工程要求：
- 先实现一个小规模 fast mode，方便测试流程；再通过配置切回 n=1024 的正式实验。
- 每条曲线结果保存为 tidy csv，字段至少有 algorithm, ensemble, l, delta, m, rho_w, fit_status。
- 如果 logistic regression 在某些 delta 上拟合失败，不能静默吞掉；要在 csv 和日志里写 fit_status 与失败原因。

完成后写 日志/步骤06_*.md，进入 STEP 7。
```

---

### STEP 7：实现 fixed vs normalized 和 RA-SOMP+MUSIC 对照实验

#### 允许修改

- `src/joint_sparse_recovery/experiments/step_size_compare.py`
- `src/joint_sparse_recovery/experiments/rank_aware_compare.py`
- `scripts/run_step_size_compare.py`
- `scripts/run_rank_aware_compare.py`
- `configs/step_size_compare.yaml`
- `configs/rank_aware_compare.yaml`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 7：实现原论文 Fig.2/Fig.6 的 fixed-vs-normalized 对照，以及 Fig.4 的 RA-SOMP+MUSIC 对照。

请逐文件生成：
1. src/joint_sparse_recovery/experiments/step_size_compare.py
2. src/joint_sparse_recovery/experiments/rank_aware_compare.py
3. scripts/run_step_size_compare.py
4. scripts/run_rank_aware_compare.py

实验要求：
- Fig.2/Fig.6：SIHT vs SNIHT，SHTP vs SNHTP，l=1 和 l=10，Gaussian 与 DCT 都做。
- SIHT 固定步长 omega=0.65，SHTP 固定步长 omega=1.0；normalized 版本按算法内部最优步长规则。
- Fig.4：SNIHT、SNHTP、SCoSaMP 与 RA-SOMP+MUSIC 比较，先做 Gaussian，l=1 和 l=10。

复用要求：
- 不要重新写一套弱相变流程，必须调用 weak_phase.py 里的公共函数。
- 只允许在本步骤新增“实验组合编排”和“对照图整理”，不要复制粘贴 STEP 6 的核心逻辑。

完成后写 日志/步骤07_*.md，进入 STEP 8。
```

---

### STEP 8：统一出图、出表、生成复现摘要

#### 允许修改

- `src/joint_sparse_recovery/plotting/phase_transition_plots.py`
- `scripts/run_all_experiments.py`
- `outputs/reports/`
- `README.md`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 8：统一整理所有实验输出，生成图、表、复现摘要，并更新 README 使用入口。

请完成：
1. 补全 phase_transition_plots.py 中所有绘图函数，统一图风格、坐标轴、图例、标题。
2. 实现 scripts/run_all_experiments.py，按 strong -> step_size_compare -> weak_phase -> rank_aware_compare 顺序串行运行。
3. 在 outputs/reports/ 生成一个 Markdown 摘要，至少列出：
   - 已复现哪些原论文图/表
   - 每张图对应哪个输出文件
   - 哪些结果定性一致、哪些仍有偏差
   - 哪些配置或算法实现仍是 TODO
4. 更新 README.md，只保留新主线入口，不要再写已删除旧基线脚本。
5. 写 日志/步骤08_*.md。

要求：
- run_all_experiments.py 遇到某一步失败时要明确报“哪个实验失败、建议先看哪一份日志”。
- 图表文件命名要和论文图号尽量对应，例如 fig1_strong_phase.png、fig3_weak_phase_gaussian.png。
```

---

### STEP 9：最终自检与偏差定位入口

#### 允许修改

- `tests/`
- `outputs/reports/`
- `日志/`

#### 执行 Prompt

```text
你现在执行 STEP 9：做最终自检，并把“如果复现结果对不上，该先看哪里”写成一份排查入口。

请完成：
1. 运行 tests/ 下所有可运行测试。
2. 快速抽查 outputs/tables/ 和 outputs/figures/ 是否齐全，文件命名是否和 README/报告一致。
3. 新建 outputs/reports/复现偏差排查入口.md，按以下顺序写排查路径：
   - 先看最近一份 日志/步骤XX_*.md
   - 再看对应实验 config
   - 再看算法实现文件
   - 再看 weak_phase 拟合状态或 stopping reason
4. 写 日志/步骤09_*.md，总结当前“已完成 / 未完成 / 风险点”。

要求：
- 不要把“趋势接近”写成“完全复现成功”。
- 必须显式区分：
  A. 原论文明确做过
  B. 本项目已经实现
  C. 本项目尚未实现
```

---

## 4. 推荐 AI 执行总控 Prompt

如果后续你想让 AI 按这份工作流自动推进，可以直接发下面这段总控提示词：

```text
你现在是“Greedy Algorithms for Joint Sparse Recovery 论文复现实验代码代理”。

请严格按 docs/ai_workflow/联合稀疏复现实验_AI逐文件代码生成工作流.md 执行，不要跳步。

全局规则：
1. 一次只执行一个 STEP。
2. 每个 STEP 只能修改该 STEP 允许修改的文件范围。
3. 每个 STEP 完成后，必须先在“日志/”中新建一份“步骤XX_YYYYMMDD_HHMM_步骤名.md”，记录目标、改了哪些文件、执行了什么命令、自检结果、问题、下一步。
4. 写完日志后，再告诉我“STEP X 已完成，建议进入 STEP X+1”。
5. 如果某一步结果异常，不要直接跳到下一步；先读取最近 2~3 份日志和相关 config/code，按 Skill 4 的方式定位原因。
6. 严格区分“原论文明确做过 / 本项目已实现 / 本项目计划补做但未完成”，不要混写。

现在从 STEP 0 开始执行。
```
