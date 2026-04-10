"""Projection operators on a fixed row support."""

from __future__ import annotations

import numpy as np
from scipy.sparse.linalg import cg


def _normalize_support(support: np.ndarray | list[int] | tuple[int, ...]) -> np.ndarray:
    support_array = np.asarray(support, dtype=int)
    if support_array.size == 0:
        return np.array([], dtype=int)
    return np.unique(np.sort(support_array))


def least_squares_on_support(
    A: np.ndarray,
    Y: np.ndarray,
    support: np.ndarray | list[int] | tuple[int, ...],
    n_rows: int | None = None,
) -> np.ndarray:
    """Solve min ||Y - AZ||_F subject to supp(Z) subset of support."""

    A = np.asarray(A)
    Y = np.asarray(Y)
    if A.ndim != 2 or Y.ndim != 2:
        raise ValueError("A and Y must both be 2D arrays")
    if A.shape[0] != Y.shape[0]:
        raise ValueError(f"A and Y row mismatch: {A.shape[0]} != {Y.shape[0]}")

    n_total = A.shape[1] if n_rows is None else int(n_rows)
    if n_total < A.shape[1]:
        raise ValueError("n_rows cannot be smaller than A.shape[1]")

    support_array = _normalize_support(support)
    X_hat = np.zeros((n_total, Y.shape[1]), dtype=np.result_type(A, Y, np.float64))
    if support_array.size == 0:
        return X_hat

    A_support = A[:, support_array]
    X_support, *_ = np.linalg.lstsq(A_support, Y, rcond=None)
    X_hat[support_array, :] = X_support
    return X_hat


def restricted_cg_projection(
    A: np.ndarray,
    Y: np.ndarray,
    support: np.ndarray | list[int] | tuple[int, ...],
    x0: np.ndarray | None = None,
    max_iter: int | None = None,
    tol: float | None = None,
    n_rows: int | None = None,
) -> np.ndarray:
    """Approximate the support-restricted least-squares projection with CG.

    If CG does not converge for one column, fall back to a dense least-squares
    solve on the same support.
    """

    A = np.asarray(A)
    Y = np.asarray(Y)
    support_array = _normalize_support(support)
    n_total = A.shape[1] if n_rows is None else int(n_rows)
    X_hat = np.zeros((n_total, Y.shape[1]), dtype=np.result_type(A, Y, np.float64))
    if support_array.size == 0:
        return X_hat

    A_support = A[:, support_array]
    gram = A_support.T @ A_support
    rhs = A_support.T @ Y
    cg_rtol = 1e-8 if tol is None else float(tol)
    cg_maxiter = max(20, 4 * support_array.size) if max_iter is None else int(max_iter)

    x0_support = None
    if x0 is not None:
        x0 = np.asarray(x0)
        if x0.shape[0] >= n_total:
            x0_support = x0[support_array, :]

    solved = np.zeros((support_array.size, Y.shape[1]), dtype=X_hat.dtype)
    for col_idx in range(Y.shape[1]):
        guess = None if x0_support is None else x0_support[:, col_idx]
        try:
            col_solution, info = cg(
                gram,
                rhs[:, col_idx],
                x0=guess,
                maxiter=cg_maxiter,
                rtol=cg_rtol,
                atol=0.0,
            )
        except TypeError:
            col_solution, info = cg(
                gram,
                rhs[:, col_idx],
                x0=guess,
                maxiter=cg_maxiter,
                tol=cg_rtol,
            )

        if info != 0 or not np.all(np.isfinite(col_solution)):
            col_solution, *_ = np.linalg.lstsq(A_support, Y[:, col_idx], rcond=None)
        solved[:, col_idx] = col_solution

    X_hat[support_array, :] = solved
    return X_hat


__all__ = ["least_squares_on_support", "restricted_cg_projection"]
