from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.experiments.weak_phase import compute_weak_phase_curves, run_weak_phase_experiment
from joint_sparse_recovery.logging_utils import write_step_log
from joint_sparse_recovery.plotting.phase_transition_plots import plot_weak_phase_family

CURVE_FIELDNAMES = ["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"]
TRIAL_FIELDNAMES = [
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
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the weak phase experiment.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=None,
        help="For paper-scale runs, process at most this many single-(algorithm,ensemble,l,delta) chunks.",
    )
    return parser.parse_args()


def _curve_key_from_values(algorithm: str, ensemble: str, l_value: int, delta: float) -> tuple[str, str, int, float]:
    return algorithm, ensemble, int(l_value), round(float(delta), 10)


def _curve_key_from_row(row: dict) -> tuple[str, str, int, float]:
    return _curve_key_from_values(
        algorithm=str(row["algorithm"]),
        ensemble=str(row["ensemble"]),
        l_value=int(float(row["l"])),
        delta=float(row["delta"]),
    )


def _load_existing_rows(path: str) -> list[dict]:
    resolved = ensure_parent_dir(path)
    if not resolved.exists():
        return []
    with resolved.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        return [dict(row) for row in reader]


def _write_curve_rows(path: str, rows: list[dict]) -> Path:
    resolved = ensure_parent_dir(path)
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            str(row["ensemble"]),
            int(float(row["l"])),
            str(row["algorithm"]),
            float(row["delta"]),
        ),
    )
    with resolved.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=CURVE_FIELDNAMES)
        writer.writeheader()
        writer.writerows(sorted_rows)
    return resolved


