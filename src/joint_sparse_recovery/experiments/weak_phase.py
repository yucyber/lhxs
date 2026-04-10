"""Empirical weak phase-transition experiment pipeline."""

from __future__ import annotations

import csv
from collections.abc import Callable
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

from joint_sparse_recovery.algorithms import ALGORITHM_REGISTRY
from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.core.metrics import is_exact_recovery
from joint_sparse_recovery.data.signal_models import sample_problem_instance
from joint_sparse_recovery.plotting.phase_transition_plots import plot_weak_phase_family


def _solver_kwargs(algorithm: str, algorithms_config: dict) -> dict:
    alg_cfg = algorithms_config["algorithms"][algorithm]
    kwargs = {"max_iterations": int(alg_cfg.get("max_iterations", 300))}
    if algorithm == "SIHT":
        kwargs["omega"] = float(alg_cfg.get("fixed_step_size", 0.65))
    elif algorithm == "SHTP":
        kwargs["omega"] = float(alg_cfg.get("fixed_step_size", 1.0))
    elif algorithm == "SNIHT":
        kwargs["fallback_omega"] = 1.0
    elif algorithm == "SNHTP":
        kwargs["fallback_omega"] = 1.0
    elif algorithm == "SCoSaMP":
        kwargs["candidate_factor"] = int(alg_cfg.get("candidate_size", 1))
    elif algorithm == "RA-SOMP+MUSIC":
        kwargs["use_music"] = bool(alg_cfg.get("music_refinement", True))
    return kwargs


def evaluate_success_rate(
    solver: Callable,
    solver_kwargs: dict,
    m: int,
    n: int,
    k: int,
    l: int,
    matrix_ensemble: str,
    n_trials: int,
    rng: np.random.Generator,
    success_tol: float = 1e-3,
    matrix_options: dict | None = None,
) -> tuple[float, list[dict]]:
    """Run repeated trials for one (m, n, k, l) setting."""

    records: list[dict] = []
    success_count = 0
    for _ in range(int(n_trials)):
        problem = sample_problem_instance(
            m=m,
            n=n,
            k=k,
            l=l,
            matrix_ensemble=matrix_ensemble,
            rng=rng,
            value_ensemble="rademacher",
            matrix_options=matrix_options,
        )
        result = solver(problem.A, problem.Y, k, **solver_kwargs)
        success = is_exact_recovery(result.x_hat, problem.X_true, tol=success_tol)
        success_count += int(success)
        records.append(
            {
                "k": int(k),
                "rho": float(k / max(m, 1)),
                "success": int(success),
                "n_iter": int(result.n_iter),
                "residual_norm": float(result.residual_norm),
                "stop_reason": result.stop_reason,
            }
        )
    return success_count / float(max(n_trials, 1)), records


def binary_search_k_interval(
    solver: Callable,
    solver_kwargs: dict,
    m: int,
    n: int,
    l: int,
    matrix_ensemble: str,
    n_trials: int,
    rng: np.random.Generator,
    max_steps: int = 12,
    success_tol: float = 1e-3,
    high_success_threshold: float = 0.8,
    low_success_threshold: float = 0.2,
    matrix_options: dict | None = None,
) -> tuple[int, int]:
    """Find a [kmin, kmax] transition interval."""

    k_upper = max(1, min(m - 1, n - 1))

    low_success, _ = evaluate_success_rate(
        solver,
        solver_kwargs,
        m,
        n,
        1,
        l,
        matrix_ensemble,
        n_trials,
        rng,
        success_tol,
        matrix_options=matrix_options,
    )
    if low_success < high_success_threshold:
        return 0, min(2, k_upper)

    high_success, _ = evaluate_success_rate(
        solver,
        solver_kwargs,
        m,
        n,
        k_upper,
        l,
        matrix_ensemble,
        n_trials,
        rng,
        success_tol,
        matrix_options=matrix_options,
    )
    if high_success > low_success_threshold:
        return max(1, k_upper - 1), k_upper

    lo, hi = 1, k_upper
    for _ in range(int(max_steps)):
        if hi - lo <= 1:
            break
        mid = (lo + hi) // 2
        mid_success, _ = evaluate_success_rate(
            solver,
            solver_kwargs,
            m,
            n,
            mid,
            l,
            matrix_ensemble,
            n_trials,
            rng,
            success_tol,
            matrix_options=matrix_options,
        )
        if mid_success >= high_success_threshold:
            lo = mid
        elif mid_success <= low_success_threshold:
            hi = mid
        else:
            lo = max(lo, mid - 1)
            hi = min(hi, mid + 1)
            break
    return int(lo), int(hi)


