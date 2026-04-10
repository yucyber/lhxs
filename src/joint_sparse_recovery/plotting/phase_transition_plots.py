"""Plot helpers for strong/weak phase-transition figures."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from joint_sparse_recovery.config_utils import ensure_parent_dir


def _group_by(rows: list[dict], keys: tuple[str, ...]) -> dict[tuple, list[dict]]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def _sorted_group_items(rows: list[dict], keys: tuple[str, ...]) -> list[tuple[tuple, list[dict]]]:
    grouped = _group_by(rows, keys)
    return sorted(grouped.items(), key=lambda item: tuple(str(value) for value in item[0]))


def _sorted_xy(rows: list[dict], x_key: str, y_key: str) -> tuple[np.ndarray, np.ndarray]:
    sorted_rows = sorted(rows, key=lambda row: row[x_key])
    x = np.array([float(row[x_key]) for row in sorted_rows], dtype=float)
    y = np.array([float(row[y_key]) for row in sorted_rows], dtype=float)
    return x, y


def plot_strong_phase(rows: list[dict], output_path: str | Path) -> Path:
    """Plot one Fig.1-style strong phase-transition figure."""

    output_file = ensure_parent_dir(output_path)
    plt.figure(figsize=(8, 6))
    for (algorithm,), group_rows in _sorted_group_items(rows, ("algorithm",)):
        delta, rho = _sorted_xy(group_rows, "delta", "rho")
        plt.plot(delta, rho, marker="o", linewidth=2, markersize=4, label=algorithm)
    plt.xlabel(r"$\delta=m/n$")
    plt.ylabel(r"$\rho=k/m$")
    plt.title("Strong Recovery Phase Transitions: surrogate $\\mu_{alg}(\\delta,\\rho)=1$")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=180)
    plt.close()
    return output_file


def plot_weak_phase_family(
    rows: list[dict],
    output_path: str | Path,
    title: str,
    group_keys: tuple[str, ...] = ("algorithm", "l"),
) -> Path:
    """Plot weak phase-transition curves grouped by algorithm and sparsity level."""

    output_file = ensure_parent_dir(output_path)
    plt.figure(figsize=(8, 6))
    for key_tuple, group_rows in _sorted_group_items(rows, group_keys):
        delta, rho = _sorted_xy(group_rows, "delta", "rho_w")
        label = ", ".join(f"{key}={value}" for key, value in zip(group_keys, key_tuple, strict=True))
        plt.plot(delta, rho, marker="o", linewidth=2, markersize=4, label=label)
    plt.xlabel(r"$\delta=m/n$")
    plt.ylabel(r"$\rho=k/m$")
    plt.title(title)
    plt.ylim(bottom=0.0)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_file, dpi=180)
    plt.close()
    return output_file


def plot_step_size_compare(rows: list[dict], output_path: str | Path) -> Path:
    """Plot fixed-step and normalized-step comparisons."""

    return plot_weak_phase_family(
        rows=rows,
        output_path=output_path,
        title="Fixed Step Size vs Normalized Step Size",
        group_keys=("ensemble", "algorithm", "l"),
    )


def plot_rank_aware_compare(rows: list[dict], output_path: str | Path) -> Path:
    """Plot SNIHT/SNHTP/SCoSaMP versus RA-SOMP+MUSIC."""

    return plot_weak_phase_family(
        rows=rows,
        output_path=output_path,
        title="Weak Recovery Phase Transitions: Rank-Aware Comparison",
        group_keys=("algorithm", "l"),
    )


__all__ = [
    "plot_rank_aware_compare",
    "plot_step_size_compare",
    "plot_strong_phase",
    "plot_weak_phase_family",
]