def _append_trial_rows(path: str, rows: list[dict]) -> Path:
    resolved = ensure_parent_dir(path)
    file_exists = resolved.exists()
    with resolved.open("a", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=TRIAL_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
    return resolved


def _chunk_plan(run_cfg: dict) -> list[dict]:
    chunks: list[dict] = []
    for algorithm in run_cfg["algorithms"]:
        for ensemble in run_cfg["matrix_ensembles"]:
            for l_value in run_cfg["joint_sparsity_levels"]:
                for delta in run_cfg["delta_grid"]:
                    chunks.append(
                        {
                            "algorithm": str(algorithm),
                            "ensemble": str(ensemble),
                            "l": int(l_value),
                            "delta": float(delta),
                        }
                    )
    return chunks


def _chunk_done(chunk: dict, existing_keys: set[tuple[str, str, int, float]]) -> bool:
    return _curve_key_from_values(
        chunk["algorithm"],
        chunk["ensemble"],
        chunk["l"],
        chunk["delta"],
    ) in existing_keys


def _write_progress_report(
    run_cfg: dict,
    curve_rows: list[dict],
    completed_chunks: int,
    total_chunks: int,
    processed_this_run: int,
    next_chunk: dict | None,
    trial_count: int,
) -> Path:
    report_path = ensure_parent_dir(run_cfg["output_report"])
    lines = [
        "# Weak Phase Summary",
        "",
        f"- 配置 profile：`{run_cfg['profile_name']}`",
        f"- 曲线表：`{run_cfg['output_table']}`",
        f"- trial 表：`{run_cfg['output_raw_trials']}`",
        f"- 已完成 chunk：`{completed_chunks}/{total_chunks}`",
        f"- 本次运行新增 chunk：`{processed_this_run}`",
        f"- 当前累计曲线点：`{len(curve_rows)}`",
        f"- 当前累计 trial 记录数：`{trial_count}`",
        "- 运行模式：paper-scale 下采用逐点分块落盘，可中断后直接重跑续跑。",
    ]
    if next_chunk is not None:
        lines.extend(
            [
                "- 下一个待跑 chunk：",
                f"  - algorithm=`{next_chunk['algorithm']}`",
                f"  - ensemble=`{next_chunk['ensemble']}`",
                f"  - l=`{next_chunk['l']}`",
                f"  - delta=`{next_chunk['delta']}`",
            ]
        )
    else:
        lines.append("- 当前所有 chunk 已完成。")
    lines.extend(
        [
            "- 真实性边界：`paper` profile 更接近论文规模，但 strong phase exact ARIP 公式仍需单独补齐；若 fit_status 出现大量 fallback，应先回查 band/search 参数。",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _run_incremental_weak_phase(
    run_cfg: dict,
    algorithms_config: dict,
    profile: str | None,
    max_chunks: int | None,
) -> tuple[list[dict], int, int]:
    chunk_plan = _chunk_plan(run_cfg)
    row_map = {_curve_key_from_row(row): row for row in _load_existing_rows(run_cfg["output_table"])}
    trial_count = max(0, len(_load_existing_rows(run_cfg["output_raw_trials"])))
    processed_this_run = 0

    for chunk in chunk_plan:
        if _chunk_done(chunk, set(row_map)):
            continue
        if max_chunks is not None and processed_this_run >= max_chunks:
            break

        start_time = time.perf_counter()
        sub_run_cfg = dict(run_cfg)
        sub_run_cfg["algorithms"] = [chunk["algorithm"]]
        sub_run_cfg["matrix_ensembles"] = [chunk["ensemble"]]
        sub_run_cfg["joint_sparsity_levels"] = [chunk["l"]]
        sub_run_cfg["delta_grid"] = [chunk["delta"]]

        chunk_rows, chunk_trials = compute_weak_phase_curves(
            run_cfg=sub_run_cfg,
            algorithms_config=algorithms_config,
            experiment_name="weak_phase",
        )

        for row in chunk_rows:
            row_map[_curve_key_from_row(row)] = row
        _write_curve_rows(run_cfg["output_table"], list(row_map.values()))
        _append_trial_rows(run_cfg["output_raw_trials"], chunk_trials)
        trial_count += len(chunk_trials)

        curve_rows = list(row_map.values())
        for ensemble_key, figure_key, title in [
            ("gaussian", "output_figure_gaussian", "Weak Recovery Phase Transitions: Gaussian Matrix Ensemble"),
            ("dct", "output_figure_dct", "Weak Recovery Phase Transitions: DCT Matrix Ensemble"),
        ]:
            subset = [row for row in curve_rows if row["ensemble"] == ensemble_key]
            if subset and figure_key in run_cfg:
                plot_weak_phase_family(subset, run_cfg[figure_key], title=title)

        processed_this_run += 1
        completed_chunks = sum(1 for item in chunk_plan if _chunk_done(item, set(row_map)))
        next_chunk = next((item for item in chunk_plan if not _chunk_done(item, set(row_map))), None)
        _write_progress_report(
            run_cfg=run_cfg,
            curve_rows=curve_rows,
            completed_chunks=completed_chunks,
            total_chunks=len(chunk_plan),
            processed_this_run=processed_this_run,
            next_chunk=next_chunk,
            trial_count=trial_count,
        )
        elapsed = time.perf_counter() - start_time
        print(
            "chunk done:",
            f"profile={profile or 'quick'}",
            f"algorithm={chunk['algorithm']}",
            f"ensemble={chunk['ensemble']}",
            f"l={chunk['l']}",
            f"delta={chunk['delta']}",
            f"elapsed_sec={elapsed:.1f}",
            f"completed={completed_chunks}/{len(chunk_plan)}",
        )

    curve_rows = list(row_map.values())
    completed_chunks = sum(1 for item in chunk_plan if _chunk_done(item, set(row_map)))
    next_chunk = next((item for item in chunk_plan if not _chunk_done(item, set(row_map))), None)
    _write_progress_report(
        run_cfg=run_cfg,
        curve_rows=curve_rows,
        completed_chunks=completed_chunks,
        total_chunks=len(chunk_plan),
        processed_this_run=processed_this_run,
        next_chunk=next_chunk,
        trial_count=trial_count,
    )
    return curve_rows, trial_count, processed_this_run


def main() -> None:
    args = _parse_args()
    config = load_config("configs/weak_phase.yaml")
    run_cfg = resolve_run_config(config, profile=args.profile)
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    chunk_suffix = "" if args.max_chunks is None else f" --max-chunks {args.max_chunks}"

    if run_cfg["profile_name"] == "quick":
        curve_rows, trial_rows = run_weak_phase_experiment(profile=args.profile)
        log_path = write_step_log(
            step_index=6,
            step_name="弱相变实验运行",
            objective="运行 weak phase transition 二分搜索、采样、logistic 拟合并保存曲线和原始 trial",
            changed_files=[
                run_cfg["output_table"],
                run_cfg["output_raw_trials"],
                run_cfg["output_figure_gaussian"],
                run_cfg["output_figure_dct"],
                run_cfg["output_report"],
            ],
            commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_weak_phase.py{profile_suffix}"],
            self_check=f"已生成 {len(curve_rows)} 条弱相变曲线点和 {len(trial_rows)} 条 trial 记录。",
            issues="默认 run 配置使用快速尺度；如果要贴近论文 n=1024 全量实验，请优先调整 configs/weak_phase.yaml。",
            next_step="运行 scripts/run_rank_aware_compare.py 或 scripts/run_all_experiments.py。",
        )
        print(f"weak phase done, curves={len(curve_rows)}, trials={len(trial_rows)}, log={log_path}")
        return

    algorithms_config = load_config("configs/algorithms.yaml")
    curve_rows, trial_count, processed_this_run = _run_incremental_weak_phase(
        run_cfg=run_cfg,
        algorithms_config=algorithms_config,
        profile=args.profile,
        max_chunks=args.max_chunks,
    )
    total_chunks = len(_chunk_plan(run_cfg))
    log_path = write_step_log(
        step_index=6,
        step_name="弱相变实验运行_paper",
        objective="在 paper profile 下逐点分块运行 weak phase 实验，支持中断后续跑",
        changed_files=[
            run_cfg["output_table"],
            run_cfg["output_raw_trials"],
            run_cfg["output_figure_gaussian"],
            run_cfg["output_figure_dct"],
            run_cfg["output_report"],
        ],
        commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_weak_phase.py{profile_suffix}{chunk_suffix}"],
        self_check=f"当前累计 {len(curve_rows)} 条曲线点、{trial_count} 条 trial 记录，本次新增 {processed_this_run} 个 chunk。",
        issues="paper-scale 计算量很大；当前脚本已改成每个 (algorithm, ensemble, l, delta) chunk 落盘一次，后续重跑会自动跳过已完成 chunk。",
        next_step="继续重跑相同命令即可续跑；如需先试速度，可先用 --max-chunks 1 或 2。",
    )
    print(
        "weak phase incremental pass done,",
        f"curves={len(curve_rows)}, trials={trial_count}, processed_this_run={processed_this_run}, total_chunks={total_chunks}, log={log_path}",
    )


if __name__ == "__main__":
    main()
