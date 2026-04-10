from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.config_utils import ensure_parent_dir, load_config, resolve_run_config
from joint_sparse_recovery.experiments.rank_aware_compare import run_rank_aware_comparison
from joint_sparse_recovery.experiments.weak_phase import compute_weak_phase_curves
from joint_sparse_recovery.logging_utils import write_step_log
from joint_sparse_recovery.plotting.phase_transition_plots import plot_rank_aware_compare

FIELDNAMES = ["algorithm", "ensemble", "l", "delta", "m", "k_min", "k_max", "rho_w", "fit_status"]
SKIPPED_FIELDNAMES = ["algorithm", "ensemble", "l", "delta", "reason", "timeout_sec"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the rank-aware comparison experiment.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=None,
        help="For paper-scale runs, process at most this many single-(algorithm,l,delta) chunks.",
    )
    parser.add_argument(
        "--chunk-timeout-sec",
        type=int,
        default=180,
        help="Per-chunk timeout in seconds for paper-scale rank-aware runs.",
    )
    parser.add_argument("--child-algorithm", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--child-ensemble", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--child-l", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--child-delta", type=float, default=None, help=argparse.SUPPRESS)
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
        writer = csv.DictWriter(file_obj, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(sorted_rows)
    return resolved


def _skipped_chunks_path(run_cfg: dict) -> str:
    return run_cfg["output_table"].replace("_curves.csv", "_skipped_chunks.csv")


def _load_skipped_chunks(path: str) -> list[dict]:
    resolved = ensure_parent_dir(path)
    if not resolved.exists():
        return []
    with resolved.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        return [dict(row) for row in reader]


def _write_skipped_chunks(path: str, rows: list[dict]) -> Path:
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
        writer = csv.DictWriter(file_obj, fieldnames=SKIPPED_FIELDNAMES)
        writer.writeheader()
        writer.writerows(sorted_rows)
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


def _chunk_skipped(chunk: dict, skipped_keys: set[tuple[str, str, int, float]]) -> bool:
    return _curve_key_from_values(
        chunk["algorithm"],
        chunk["ensemble"],
        chunk["l"],
        chunk["delta"],
    ) in skipped_keys


def _write_progress_report(
    run_cfg: dict,
    rows: list[dict],
    skipped_rows: list[dict],
    completed_chunks: int,
    total_chunks: int,
    processed_this_run: int,
    next_chunk: dict | None,
) -> Path:
    report_path = ensure_parent_dir(run_cfg["output_report"])
    lines = [
        "# Rank-Aware Comparison",
        "",
        f"- 配置 profile：`{run_cfg['profile_name']}`",
        f"- 曲线表：`{run_cfg['output_table']}`",
        f"- 对照图：`{run_cfg['output_figure']}`",
        f"- 已完成 chunk：`{completed_chunks}/{total_chunks}`",
        f"- 本次运行新增 chunk：`{processed_this_run}`",
        f"- 当前累计曲线点：`{len(rows)}`",
        f"- 当前累计跳过 chunk：`{len(skipped_rows)}`",
        "- 运行模式：paper-scale 下采用逐点分块落盘，可中断后直接重跑续跑。",
        f"- 跳过记录：`{_skipped_chunks_path(run_cfg)}`",
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
    if skipped_rows:
        latest = skipped_rows[-1]
        lines.extend(
            [
                "- 最近一次跳过 chunk：",
                f"  - algorithm=`{latest['algorithm']}`",
                f"  - ensemble=`{latest['ensemble']}`",
                f"  - l=`{latest['l']}`",
                f"  - delta=`{latest['delta']}`",
                f"  - reason=`{latest['reason']}`",
            ]
        )
    lines.extend(
        [
            "- 真实性边界：RA-SOMP+MUSIC 已增强为更接近论文流程的近似实现，但仍需文献级等价核对。",
            "- 保护机制：单 chunk 现在通过子进程执行并带超时，避免前端中断后后台进程长时间失控。",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _run_child_chunk(args: argparse.Namespace) -> None:
    config = load_config("configs/rank_aware_compare.yaml")
    run_cfg = resolve_run_config(config, profile=args.profile)
    algorithms_config = load_config("configs/algorithms.yaml")
    sub_run_cfg = dict(run_cfg)
    sub_run_cfg["algorithms"] = [str(args.child_algorithm)]
    sub_run_cfg["matrix_ensembles"] = [str(args.child_ensemble)]
    sub_run_cfg["joint_sparsity_levels"] = [int(args.child_l)]
    sub_run_cfg["delta_grid"] = [float(args.child_delta)]
    chunk_rows, _ = compute_weak_phase_curves(
        run_cfg=sub_run_cfg,
        algorithms_config=algorithms_config,
        experiment_name="rank_aware_compare",
    )
    print(json.dumps(chunk_rows, ensure_ascii=True))


def _run_chunk_subprocess(chunk: dict, profile: str | None, timeout_sec: int) -> list[dict]:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_rank_aware_compare.py"),
    ]
    if profile:
        command.extend(["--profile", profile])
    command.extend(
        [
            "--child-algorithm",
            str(chunk["algorithm"]),
            "--child-ensemble",
            str(chunk["ensemble"]),
            "--child-l",
            str(chunk["l"]),
            "--child-delta",
            str(chunk["delta"]),
        ]
    )
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout_sec,
        check=True,
    )
    stdout = completed.stdout.strip().splitlines()
    if not stdout:
        raise RuntimeError("child chunk produced no stdout")
    return json.loads(stdout[-1])


def _effective_timeout_sec(chunk: dict, timeout_sec: int) -> int:
    if str(chunk["algorithm"]) == "SCoSaMP":
        return min(int(timeout_sec), 45)
    return int(timeout_sec)


def _run_incremental_rank_aware(
    run_cfg: dict,
    profile: str | None,
    max_chunks: int | None,
    chunk_timeout_sec: int,
) -> tuple[list[dict], int]:
    chunk_plan = _chunk_plan(run_cfg)
    row_map = {_curve_key_from_row(row): row for row in _load_existing_rows(run_cfg["output_table"])}
    skipped_path = _skipped_chunks_path(run_cfg)
    skipped_rows = _load_skipped_chunks(skipped_path)
    skipped_map = {
        _curve_key_from_values(row["algorithm"], row["ensemble"], int(float(row["l"])), float(row["delta"])): row
        for row in skipped_rows
    }
    processed_this_run = 0

    for chunk in chunk_plan:
        if _chunk_done(chunk, set(row_map)):
            continue
        if _chunk_skipped(chunk, set(skipped_map)):
            continue
        if max_chunks is not None and processed_this_run >= max_chunks:
            break

        start_time = time.perf_counter()
        chunk_status = "completed"
        effective_timeout_sec = _effective_timeout_sec(chunk, chunk_timeout_sec)
        try:
            chunk_rows = _run_chunk_subprocess(chunk, profile, timeout_sec=effective_timeout_sec)
            for row in chunk_rows:
                row_map[_curve_key_from_row(row)] = row
            rows = list(row_map.values())
            _write_curve_rows(run_cfg["output_table"], rows)
            plot_rank_aware_compare(rows, run_cfg["output_figure"])
        except subprocess.TimeoutExpired:
            chunk_status = "timeout"
            skipped_row = {
                "algorithm": chunk["algorithm"],
                "ensemble": chunk["ensemble"],
                "l": int(chunk["l"]),
                "delta": float(chunk["delta"]),
                "reason": "timeout",
                "timeout_sec": int(effective_timeout_sec),
            }
            skipped_map[_curve_key_from_values(chunk["algorithm"], chunk["ensemble"], chunk["l"], chunk["delta"])] = skipped_row
            skipped_rows = list(skipped_map.values())
            _write_skipped_chunks(skipped_path, skipped_rows)
            rows = list(row_map.values())
        except subprocess.CalledProcessError as exc:
            chunk_status = "failed"
            skipped_row = {
                "algorithm": chunk["algorithm"],
                "ensemble": chunk["ensemble"],
                "l": int(chunk["l"]),
                "delta": float(chunk["delta"]),
                "reason": f"failed:{exc.returncode}",
                "timeout_sec": int(effective_timeout_sec),
            }
            skipped_map[_curve_key_from_values(chunk["algorithm"], chunk["ensemble"], chunk["l"], chunk["delta"])] = skipped_row
            skipped_rows = list(skipped_map.values())
            _write_skipped_chunks(skipped_path, skipped_rows)
            rows = list(row_map.values())

        processed_this_run += 1
        completed_chunks = sum(1 for item in chunk_plan if _chunk_done(item, set(row_map)) or _chunk_skipped(item, set(skipped_map)))
        next_chunk = next(
            (item for item in chunk_plan if not _chunk_done(item, set(row_map)) and not _chunk_skipped(item, set(skipped_map))),
            None,
        )
        _write_progress_report(
            run_cfg=run_cfg,
            rows=rows,
            skipped_rows=list(skipped_map.values()),
            completed_chunks=completed_chunks,
            total_chunks=len(chunk_plan),
            processed_this_run=processed_this_run,
            next_chunk=next_chunk,
        )
        elapsed = time.perf_counter() - start_time
        verb = "chunk done:" if chunk_status == "completed" else "chunk skipped:"
        print(
            verb,
            f"profile={profile or 'quick'}",
            f"algorithm={chunk['algorithm']}",
            f"ensemble={chunk['ensemble']}",
            f"l={chunk['l']}",
            f"delta={chunk['delta']}",
            f"status={chunk_status}",
            f"elapsed_sec={elapsed:.1f}",
            f"completed={completed_chunks}/{len(chunk_plan)}",
        )

    rows = list(row_map.values())
    skipped_rows = list(skipped_map.values())
    completed_chunks = sum(1 for item in chunk_plan if _chunk_done(item, set(row_map)) or _chunk_skipped(item, set(skipped_map)))
    next_chunk = next(
        (item for item in chunk_plan if not _chunk_done(item, set(row_map)) and not _chunk_skipped(item, set(skipped_map))),
        None,
    )
    _write_progress_report(
        run_cfg=run_cfg,
        rows=rows,
        skipped_rows=skipped_rows,
        completed_chunks=completed_chunks,
        total_chunks=len(chunk_plan),
        processed_this_run=processed_this_run,
        next_chunk=next_chunk,
    )
    return rows, processed_this_run


def main() -> None:
    args = _parse_args()
    if args.child_algorithm is not None:
        _run_child_chunk(args)
        return

    config = load_config("configs/rank_aware_compare.yaml")
    run_cfg = resolve_run_config(config, profile=args.profile)
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    chunk_suffix = "" if args.max_chunks is None else f" --max-chunks {args.max_chunks}"
    timeout_suffix = f" --chunk-timeout-sec {args.chunk_timeout_sec}"

    if run_cfg["profile_name"] == "quick":
        rows = run_rank_aware_comparison(profile=args.profile)
        log_path = write_step_log(
            step_index=7,
            step_name="RankAware对照实验运行",
            objective="运行 SNIHT/SNHTP/SCoSaMP 与 RA-SOMP+MUSIC 的 weak phase transition 对照实验",
            changed_files=[run_cfg["output_table"], run_cfg["output_figure"], run_cfg["output_report"]],
            commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_rank_aware_compare.py{profile_suffix}"],
            self_check=f"已生成 {len(rows)} 条 rank-aware 对照曲线点。",
            issues="RA-SOMP+MUSIC 当前是紧凑近似实现，如果对照曲线反常，优先回查该模块。",
            next_step="运行 scripts/run_all_experiments.py 汇总全部实验。",
        )
        print(f"rank-aware comparison done, rows={len(rows)}, log={log_path}")
        return

    rows, processed_this_run = _run_incremental_rank_aware(
        run_cfg=run_cfg,
        profile=args.profile,
        max_chunks=args.max_chunks,
        chunk_timeout_sec=args.chunk_timeout_sec,
    )
    total_chunks = len(_chunk_plan(run_cfg))
    log_path = write_step_log(
        step_index=7,
        step_name="RankAware对照实验运行_paper",
        objective="在 paper profile 下逐点分块运行 rank-aware 对照实验，支持中断后续跑",
        changed_files=[run_cfg["output_table"], run_cfg["output_figure"], run_cfg["output_report"], _skipped_chunks_path(run_cfg)],
        commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_rank_aware_compare.py{profile_suffix}{chunk_suffix}{timeout_suffix}"],
        self_check=f"当前累计 {len(rows)} 条曲线点，本次新增 {processed_this_run} 个 chunk。",
        issues="paper-scale 计算量很大；当前脚本已改成每个 chunk 子进程执行并带超时，超时或失败的 chunk 会写入 skipped_chunks.csv 并在后续续跑时自动跳过。",
        next_step="继续重跑相同命令即可续跑；如需重试跳过点，可先手工清理 skipped_chunks.csv 中对应记录。",
    )
    print(
        "rank-aware incremental pass done,",
        f"rows={len(rows)}, processed_this_run={processed_this_run}, total_chunks={total_chunks}, log={log_path}",
    )


if __name__ == "__main__":
    main()
