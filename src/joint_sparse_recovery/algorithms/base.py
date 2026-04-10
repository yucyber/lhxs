"""Common result objects and helpers for joint sparse solvers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from joint_sparse_recovery.core.support_ops import detect_support


@dataclass
class SparseRecoveryResult:
    """Unified solver output used by all experiment pipelines."""

    x_hat: np.ndarray
    support_hat: np.ndarray
    n_iter: int
    residual_norm: float
    stop_reason: str
    residual_history: list[float]


def validate_problem_inputs(A: np.ndarray, Y: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Validate solver inputs and return normalized numpy objects."""

    A = np.asarray(A, dtype=float)
    Y = np.asarray(Y, dtype=float)
    k = int(k)
    if A.ndim != 2 or Y.ndim != 2:
        raise ValueError("A and Y must be 2D arrays")
    if A.shape[0] != Y.shape[0]:
        raise ValueError(f"A and Y row mismatch: {A.shape[0]} != {Y.shape[0]}")
    if k < 0 or k > A.shape[1]:
        raise ValueError(f"k must satisfy 0 <= k <= n, got k={k}, n={A.shape[1]}")
    return A, Y, k


def finalize_result(
    X_hat: np.ndarray,
    n_iter: int,
    residual_norm: float,
    stop_reason: str,
    residual_history: list[float],
    k: int,
) -> SparseRecoveryResult:
    """Pack a common solver result."""

    support_hat = np.sort(detect_support(X_hat, k))
    return SparseRecoveryResult(
        x_hat=np.asarray(X_hat, dtype=float),
        support_hat=support_hat,
        n_iter=int(n_iter),
        residual_norm=float(residual_norm),
        stop_reason=str(stop_reason),
        residual_history=[float(v) for v in residual_history],
    )


def default_late_start(algorithm_family: str) -> int:
    """Return the paper's late-rate threshold start iteration by family."""

    if algorithm_family == "thresholding":
        return 700
    return 125


__all__ = [
    "SparseRecoveryResult",
    "default_late_start",
    "finalize_result",
    "validate_problem_inputs",
]