def sample_transition_band(k_min: int, k_max: int, grid_size: int) -> np.ndarray:
    """Return integer k samples on the candidate transition band."""

    k_min = int(max(0, k_min))
    k_max = int(max(k_min, k_max))
    if k_max - k_min <= int(grid_size):
        return np.arange(k_min, k_max + 1, dtype=int)
    return np.unique(np.round(np.linspace(k_min, k_max, int(grid_size))).astype(int))


def _logistic_curve(rho: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-(intercept + slope * rho)))


def _fallback_transition_rho(rho_values: np.ndarray, success_values: np.ndarray) -> tuple[float, str]:
    if np.all(success_values >= 0.5):
        return float(np.max(rho_values)), "all_success_fallback"
    if np.all(success_values < 0.5):
        return 0.0, "all_failure_fallback"
    order = np.argsort(rho_values)
    rho_sorted = rho_values[order]
    success_sorted = success_values[order]
    crossing = np.where(np.diff((success_sorted >= 0.5).astype(int)) != 0)[0]
    if crossing.size == 0:
        return float(rho_sorted[np.argmin(np.abs(success_sorted - 0.5))]), "nearest_half_fallback"
    idx = crossing[0]
    return float(0.5 * (rho_sorted[idx] + rho_sorted[idx + 1])), "crossing_fallback"


def fit_weak_transition_curve(band_records: list[dict]) -> tuple[float, str]:
    """Estimate rho_W(delta) as the 50% success point of a logistic fit."""

    rho_values = np.asarray([row["rho"] for row in band_records], dtype=float)
    success_values = np.asarray([row["success"] for row in band_records], dtype=float)
    if rho_values.size == 0:
        return 0.0, "empty_band"
    if np.unique(success_values).size < 2:
        return _fallback_transition_rho(rho_values, success_values)

    try:
        params, _ = curve_fit(
            _logistic_curve,
            rho_values,
            success_values,
            p0=np.array([5.0, -20.0]),
            bounds=([-100.0, -1000.0], [100.0, -1e-6]),
            maxfev=20000,
        )
        intercept, slope = float(params[0]), float(params[1])
        rho_w = -intercept / slope
        if not np.isfinite(rho_w):
            return _fallback_transition_rho(rho_values, success_values)
        return float(np.clip(rho_w, 0.0, 1.0)), "logistic_fit"
    except Exception as exc:  # noqa: BLE001
        rho_w, status = _fallback_transition_rho(rho_values, success_values)
        return rho_w, f"{status}:{type(exc).__name__}"


def _write_weak_phase_report(curve_rows: list[dict], trial_rows: list[dict], run_cfg: dict) -> None:
    if "output_report" not in run_cfg:
        return

    fit_counts: dict[str, int] = {}
    for row in curve_rows:
        status = str(row["fit_status"])
        fit_counts[status] = fit_counts.get(status, 0) + 1

    fit_lines = ["- 无"] if not fit_counts else [f"- `{key}`: {value}" for key, value in sorted(fit_counts.items())]
    matrix_option_lines = []
    matrix_options = run_cfg.get("matrix_options", {})
    for ensemble, options in sorted(matrix_options.items()):
        matrix_option_lines.append(f"- `{ensemble}`: `{options}`")
    if not matrix_option_lines:
        matrix_option_lines.append("- 使用默认矩阵选项")

    report_path = ensure_parent_dir(run_cfg["output_report"])
    report_path.write_text(
        "\n".join(
            [
                "# Weak Phase Summary",
                "",
                f"- 配置 profile：`{run_cfg['profile_name']}`",
                f"- 曲线表：`{run_cfg['output_table']}`",
                f"- trial 表：`{run_cfg['output_raw_trials']}`",
                f"- 曲线点数：{len(curve_rows)}",
                f"- trial 记录数：{len(trial_rows)}",
                "- 拟合状态分布：",
                *fit_lines,
                "- 矩阵选项：",
                *matrix_option_lines,
                "- 真实性边界：若使用 `paper` profile，弱相变配置会切到 n=1024 和更接近论文的 band/trial 设置；强相变 exact ARIP 公式仍需补齐。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run_weak_phase_experiment(
    config_path: str | Path = "configs/weak_phase.yaml",
    algorithms_config_path: str | Path = "configs/algorithms.yaml",
    profile: str | None = None,
) -> tuple[list[dict], list[dict]]:
    """Run weak phase-transition experiments and save curve/trial outputs."""

    config = load_config(config_path)
    algorithms_config = load_config(algorithms_config_path)
    run_cfg = resolve_run_config(config, profile=profile)
    curve_rows, trial_rows = compute_weak_phase_curves(
        run_cfg=run_cfg,
        algorithms_config=algorithms_config,
        experiment_name="weak_phase",
    )

    curve_path = ensure_parent_dir(run_cfg["output_table"])
    with curve_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"],
        )
        writer.writeheader()
        writer.writerows(curve_rows)

    raw_path = ensure_parent_dir(run_cfg["output_raw_trials"])
    with raw_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=[
                "experiment",
                "algorithm",
                "ensemble",
                "l",
                "delta",
                "m",
                "k",
                "rho",
                "success",
                "n_iter",
                "residual_norm",
                "stop_reason",
            ],
        )
        writer.writeheader()
        writer.writerows(trial_rows)

    for ensemble_key, figure_key, title in [
        ("gaussian", "output_figure_gaussian", "Weak Recovery Phase Transitions: Gaussian Matrix Ensemble"),
        ("dct", "output_figure_dct", "Weak Recovery Phase Transitions: DCT Matrix Ensemble"),
    ]:
        subset = [row for row in curve_rows if row["ensemble"] == ensemble_key]
        if subset and figure_key in run_cfg:
            plot_weak_phase_family(subset, run_cfg[figure_key], title=title)

    _write_weak_phase_report(curve_rows, trial_rows, run_cfg)
    return curve_rows, trial_rows


