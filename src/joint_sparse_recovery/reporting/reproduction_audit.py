"""Generate a Markdown audit of current reproduction status."""

from __future__ import annotations

from joint_sparse_recovery.config_utils import (
    ensure_parent_dir,
    load_config,
    resolve_project_path,
    resolve_run_config,
)


def _exists_text(path: str) -> str:
    return "已生成" if resolve_project_path(path).exists() else "未生成"


def _status_line(status: str, task: str, notes: str) -> str:
    return f"| {status} | {task} | {notes} |"


def _weak_phase_scale_note(run_cfg: dict) -> str:
    return (
        f"`n={run_cfg['n']}`，delta 点数 `{len(run_cfg['delta_grid'])}`，"
        f"binary/band trial=`{run_cfg['binary_search_trials']}/{run_cfg['band_trials']}`"
    )


def write_reproduction_audit(profile: str | None = None) -> Path:
    """Write the current reproduction-status audit as Markdown."""

    strong_cfg = resolve_run_config(load_config("configs/strong_phase.yaml"), profile=profile)
    weak_cfg = resolve_run_config(load_config("configs/weak_phase.yaml"), profile=profile)
    step_cfg = resolve_run_config(load_config("configs/step_size_compare.yaml"), profile=profile)
    rank_cfg = resolve_run_config(load_config("configs/rank_aware_compare.yaml"), profile=profile)
    algorithms_cfg = load_config("configs/algorithms.yaml")

    report_path = ensure_parent_dir(
        "outputs/reports/复现状态对照表.md"
        if strong_cfg["profile_name"] == strong_cfg["default_profile"]
        else f"outputs/profiles/{strong_cfg['profile_name']}/reports/复现状态对照表.md"
    )

    strong_status = "近似完成" if strong_cfg["bound_model"] == "surrogate_arip_v1" else "已完成"
    dct_normalized = weak_cfg.get("matrix_options", {}).get("dct", {}).get("normalize_columns", True)
    ra_note = algorithms_cfg["algorithms"]["RA-SOMP+MUSIC"]["paper_reference"]

    lines = [
        "# 复现状态对照表",
        "",
        f"- 审计 profile：`{strong_cfg['profile_name']}`",
        f"- strong phase 输出：`{strong_cfg['output_table']}`（{_exists_text(strong_cfg['output_table'])}）",
        f"- weak phase 输出：`{weak_cfg['output_table']}`（{_exists_text(weak_cfg['output_table'])}）",
        f"- rank-aware 输出：`{rank_cfg['output_table']}`（{_exists_text(rank_cfg['output_table'])}）",
        "",
        "## 任务优先状态",
        "",
        "| 状态 | 任务 | 当前判断 |",
        "| --- | --- | --- |",
        _status_line(
            "P0/" + strong_status,
            "Strong phase exact ARIP 边界",
            "当前仍是 `surrogate_arip_v1`，曲线分辨率可提到 paper 级，但严格 [21] 闭式边界仍缺来源。",
        ),
        _status_line(
            "P0/已就绪",
            "Weak phase paper-scale 运行配置",
            f"已支持 profile 切换；{_weak_phase_scale_note(weak_cfg)}。",
        ),
        _status_line(
            "P0/已就绪",
            "Step-size compare paper-scale 运行配置",
            f"已支持 profile 切换；{_weak_phase_scale_note(step_cfg)}。",
        ),
        _status_line(
            "P0/" + ("近似完成" if "近似" in ra_note or "approx" in ra_note.lower() else "已完成"),
            "RA-SOMP+MUSIC 基线",
            ra_note,
        ),
        _status_line(
            "P1/" + ("已对齐" if not dct_normalized else "待验证"),
            "DCT 生成方式",
            "paper profile 已允许关闭 DCT 列归一化；若图形仍偏离，再核查行采样和归一化细节。",
        ),
        _status_line(
            "P1/待运行",
            "Paper-scale 全量实验结果",
            "profile 已具备，但 full run 尚需实际执行并检查 fit_status / 曲线形状。",
        ),
        "",
        "## 建议执行顺序",
        "",
        "1. 先运行 `paper` profile 的 step-size / weak / rank-aware 实验。",
        "2. 检查 `fit_status` 是否大量落在 fallback；若是，优先调 band/search 参数，不要先改算法。",
        "3. 最后再补 strong phase exact ARIP 公式来源并切换 `bound_model`。",
        "",
        "## 关键提醒",
        "",
        "- 现在最值得先做的是把经验曲线全部切到 `paper` profile 跑一遍，因为这部分最接近可交付复现结果。",
        "- strong phase 是否能称为“严格复现”，取决于 [21] 的 exact L/U 边界，而不是单纯把 delta 采样变密。",
        "- RA-SOMP+MUSIC 已从单次 refine 版升级为 hybrid `k-rank` greedy + MUSIC completion，但还需要文献级核对。",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


__all__ = ["write_reproduction_audit"]
