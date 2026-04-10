"""SCoSaMP implementation for MMV recovery."""

from __future__ import annotations

import numpy as np

from joint_sparse_recovery.algorithms.base import (
    default_late_start,
    finalize_result,
    validate_problem_inputs,
)
from joint_sparse_recovery.core.projections import restricted_cg_projection
from joint_sparse_recovery.core.stopping import ResidualHistory, should_stop
from joint_sparse_recovery.core.support_ops import detect_support, hard_threshold_rows


def scosamp(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    candidate_factor: int = 1,
    max_iterations: int = 300,
) -> object:
    """Simultaneous CoSaMP with row-support detection and pruning."""

    A, Y, k = validate_problem_inputs(A, Y, k)
    n_rows, n_cols = A.shape[1], Y.shape[1]
    X = np.zeros((n_rows, n_cols), dtype=float)
    R = Y - A @ X
    support = np.array([], dtype=int)
    y_norm = np.linalg.norm(Y, ord="fro")
    history = ResidualHistory()

    stop_reason = "max_iterations"
    residual_norm = np.linalg.norm(R, ord="fro")
    for iteration in range(1, max_iterations + 1):
        candidate_count = max(1, int(candidate_factor) * k) if k > 0 else 0
        candidate_support = detect_support(A.T @ R, candidate_count)
        merged_support = np.union1d(support, candidate_support)
        U = restricted_cg_projection(A, Y, merged_support, x0=X, n_rows=n_rows)
        X, support = hard_threshold_rows(U, k)
        support = np.sort(support)
        R = Y - A @ X
        residual_norm = np.linalg.norm(R, ord="fro")
        history.append(residual_norm)
        stop, stop_reason = should_stop(
            iteration=iteration,
            residual_norm=residual_norm,
            y_norm=y_norm,
            m=A.shape[0],
            n=A.shape[1],
            max_iterations=max_iterations,
            history=history,
            late_start=default_late_start("cosamp"),
        )
        if stop:
            return finalize_result(X, iteration, residual_norm, stop_reason, history.values, k)

    return finalize_result(X, max_iterations, residual_norm, stop_reason, history.values, k)


__all__ = ["scosamp"]
