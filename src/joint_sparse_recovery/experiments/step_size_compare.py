"""Fixed-step versus normalized-step weak transition comparisons."""

from __future__ import annotations

import csv
from pathlib import Path

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.experiments.weak_phase import compute_weak_phase_curves
from joint_sparse_recovery.plotting.phase_transition_plots import plot_step_size_compare


def run_step_size_comparison(
    config_path: str | Path = "configs/step_size_compare.yaml",
    algorithms_config_path: str | Path = "configs/algorithms.yaml",
    profile: str | None = None,
) -> list[dict]:
    """Run SIHT-vs-SNIHT and SHTP-vs-SNHTP comparisons."""

    config = load_config(config_path)
    algorithms_config = load_config(algorithms_config_path)
    run_cfg = resolve_run_config(config, profile=profile)
    run_cfg["algorithms"] = sorted({name for pair in run_cfg["algorithm_pairs"] for name in pair})

    curve_rows, _ = compute_weak_phase_curves(
        run_cfg=run_cfg,
        algorithms_config=algorithms_config,
        experiment_name="step_size_compare",
    )

    table_path = ensure_parent_dir(run_cfg["output_table"])
    with table_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"],
        )
        writer.writeheader()
        writer.writerows(curve_rows)

    plot_step_size_compare(curve_rows, run_cfg["output_figure"])
    report_path = ensure_parent_dir(run_cfg["output_report"])
    report_path.write_text(
        "\n".join(
            [
                "# Fixed Step Size vs Normalized Step Size",
                "",
                f"- 配置 profile：`{run_cfg['profile_name']}`",
                f"- 曲线表：`{run_cfg['output_table']}`",
                f"- 对照图：`{run_cfg['output_figure']}`",
                "- 解读提示：同一 `ensemble/l` 下，比较 SIHT vs SNIHT、SHTP vs SNHTP 的 `rho_w(delta)` 曲线高低。",
                "- 真实性边界：当前默认 run 配置是快速实验尺度，不是论文 n=1024 的完整尺度。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return curve_rows


__all__ = ["run_step_size_comparison"]
