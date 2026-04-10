from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.config_utils import ensure_parent_dir
from joint_sparse_recovery.experiments.rank_aware_compare import run_rank_aware_comparison
from joint_sparse_recovery.experiments.step_size_compare import run_step_size_comparison
from joint_sparse_recovery.experiments.strong_phase import run_strong_phase_experiment
from joint_sparse_recovery.experiments.weak_phase import run_weak_phase_experiment
from joint_sparse_recovery.logging_utils import write_step_log
from joint_sparse_recovery.reporting import write_reproduction_audit


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run all joint sparse recovery experiments.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    return parser.parse_args()


def _output_path(relative_path: str, profile: str | None) -> str:
    if not profile or profile == "quick":
        return f"outputs/{relative_path}"
    return f"outputs/profiles/{profile}/{relative_path}"


def _write_summary_report(section_lines: list[str], profile: str | None) -> Path:
    report_path = ensure_parent_dir(_output_path("reports/实验总览报告.md", profile))
    report_path.write_text("\n".join(section_lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    args = _parse_args()
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    strong_table = _output_path("tables/strong_phase_curves.csv", args.profile)
    strong_figure = _output_path("figures/fig1_strong_phase.png", args.profile)
    step_table = _output_path("tables/step_size_compare_curves.csv", args.profile)
    step_figure = _output_path("figures/fig2_fig6_step_size_compare.png", args.profile)
    step_report = _output_path("reports/step_size_compare_summary.md", args.profile)
    weak_table = _output_path("tables/weak_phase_curves.csv", args.profile)
    weak_trials_table = _output_path("tables/weak_phase_trials.csv", args.profile)
    weak_figure_gaussian = _output_path("figures/fig3_weak_phase_gaussian.png", args.profile)
    weak_figure_dct = _output_path("figures/fig7_weak_phase_dct.png", args.profile)
    weak_report = _output_path("reports/weak_phase_summary.md", args.profile)
    rank_table = _output_path("tables/rank_aware_compare_curves.csv", args.profile)
    rank_figure = _output_path("figures/fig4_rank_aware_compare.png", args.profile)
    rank_report = _output_path("reports/rank_aware_compare_summary.md", args.profile)

    section_lines = [
        "# 实验总览报告",
        "",
        f"- 配置 profile：`{args.profile or 'quick'}`",
        "",
        "## 执行顺序",
        "",
        "1. strong phase transition",
        "2. fixed vs normalized step-size comparison",
        "3. weak phase transition",
        "4. RA-SOMP+MUSIC comparison",
        "",
    ]
    changed_files = []

    try:
        strong_rows = run_strong_phase_experiment(profile=args.profile)
        section_lines.extend(
            [
                "## Strong Phase",
                "",
                f"- 输出表：`{strong_table}`",
                f"- 输出图：`{strong_figure}`",
                f"- 曲线采样点数：{len(strong_rows)}",
                "- 真实性边界：当前曲线使用 surrogate ARIP 边界，不能直接声称严格复现原文 Fig.1。",
                "",
            ]
        )
        changed_files.extend(
            [
                strong_table,
                strong_figure,
            ]
        )

        step_rows = run_step_size_comparison(profile=args.profile)
        section_lines.extend(
            [
                "## Step Size Compare",
                "",
                f"- 输出表：`{step_table}`",
                f"- 输出图：`{step_figure}`",
                f"- 曲线采样点数：{len(step_rows)}",
                "",
            ]
        )
        changed_files.extend(
            [
                step_table,
                step_figure,
                step_report,
            ]
        )

        weak_curves, weak_trials = run_weak_phase_experiment(profile=args.profile)
        section_lines.extend(
            [
                "## Weak Phase",
                "",
                f"- 输出曲线表：`{weak_table}`",
                f"- 输出 trial 表：`{weak_trials_table}`",
                f"- Gaussian 图：`{weak_figure_gaussian}`",
                f"- DCT 图：`{weak_figure_dct}`",
                f"- 曲线点数：{len(weak_curves)}",
                f"- trial 记录数：{len(weak_trials)}",
                "",
            ]
        )
        changed_files.extend(
            [
                weak_table,
                weak_trials_table,
                weak_figure_gaussian,
                weak_figure_dct,
                weak_report,
            ]
        )

        rank_rows = run_rank_aware_comparison(profile=args.profile)
        section_lines.extend(
            [
                "## Rank-Aware Compare",
                "",
                f"- 输出表：`{rank_table}`",
                f"- 输出图：`{rank_figure}`",
                f"- 曲线采样点数：{len(rank_rows)}",
                "- 真实性边界：RA-SOMP+MUSIC 当前是近似实现，若 Fig.4 趋势异常，先查 `src/joint_sparse_recovery/algorithms/ra_somp_music.py` 和最近日志。",
                "",
            ]
        )
        changed_files.extend(
            [
                rank_table,
                rank_figure,
                rank_report,
            ]
        )

        audit_path = write_reproduction_audit(profile=args.profile)
        changed_files.append(str(audit_path))
        report_path = _write_summary_report(section_lines, args.profile)
        changed_files.append(str(report_path))

        log_path = write_step_log(
            step_index=8,
            step_name="全量实验自动运行",
            objective="串行运行 strong/step-size/weak/rank-aware 四组实验，保存图表与总览报告",
            changed_files=changed_files,
            commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_all_experiments.py{profile_suffix}"],
            self_check=f"实验全部执行完成，总览报告已生成：{report_path}；审计报告已生成：{audit_path}",
            issues="当前默认配置仍无法自动补齐 strong phase exact ARIP 公式；RA-SOMP+MUSIC 是更接近论文的近似版，不应过度宣称严格等价。",
            next_step="运行单元测试并生成最终自检日志。",
        )
        print(f"all experiments done, report={report_path}, log={log_path}")
    except Exception as exc:  # noqa: BLE001
        section_lines.extend(
            [
                "## 失败信息",
                "",
                f"- 失败类型：`{type(exc).__name__}`",
                f"- 失败消息：`{exc}`",
                "- 建议先看 `日志/` 最近 2~3 份步骤记录，再定位具体实验模块。",
                "",
                "```text",
                traceback.format_exc(),
                "```",
            ]
        )
        report_path = _write_summary_report(section_lines, args.profile)
        write_step_log(
            step_index=8,
            step_name="全量实验自动运行失败",
            objective="串行运行全部实验时失败，记录错误和排查入口",
            changed_files=[str(path) for path in changed_files] + [str(report_path)],
            commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_all_experiments.py{profile_suffix}"],
            self_check="运行失败，已写 outputs/reports/实验总览报告.md 中的失败信息。",
            issues=f"{type(exc).__name__}: {exc}",
            next_step="先读最近日志和 traceback，再修正对应模块后重跑。",
        )
        raise


if __name__ == "__main__":
    main()
