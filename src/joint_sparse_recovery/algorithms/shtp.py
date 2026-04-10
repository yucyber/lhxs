"""SHTP and SNHTP implementations for MMV recovery."""

from __future__ import annotations

import numpy as np

from joint_sparse_recovery.algorithms.base import (
    default_late_start,
    finalize_result,
    validate_problem_inputs,
)
from joint_sparse_recovery.algorithms.siht import _normalized_step_size
from joint_sparse_recovery.core.projections import restricted_cg_projection
from joint_sparse_recovery.core.stopping import ResidualHistory, should_stop
from joint_sparse_recovery.core.support_ops import detect_support


def _run_htp_variant(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    omega: float,
    normalized: bool,
    max_iterations: int,
) -> object:
    A, Y, k = validate_problem_inputs(A, Y, k)
    n_rows, n_cols = A.shape[1], Y.shape[1]
    X = np.zeros((n_rows, n_cols), dtype=float)
    R = Y - A @ X
    y_norm = np.linalg.norm(Y, ord="fro")
    support = np.sort(detect_support(A.T @ R, k))
    history = ResidualHistory()

    stop_reason = "max_iterations"
    residual_norm = np.linalg.norm(R, ord="fro")
    for iteration in range(1, max_iterations + 1):
        gradient = A.T @ R
        step = _normalized_step_size(A, gradient, support, omega) if normalized else float(omega)
        proxy = X + step * gradient
        support = np.sort(detect_support(proxy, k))
        X = restricted_cg_projection(A, Y, support, x0=X, n_rows=n_rows)
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
            late_start=default_late_start("pursuit"),
        )
        if stop:
            return finalize_result(X, iteration, residual_norm, stop_reason, history.values, k)

    return finalize_result(X, max_iterations, residual_norm, stop_reason, history.values, k)


def shtp(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    omega: float = 1.0,
    max_iterations: int = 300,
) -> object:
    """Simultaneous HTP with fixed step size."""

    return _run_htp_variant(
        A=A,
        Y=Y,
        k=k,
        omega=omega,
        normalized=False,
        max_iterations=max_iterations,
    )


def snhtp(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    fallback_omega: float = 1.0,
    max_iterations: int = 300,
) -> object:
    """Simultaneous normalized HTP with adaptive step size."""

    return _run_htp_variant(
        A=A,
        Y=Y,
        k=k,
        omega=fallback_omega,
        normalized=True,
        max_iterations=max_iterations,
    )


__all__ = ["shtp", "snhtp"]
