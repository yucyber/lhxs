# 联合稀疏恢复论文复现项目

本项目围绕论文 **Greedy Algorithms for Joint Sparse Recovery** 做本科毕设级复现整理，包含论文初稿、目标论文清洗文本、AI 工作流方案、中文步骤日志，以及面向 AI 辅助写作/复现的 skills 规则。

## 当前项目状态

### 已整理资产

- 毕业论文初稿：已整理到 `docs/thesis_draft/`
- 目标论文 AI 可读材料：已整理到 `docs/reference_paper/`
- AI 逐文件代码生成方案：已整理到 `docs/ai_workflow/`
- 步骤切换日志：已创建中文目录 `日志/`
- 项目专用 AI 工作流：已放在 `skills/`，并同步了 `.github/` 下的 Copilot skill 配置

### 需要继续对齐的主线

根据 `skills/skills.md` 的项目规则，旧 JOMP/JHTP/JCoSaMP 基线目录已清理，后续代码实现只围绕目标论文主线展开，优先补齐：

- SIHT / SNIHT / SHTP / SNHTP / SCoSaMP
- ARIP 理论保证与收敛/稳定性表述
- strong phase transition / weak phase transition 实验
- 与 RA-SOMP+MUSIC 的对比实验

## 目录结构

```text
.
├── README.md
├── .github/
│   ├── copilot-instructions.md
│   └── skills/
│       └── joint-sparse-thesis-router/
│           └── SKILL.md
├── docs/
│   ├── ai_workflow/
│   │   └── 联合稀疏复现实验_AI逐文件代码生成工作流.md
│   ├── reference_paper/
│   │   ├── Greedy_Algorithms_for_Joint_Sparse_Recovery_AI_digest_zh.md
│   │   ├── Greedy_Algorithms_for_Joint_Sparse_Recovery_chunks.jsonl
│   │   ├── Greedy_Algorithms_for_Joint_Sparse_Recovery_clean.md
│   │   └── Greedy_Algorithms_for_Joint_Sparse_Recovery_digest.json
│   └── thesis_draft/
│       └── 毕业论文_参考文献按引用顺序重排_v2.md
├── skills/
    ├── ai_router_rules_prompt.md
    ├── skills.md
    └── skills_usage_examples.md
└── 日志/
    ├── 日志记录规范.md
    └── 步骤00_20260404_0305_项目清理与工作流方案.md
```

## 关键文件说明

| 路径 | 作用 |
| --- | --- |
| `docs/ai_workflow/联合稀疏复现实验_AI逐文件代码生成工作流.md` | AI 逐文件生成代码的目录树、模块职责、分步骤执行 prompt、日志切换规则 |
| `docs/ai_workflow/联合稀疏论文完整复现计划书.md` | 当前未完成项的优先级、难易程度、实施方案与推进顺序 |
| `docs/thesis_draft/毕业论文_参考文献按引用顺序重排_v2.md` | 当前论文初稿/正文材料 |
| `docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_clean.md` | 目标论文清洗版 Markdown，适合直接给 AI 阅读 |
| `docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_chunks.jsonl` | 按页切块文本，适合后续做 RAG/检索 |
| `docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_digest.json` | 论文结构化摘要，适合程序路由 |
| `docs/reference_paper/Greedy_Algorithms_for_Joint_Sparse_Recovery_AI_digest_zh.md` | 目标论文中文导读 |
| `skills/skills.md` | 项目长期 skill 库 |
| `skills/ai_router_rules_prompt.md` | 自动判定意图、自动选 skill、渐进式披露的规则提示词 |
| `skills/skills_usage_examples.md` | 不同任务下如何路由 skill 的例子 |
| `.github/copilot-instructions.md` | Copilot 侧默认工作流说明 |
| `.github/skills/joint-sparse-thesis-router/SKILL.md` | Copilot 侧项目路由 skill |
| `日志/日志记录规范.md` | 每次切换步骤时，AI 应记录哪些字段、日志如何命名 |
| `日志/步骤00_20260404_0305_项目清理与工作流方案.md` | 本次清理旧目录、创建工作流方案和日志目录的首条记录 |

## AI 代码生成方案入口

如果你要让 AI 直接按步骤生成复现实验代码，请先打开：

- `docs/ai_workflow/联合稀疏复现实验_AI逐文件代码生成工作流.md`
- `docs/ai_workflow/联合稀疏论文完整复现计划书.md`

建议从文档里的 **STEP 0** 开始执行，不要跳步。

如果中途结果对不上，先看 `日志/` 里最近 2~3 份步骤记录，再按 `skills/skills.md` 的 **Skill 4：实验异常诊断** 回溯排查。

## 当前代码与实验怎么跑

### 1. 一键运行全部实验

