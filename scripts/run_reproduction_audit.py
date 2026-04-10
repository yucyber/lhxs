from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from joint_sparse_recovery.logging_utils import write_step_log
from joint_sparse_recovery.reporting import write_reproduction_audit


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a reproduction audit report.")
    parser.add_argument("--profile", default=None, help="Config profile override, e.g. quick or paper.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    audit_path = write_reproduction_audit(profile=args.profile)
    profile_suffix = "" if not args.profile else f" --profile {args.profile}"
    log_path = write_step_log(
        step_index=10,
        step_name="复现状态审计",
        objective="生成当前完整复现进度、近似项和阻塞项的对照表",
        changed_files=[str(audit_path)],
        commands=[f".\\.venv\\Scripts\\python.exe scripts\\run_reproduction_audit.py{profile_suffix}"],
        self_check=f"复现状态审计已生成：{audit_path}",
        issues="该审计会如实区分‘严格复现’、‘近似完成’和‘待运行/待补齐’；不会把 surrogate/approx 伪装成完整复现。",
        next_step="根据审计表优先跑 paper profile 的 weak/step-size/rank-aware 实验，再继续补 strong phase exact ARIP。",
    )
    print(f"reproduction audit done, audit={audit_path}, log={log_path}")


if __name__ == "__main__":
    main()
