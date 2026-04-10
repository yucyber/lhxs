"""Weak transition comparison against a rank-aware baseline."""

from __future__ import annotations

import csv
from pathlib import Path

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.experiments.weak_phase import compute_weak_phase_curves
from joint_sparse_recovery.plotting.phase_transition_plots import plot_rank_aware_compare


def run_rank_aware_comparison(
    config_path: str | Path = "configs/rank_aware_compare.yaml",
    algorithms_config_path: str | Path = "configs/algorithms.yaml",
    profile: str | None = None,
) -> list[dict]:
    """Compare SNIHT/SNHTP/SCoSaMP against RA-SOMP+MUSIC."""

    config = load_config(config_path)
    algorithms_config = load_config(algorithms_config_path)
    run_cfg = resolve_run_config(config, profile=profile)

    curve_rows, _ = compute_weak_phase_curves(
        run_cfg=run_cfg,
        algorithms_config=algorithms_config,
        experiment_name="rank_aware_compare",
    )

    table_path = ensure_parent_dir(run_cfg["output_table"])
    with table_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"],
        )
        writer.writeheader()
        writer.writerows(curve_rows)

    plot_rank_aware_compare(curve_rows, run_cfg["output_figure"])
    report_path = ensure_parent_dir(run_cfg["output_report"])
    report_path.write_text(
        "\n".join(
            [
                "# Rank-Aware Comparison",
                "",
                f"- 配置 profile：`{run_cfg['profile_name']}`",
                f"- 曲线表：`{run_cfg['output_table']}`",
                f"- 对照图：`{run_cfg['output_figure']}`",
                "- 解读提示：比较 RA-SOMP+MUSIC 与 SNIHT/SNHTP/SCoSaMP 在 `l=1,10` 下的弱相变曲线。",
                "- 真实性边界：当前 RA-SOMP+MUSIC 已升级为 hybrid k-rank greedy + MUSIC completion 近似版，但仍不能直接视为文献严格等价实现。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return curve_rows


__all__ = ["run_rank_aware_comparison"]