```powershell
.\.venv\Scripts\python.exe .\scripts\run_all_experiments.py
```

### 1.1 运行更接近论文尺度的 `paper` profile

```powershell
.\.venv\Scripts\python.exe .\scripts\run_all_experiments.py --profile paper
```

### 2. 单独运行某一组实验

```powershell
.\.venv\Scripts\python.exe .\scripts\run_strong_phase.py
.\.venv\Scripts\python.exe .\scripts\run_step_size_compare.py
.\.venv\Scripts\python.exe .\scripts\run_weak_phase.py
.\.venv\Scripts\python.exe .\scripts\run_rank_aware_compare.py
.\.venv\Scripts\python.exe .\scripts\run_reproduction_audit.py
```

也可以给任一脚本追加 `--profile paper`：

```powershell
.\.venv\Scripts\python.exe .\scripts\run_step_size_compare.py --profile paper
.\.venv\Scripts\python.exe .\scripts\run_weak_phase.py --profile paper
.\.venv\Scripts\python.exe .\scripts\run_rank_aware_compare.py --profile paper
.\.venv\Scripts\python.exe .\scripts\run_reproduction_audit.py --profile paper
```

### 3. 运行单元测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

### 4. 输出结果在哪里

- 图像：`outputs/figures/`
- 表格：`outputs/tables/`
- 报告：`outputs/reports/`
- `paper` profile 输出：`outputs/profiles/paper/`
- 步骤日志：`日志/`

当前已经自动跑出一版快速实验结果，可先看：

- `outputs/reports/实验总览报告.md`
- `outputs/reports/复现状态对照表.md`
- `outputs/reports/复现偏差排查入口.md`
- `outputs/figures/fig1_strong_phase.png`
- `outputs/figures/fig2_fig6_step_size_compare.png`
- `outputs/figures/fig3_weak_phase_gaussian.png`
- `outputs/figures/fig4_rank_aware_compare.png`
- `outputs/figures/fig7_weak_phase_dct.png`

### 5. 重要说明

当前 `configs/*.yaml` 的 `paper_reference` 保存原论文协议，`run` 保存默认快速可跑参数，`paper` profile 保存更接近论文尺度的运行参数。

这意味着：

- **已经能自动跑完整实验管线**
- 但当前默认输出是**快速配置下的工程复现结果**
- `--profile paper` 会把输出写到 `outputs/profiles/paper/`，避免覆盖 quick 结果
- `strong phase transition` 目前使用 **surrogate ARIP 边界**
- `RA-SOMP+MUSIC` 目前是**hybrid k-rank greedy + MUSIC completion 的近似实现**

所以当前结果适合先做“流程跑通 + 趋势检查 + 偏差定位”，如果要进一步贴近论文正式曲线，下一步应该优先逐步放大 `configs/*.yaml` 的 `run` 尺度，并核对 strong-phase ARIP 边界公式和 rank-aware 基线实现。

## AI Skills 使用方式

### 推荐入口 1：直接看本地 skill 库

- 先读 `skills/ai_router_rules_prompt.md`
- 再把 `skills/skills.md` 作为长期技能库引用
- 不确定怎么问时，看 `skills/skills_usage_examples.md`

### 推荐入口 2：Copilot / GitHub skill

如果你在支持 `.github` skills 的工具里工作，可以直接用 `.github/skills/joint-sparse-thesis-router/SKILL.md` 和 `.github/copilot-instructions.md` 这套路由规则。

### 这个项目默认的 8 类工作流

- Skill 1：论文复现差距扫描
- Skill 2：实验协议抽取
- Skill 3：复现实验代码共创
- Skill 4：实验异常诊断
- Skill 5：结果解读与论文成文
- Skill 6：答辩准备与提问预测
- Skill 7：ARIP / 相变理论压缩讲解
- Skill 8：图表复刻与 caption 生成

### 短句调用示例

- “第四章偏了吗？”
- “原论文 weak phase transition 怎么设参数？”
- “帮我把 SNIHT 和 SNHTP 的代码结构搭起来”
- “这张图为什么比原论文低很多？”
- “帮我写这一节实验分析”
- “ARIP 答辩时怎么讲？”

## 建议的下一步工作顺序

1. 先读 `docs/ai_workflow/联合稀疏复现实验_AI逐文件代码生成工作流.md`。
2. 按文档里的总控 Prompt，从 **STEP 0** 开始让 AI 逐步生成 `configs/`、`src/`、`scripts/`、`tests/`。
3. 每完成一步，先在 `日志/` 写本步记录，再进入下一步。
4. 等实验结果出来后，再用 `skills/skills.md` 里的 **Skill 5/6/7/8** 做论文分析、答辩准备、理论讲解和图表说明。