def compute_weak_phase_curves(
    run_cfg: dict,
    algorithms_config: dict,
    experiment_name: str,
) -> tuple[list[dict], list[dict]]:
    """Compute weak phase-transition curves for one experiment configuration."""

    success_tol = float(algorithms_config["success"]["frobenius_tol"])
    rng = np.random.default_rng(int(run_cfg["random_seed"]))

    curve_rows: list[dict] = []
    trial_rows: list[dict] = []
    for matrix_ensemble in run_cfg["matrix_ensembles"]:
        matrix_options = run_cfg.get("matrix_options", {}).get(matrix_ensemble, {})
        for algorithm in run_cfg["algorithms"]:
            solver = ALGORITHM_REGISTRY[algorithm]
            kwargs = _solver_kwargs(algorithm, algorithms_config)
            for l_value in run_cfg["joint_sparsity_levels"]:
                for delta in run_cfg["delta_grid"]:
                    m = int(np.ceil(float(delta) * int(run_cfg["n"])))
                    k_min, k_max = binary_search_k_interval(
                        solver=solver,
                        solver_kwargs=kwargs,
                        m=m,
                        n=int(run_cfg["n"]),
                        l=int(l_value),
                        matrix_ensemble=matrix_ensemble,
                        n_trials=int(run_cfg["binary_search_trials"]),
                        rng=rng,
                        max_steps=int(run_cfg["max_binary_search_steps"]),
                        success_tol=success_tol,
                        matrix_options=matrix_options,
                    )
                    band_ks = sample_transition_band(k_min, k_max, int(run_cfg["band_grid_size"]))
                    band_records: list[dict] = []
                    for k in band_ks:
                        success_rate, records = evaluate_success_rate(
                            solver=solver,
                            solver_kwargs=kwargs,
                            m=m,
                            n=int(run_cfg["n"]),
                            k=int(k),
                            l=int(l_value),
                            matrix_ensemble=matrix_ensemble,
                            n_trials=int(run_cfg["band_trials"]),
                            rng=rng,
                            success_tol=success_tol,
                            matrix_options=matrix_options,
                        )
                        for record in records:
                            trial_row = {
                                "experiment": experiment_name,
                                "algorithm": algorithm,
                                "ensemble": matrix_ensemble,
                                "l": int(l_value),
                                "delta": float(delta),
                                "m": int(m),
                                **record,
                            }
                            trial_rows.append(trial_row)
                            band_records.append(record)
                        band_records.append(
                            {
                                "k": int(k),
                                "rho": float(k / max(m, 1)),
                                "success": float(success_rate),
                            }
                        )
                    rho_w, fit_status = fit_weak_transition_curve(band_records)
                    curve_rows.append(
                        {
                            "algorithm": algorithm,
                            "ensemble": matrix_ensemble,
                            "l": int(l_value),
                            "delta": float(delta),
                            "m": int(m),
                            "k_min": int(k_min),
                            "k_max": int(k_max),
                            "rho_w": float(rho_w),
                            "fit_status": fit_status,
                        }
                    )

    return curve_rows, trial_rows


__all__ = [
    "binary_search_k_interval",
    "compute_weak_phase_curves",
    "evaluate_success_rate",
    "fit_weak_transition_curve",
    "run_weak_phase_experiment",
    "sample_transition_band",
]
