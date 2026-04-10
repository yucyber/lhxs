"""Hybrid RA-SOMP + MUSIC baseline for phase-transition comparison.

This implementation is still a compact approximation of the paper's
rank-aware baseline, but it is closer to the intended workflow than the
previous "run SOMP for k steps, then do a single MUSIC refinement"
version:

1. Estimate the signal subspace rank from Y.
2. Run a rank-aware greedy stage for max(k-rank(Y), 0) support atoms.
3. Complete the support with a MUSIC-style noise-subspace score.
4. Refit X on the final support by least squares.
"""

from __future__ import annotations

import numpy as np

from joint_sparse_recovery.algorithms.base import (
    default_late_start,
    finalize_result,
    validate_problem_inputs,
)
from joint_sparse_recovery.core.projections import least_squares_on_support
from joint_sparse_recovery.core.stopping import ResidualHistory, should_stop


def _safe_rank(matrix: np.ndarray) -> int:
    if np.linalg.norm(matrix, ord="fro") <= 1e-12:
        return 0
    return int(np.linalg.matrix_rank(matrix))


def _signal_basis(matrix: np.ndarray, rank: int | None = None) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("matrix must be 2D")
    if np.linalg.norm(matrix, ord="fro") <= 1e-12:
        return np.zeros((matrix.shape[0], 0), dtype=float)

    max_rank = min(matrix.shape)
    effective_rank = max_rank if rank is None else max(0, min(int(rank), max_rank))
    if effective_rank == 0:
        return np.zeros((matrix.shape[0], 0), dtype=float)

    u_mat, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    numerical_rank = int(np.sum(singular_values > 1e-10))
    keep = numerical_rank if rank is None else min(effective_rank, numerical_rank)
    if keep <= 0:
        return np.zeros((matrix.shape[0], 0), dtype=float)
    return np.asarray(u_mat[:, :keep], dtype=float)


def _rank_aware_scores(A: np.ndarray, residual: np.ndarray, support: np.ndarray) -> np.ndarray:
    """Score atoms by residual signal-subspace alignment."""

    basis = _signal_basis(residual)
    if basis.shape[1] == 0:
        scores = np.linalg.norm(A.T @ residual, axis=1)
    else:
        scores = np.linalg.norm(A.T @ basis, axis=1)
    scores = np.asarray(scores, dtype=float)
    if support.size:
        scores[np.asarray(support, dtype=int)] = -np.inf
    return scores


def _music_complete_support(
    A: np.ndarray,
    Y: np.ndarray,
    partial_support: np.ndarray,
    k: int,
) -> np.ndarray:
    """Complete the support with a MUSIC-style noise-subspace score."""

    partial_support = np.unique(np.asarray(partial_support, dtype=int))
    if k <= 0:
        return np.array([], dtype=int)
    if partial_support.size >= k:
        return np.sort(partial_support[:k])

    signal_rank = max(1, _safe_rank(Y))
    signal_basis = _signal_basis(Y, rank=signal_rank)
    noise_projector = np.eye(A.shape[0]) - signal_basis @ signal_basis.T
    noise_scores = np.linalg.norm(noise_projector @ A, axis=0)
    noise_scores[partial_support] = np.inf

    remaining = int(k - partial_support.size)
    extra_support = np.argsort(noise_scores, kind="mergesort")[:remaining]
    return np.sort(np.union1d(partial_support, extra_support))


def ra_somp_music(
    A: np.ndarray,
    Y: np.ndarray,
    k: int,
    max_iterations: int = 300,
    use_music: bool = True,
) -> object:
    """Run a hybrid rank-aware SOMP stage followed by MUSIC completion."""

    A, Y, k = validate_problem_inputs(A, Y, k)
    n_rows = A.shape[1]
    support = np.array([], dtype=int)
    X = np.zeros((A.shape[1], Y.shape[1]), dtype=float)
    R = Y - A @ X
    y_norm = np.linalg.norm(Y, ord="fro")
    history = ResidualHistory()
    residual_norm = np.linalg.norm(R, ord="fro")

    signal_rank = _safe_rank(Y)
    greedy_target = k if not use_music else max(0, k - signal_rank)
    stop_reason = "music_completion"

    if greedy_target > 0:
        for iteration in range(1, min(max_iterations, greedy_target) + 1):
            scores = _rank_aware_scores(A, R, support)
            if not np.any(np.isfinite(scores)):
                stop_reason = "no_valid_atom"
                break

            new_index = int(np.argmax(scores))
            support = np.sort(np.union1d(support, np.array([new_index], dtype=int)))
            X = least_squares_on_support(A, Y, support, n_rows=n_rows)
            R = Y - A @ X
            residual_norm = np.linalg.norm(R, ord="fro")
            history.append(residual_norm)

            stop, stop_reason = should_stop(
                iteration=iteration,
                residual_norm=residual_norm,
                y_norm=y_norm,
                m=A.shape[0],
                n=A.shape[1],
                max_iterations=min(max_iterations, greedy_target),
                history=history,
                late_start=default_late_start("rank_aware"),
            )
            if support.size >= greedy_target:
                stop_reason = "greedy_stage_complete"
                break
            if stop:
                break

    if use_music and k > 0:
        support = _music_complete_support(A, Y, support, k)
        X = least_squares_on_support(A, Y, support, n_rows=n_rows)
        R = Y - A @ X
        residual_norm = np.linalg.norm(R, ord="fro")
        if stop_reason == "music_completion":
            stop_reason = "music_support_completion"

    return finalize_result(
        X_hat=X,
        n_iter=max(1, len(history.values)),
        residual_norm=residual_norm,
        stop_reason=stop_reason,
        residual_history=history.values,
        k=k,
    )


__all__ = ["ra_somp_music"]
