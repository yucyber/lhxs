from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.config_utils import load_config, resolve_run_config
from joint_sparse_recovery.experiments.strong_phase import run_strong_phase_experiment
from joint_sparse_recovery.logging_utils import write_step_log


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the strong phase experiment.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    run_cfg = resolve_run_config(load_config("configs/strong_phase.yaml"), profile=args.profile)
    rows = run_strong_phase_experiment(profile=args.profile)
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    log_path = write_step_log(
        step_index=5,
        step_name="强相变实验运行",
        objective="运行 strong phase transition 理论曲线计算并保存 Fig.1 风格输出",
        changed_files=[run_cfg["output_table"], run_cfg["output_figure"]],
        commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_strong_phase.py{profile_suffix}"],
        self_check=f"已生成 {len(rows)} 条强相变曲线采样点。",
        issues="当前强相变曲线基于 surrogate ARIP 边界模型，不等同于原论文 [21] 严格闭式边界。",
        next_step="运行 scripts/run_step_size_compare.py 或 scripts/run_all_experiments.py。",
    )
    print(f"strong phase done, rows={len(rows)}, log={log_path}")


if __name__ == "__main__":
    main()
