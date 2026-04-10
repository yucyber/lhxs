"""SIHT and SNIHT implementations for MMV recovery."""

from __future__ import annotations

import numpy as np

from joint_sparse_recovery.algorithms.base import (
    default_late_start,
    finalize_result,
    validate_problem_inputs,
)
from joint_sparse_recovery.core.stopping import ResidualHistory, should_stop
from joint_sparse_recovery.core.support_ops import detect_support, hard_threshold_rows


def _normalized_step_size(
    A: np.ndarray,
    gradient: np.ndarray,
    support: np.ndarray,
    fallback_step: float,
) -> float:
    if support.size == 0:
        return float(fallback_step)
    restricted_grad = np.zeros_like(gradient)
    restricted_grad[support, :] = gradient[support, :]
    numerator = np.linalg.norm(restricted_grad, ord="fro") ** 2
    denominator = np.linalg.norm(A @ restricted_grad, ord="fro") ** 2
    if denominator <= 1e-14 or not np.isfinite(denominator):
        return float(fallback_step)
    return float(numerator / denominator)


def _run_iht_variant(
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
        X_trial = X + step * gradient
        X, support = hard_threshold_rows(X_trial, k)
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
            late_start=default_late_start("thresholding"),
        )
        if stop:
            return finalize_result(X, iteration, residual_norm, stop_reason, history.values, k)

    return finalize_result(X, max_iterations, residual_norm, stop_reason, history.values, k)


def siht(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    omega: float = 0.65,
    max_iterations: int = 5000,
) -> object:
    """Simultaneous IHT with fixed step size."""

    return _run_iht_variant(
        A=A,
        Y=Y,
        k=k,
        omega=omega,
        normalized=False,
        max_iterations=max_iterations,
    )


def sniht(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    fallback_omega: float = 1.0,
    max_iterations: int = 5000,
) -> object:
    """Simultaneous normalized IHT with adaptive step size."""

    return _run_iht_variant(
        A=A,
        Y=Y,
        k=k,
        omega=fallback_omega,
        normalized=True,
        max_iterations=max_iterations,
    )


__all__ = ["siht", "sniht"]
