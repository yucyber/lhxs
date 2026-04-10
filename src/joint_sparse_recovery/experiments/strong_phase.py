"""Strong phase-transition experiment orchestration."""

from __future__ import annotations

import csv
from pathlib import Path

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.plotting.phase_transition_plots import plot_strong_phase
from joint_sparse_recovery.theory.strong_transition import solve_strong_transition_curve


def run_strong_phase_experiment(
    config_path: str | Path = "configs/strong_phase.yaml",
    profile: str | None = None,
) -> list[dict]:
    """Compute and save all strong transition curves from one config."""

    config = load_config(config_path)
    run_cfg = resolve_run_config(config, profile=profile)

    rows: list[dict] = []
    for algorithm in run_cfg["algorithms"]:
        rows.extend(
            solve_strong_transition_curve(
                algorithm=algorithm,
                delta_grid=run_cfg["delta_grid"],
                rho_upper=run_cfg["rho_upper"],
                bound_model=run_cfg["bound_model"],
            )
        )

    table_path = ensure_parent_dir(run_cfg["output_table"])
    with table_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["algorithm", "bound_model", "delta", "rho", "mu_at_rho"],
        )
        writer.writeheader()
        writer.writerows(rows)

    plot_strong_phase(rows, run_cfg["output_figure"])
    return rows


__all__ = ["run_strong_phase_experiment"]
