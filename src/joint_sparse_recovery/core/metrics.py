"""Evaluation metrics for MMV recovery experiments."""

from __future__ import annotations

import numpy as np


def is_exact_recovery(X_hat: np.ndarray, X_true: np.ndarray, tol: float = 1e-3) -> bool:
    """Check the paper's Frobenius-norm success criterion."""

    X_hat = np.asarray(X_hat)
    X_true = np.asarray(X_true)
    if X_hat.shape != X_true.shape:
        raise ValueError(f"shape mismatch: {X_hat.shape} != {X_true.shape}")
    return bool(np.linalg.norm(X_hat - X_true, ord="fro") <= tol)


def nmse(X_hat: np.ndarray, X_true: np.ndarray, eps: float = 1e-12) -> float:
    """Return normalized MSE under Frobenius norm."""

    numerator = np.linalg.norm(np.asarray(X_hat) - np.asarray(X_true), ord="fro") ** 2
    denominator = np.linalg.norm(np.asarray(X_true), ord="fro") ** 2
    return float(numerator / (denominator + eps))


def support_recovery_rate(support_hat: np.ndarray, support_true: np.ndarray) -> float:
    """Return exact support recovery indicator as a float in {0.0, 1.0}."""

    return float(
        np.array_equal(
            np.sort(np.asarray(support_hat, dtype=int)),
            np.sort(np.asarray(support_true, dtype=int)),
        )
    )


def recovery_area_ratio(
    delta_values: np.ndarray,
    rho_values: np.ndarray,
    baseline_delta_values: np.ndarray,
    baseline_rho_values: np.ndarray,
    eps: float = 1e-12,
) -> float:
    """Return the ratio between two phase-transition recovery areas."""

    delta_values = np.asarray(delta_values, dtype=float)
    rho_values = np.asarray(rho_values, dtype=float)
    baseline_delta_values = np.asarray(baseline_delta_values, dtype=float)
    baseline_rho_values = np.asarray(baseline_rho_values, dtype=float)

    order = np.argsort(delta_values)
    base_order = np.argsort(baseline_delta_values)
    area = np.trapezoid(rho_values[order], delta_values[order])
    baseline_area = np.trapezoid(
        baseline_rho_values[base_order],
        baseline_delta_values[base_order],
    )
    return float(area / (baseline_area + eps))


__all__ = [
    "is_exact_recovery",
    "nmse",
    "recovery_area_ratio",
    "support_recovery_rate",
]
