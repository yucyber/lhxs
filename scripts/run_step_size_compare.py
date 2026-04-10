from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.experiments.step_size_compare import run_step_size_comparison
from joint_sparse_recovery.experiments.weak_phase import compute_weak_phase_curves
from joint_sparse_recovery.logging_utils import write_step_log
from joint_sparse_recovery.plotting.phase_transition_plots import plot_step_size_compare

FIELDNAMES = ["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the step-size comparison experiment.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=None,
        help="For paper-scale runs, process at most this many delta chunks in one invocation.",
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


def _load_existing_curve_rows(path: str) -> list[dict]:
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
        writer = csv.DictWriter(file_obj, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(sorted_rows)
    return resolved


def _chunk_plan(run_cfg: dict) -> list[dict]:
    chunks: list[dict] = []
    for pair in run_cfg["algorithm_pairs"]:
        pair_list = [str(name) for name in pair]
        pair_label = "_vs_".join(pair_list)
        for ensemble in run_cfg["matrix_ensembles"]:
            for l_value in run_cfg["joint_sparsity_levels"]:
                for delta in run_cfg["delta_grid"]:
                    chunks.append(
                        {
                            "pair": pair_list,
                            "pair_label": pair_label,
                            "ensemble": str(ensemble),
                            "l": int(l_value),
                            "delta": float(delta),
                        }
                    )
    return chunks


def _chunk_done(chunk: dict, existing_keys: set[tuple[str, str, int, float]]) -> bool:
    return all(
        _curve_key_from_values(name, chunk["ensemble"], chunk["l"], chunk["delta"]) in existing_keys
        for name in chunk["pair"]
    )


def _write_progress_report(
    run_cfg: dict,
    curve_rows: list[dict],
    completed_chunks: int,
    total_chunks: int,
    processed_this_run: int,
    next_chunk: dict | None,
) -> Path:
    report_path = ensure_parent_dir(run_cfg["output_report"])
    lines = [
        "# Fixed Step Size vs Normalized Step Size",
        "",
        f"- 配置 profile：`{run_cfg['profile_name']}`",
        f"- 曲线表：`{run_cfg['output_table']}`",
        f"- 对照图：`{run_cfg['output_figure']}`",
        f"- 已完成 chunk：`{completed_chunks}/{total_chunks}`",
        f"- 本次运行新增 chunk：`{processed_this_run}`",
        f"- 当前累计曲线点：`{len(curve_rows)}`",
        "- 解读提示：同一 `ensemble/l` 下，比较 SIHT vs SNIHT、SHTP vs SNHTP 的 `rho_w(delta)` 曲线高低。",
        "- 运行模式：paper-scale 下采用逐 delta 分块落盘，可中断后直接重跑续跑。",
    ]
    if next_chunk is not None:
        lines.extend(
            [
                "- 下一个待跑 chunk：",
                f"  - pair=`{next_chunk['pair_label']}`",
                f"  - ensemble=`{next_chunk['ensemble']}`",
                f"  - l=`{next_chunk['l']}`",
                f"  - delta=`{next_chunk['delta']}`",
            ]
        )
    else:
        lines.append("- 当前所有 chunk 已完成。")
    lines.extend(
        [
            "- 真实性边界：当前默认 run 配置是快速实验尺度；`paper` profile 更接近论文规模，但 strong phase exact ARIP 公式仍需单独补齐。",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _run_incremental_step_size(
    run_cfg: dict,
    algorithms_config: dict,
    profile: str | None,
    max_chunks: int | None,
) -> tuple[list[dict], int, int]:
    chunk_plan = _chunk_plan(run_cfg)
    row_map = {_curve_key_from_row(row): row for row in _load_existing_curve_rows(run_cfg["output_table"])}
    processed_this_run = 0

    for chunk in chunk_plan:
        if _chunk_done(chunk, set(row_map)):
            continue

        if max_chunks is not None and processed_this_run >= max_chunks:
            break

        start_time = time.perf_counter()
        sub_run_cfg = dict(run_cfg)
        sub_run_cfg["algorithms"] = list(chunk["pair"])
        sub_run_cfg["matrix_ensembles"] = [chunk["ensemble"]]
        sub_run_cfg["joint_sparsity_levels"] = [chunk["l"]]
        sub_run_cfg["delta_grid"] = [chunk["delta"]]
        sub_run_cfg["output_table"] = run_cfg["output_table"]
        sub_run_cfg["output_figure"] = run_cfg["output_figure"]

        chunk_rows, _ = compute_weak_phase_curves(
            run_cfg=sub_run_cfg,
            algorithms_config=algorithms_config,
            experiment_name=f"step_size_compare:{chunk['pair_label']}",
        )

        for row in chunk_rows:
            row_map[_curve_key_from_row(row)] = row

        curve_rows = list(row_map.values())
        _write_curve_rows(run_cfg["output_table"], curve_rows)
        plot_step_size_compare(curve_rows, run_cfg["output_figure"])

        processed_this_run += 1
        elapsed = time.perf_counter() - start_time
        next_chunk = next((item for item in chunk_plan if not _chunk_done(item, set(row_map))), None)
        completed_chunks = sum(1 for item in chunk_plan if _chunk_done(item, set(row_map)))
        _write_progress_report(
            run_cfg=run_cfg,
            curve_rows=curve_rows,
            completed_chunks=completed_chunks,
            total_chunks=len(chunk_plan),
            processed_this_run=processed_this_run,
            next_chunk=next_chunk,
        )
        print(
            "chunk done:",
            f"profile={profile or 'quick'}",
            f"pair={chunk['pair_label']}",
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
    )
    return curve_rows, processed_this_run, len(chunk_plan)


def main() -> None:
    args = _parse_args()
    config = load_config("configs/step_size_compare.yaml")
    run_cfg = resolve_run_config(config, profile=args.profile)
    algorithms_config = load_config("configs/algorithms.yaml")
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    chunk_suffix = "" if args.max_chunks is None else f" --max-chunks {args.max_chunks}"

    if run_cfg["profile_name"] == "quick":
        rows = run_step_size_comparison(profile=args.profile)
        log_path = write_step_log(
            step_index=7,
            step_name="步长对照实验运行",
            objective="运行 SIHT vs SNIHT 和 SHTP vs SNHTP 的 weak phase transition 对照实验",
            changed_files=[run_cfg["output_table"], run_cfg["output_figure"], run_cfg["output_report"]],
            commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_step_size_compare.py{profile_suffix}"],
            self_check=f"已生成 {len(rows)} 条步长对照曲线点。",
            issues="默认 run 配置为快速实验尺度，适合先检查趋势。",
            next_step="运行 scripts/run_weak_phase.py 或 scripts/run_all_experiments.py。",
        )
        print(f"step size comparison done, rows={len(rows)}, log={log_path}")
        return

    rows, processed_this_run, total_chunks = _run_incremental_step_size(
        run_cfg=run_cfg,
        algorithms_config=algorithms_config,
        profile=args.profile,
        max_chunks=args.max_chunks,
    )
    completed_chunks = len(rows) // 2
    log_path = write_step_log(
        step_index=7,
        step_name="步长对照实验运行_paper",
        objective="在 paper profile 下逐 delta 分块运行步长对照实验，支持中断后续跑",
        changed_files=[run_cfg["output_table"], run_cfg["output_figure"], run_cfg["output_report"]],
        commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_step_size_compare.py{profile_suffix}{chunk_suffix}"],
        self_check=f"当前累计 {len(rows)} 条曲线点，完成 {completed_chunks}/{total_chunks} 个 chunk，本次新增 {processed_this_run} 个 chunk。",
        issues="paper-scale 计算量很大；当前脚本已改成每个 delta 落盘一次，后续重跑会自动跳过已完成 chunk。",
        next_step="继续重跑相同命令即可续跑；如需先试速度，可先用 --max-chunks 1 或 2。",
    )
    print(
        "step size comparison incremental pass done,",
        f"rows={len(rows)}, processed_this_run={processed_this_run}, total_chunks={total_chunks}, log={log_path}",
    )


if __name__ == "__main__":
    main()
