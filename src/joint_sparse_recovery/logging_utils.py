"""Utilities for writing Chinese step logs during workflow execution."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = PROJECT_ROOT / "日志"


def _format_bullets(items: Sequence[str]) -> str:
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def write_step_log(
    step_index: int,
    step_name: str,
    objective: str,
    changed_files: Sequence[str],
    commands: Sequence[str],
    self_check: str,
    issues: str,
    next_step: str,
    log_dir: str | Path | None = None,
    timestamp: datetime | None = None,
) -> Path:
    """Create one Markdown log file under 日志/ for a finished workflow step."""

    resolved_log_dir = Path(log_dir) if log_dir is not None else DEFAULT_LOG_DIR
    resolved_log_dir.mkdir(parents=True, exist_ok=True)

    current_time = timestamp or datetime.now()
    stamp = current_time.strftime("%Y%m%d_%H%M")
    safe_step_name = step_name.strip().replace(" ", "_")
    log_path = resolved_log_dir / f"步骤{step_index:02d}_{stamp}_{safe_step_name}.md"

    content = "\n".join(
        [
            f"# 步骤{step_index:02d}：{step_name}",
            "",
            f"- 时间：{current_time.strftime('%Y-%m-%d %H:%M')}",
            f"- 本步骤目标：{objective}",
            "- 本步骤新增/修改文件：",
            _format_bullets(changed_files),
            "- 本步骤执行的命令：",
            _format_bullets(commands),
            f"- 自检结果：{self_check}",
            f"- 遇到的问题与判断：{issues}",
            f"- 下一步建议：{next_step}",
            "",
        ]
    )
    log_path.write_text(content, encoding="utf-8")
    return log_path


def append_step_log(log_path: str | Path, section_title: str, content: str) -> Path:
    """Append one extra section to an existing Markdown step log."""

    resolved_log_path = Path(log_path)
    with resolved_log_path.open("a", encoding="utf-8", newline="\n") as file_obj:
        file_obj.write(f"\n## {section_title}\n\n{content.rstrip()}\n")
    return resolved_log_path


__all__ = ["append_step_log", "write_step_log"]
