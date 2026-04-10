"""Support detection and row-thresholding operators for MMV matrices."""

from __future__ import annotations

import numpy as np


def row_l2_norms(matrix: np.ndarray) -> np.ndarray:
    """Return the row-wise Euclidean norms of a 2D matrix.

    Parameters
    ----------
    matrix:
        Array with shape (n, l), where rows correspond to candidate support
        indices and columns correspond to measurement vectors.
    """

    matrix = np.asarray(matrix)
    if matrix.ndim != 2:
        raise ValueError(f"matrix must be 2D, got shape={matrix.shape}")
    return np.linalg.norm(matrix, axis=1)


def detect_support(matrix: np.ndarray, k: int) -> np.ndarray:
    """Select the indices of the k rows with largest row-l2 norms."""

    scores = row_l2_norms(matrix)
    if k <= 0 or scores.size == 0:
        return np.array([], dtype=int)
    if k >= scores.size:
        return np.arange(scores.size, dtype=int)

    support = np.argpartition(scores, -k)[-k:]
    support = support[np.argsort(-scores[support], kind="mergesort")]
    return np.asarray(support, dtype=int)


def hard_threshold_rows(matrix: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Keep the k rows with largest row-l2 norms and zero out the rest."""

    matrix = np.asarray(matrix)
    if matrix.ndim != 2:
        raise ValueError(f"matrix must be 2D, got shape={matrix.shape}")

    support = detect_support(matrix, k)
    thresholded = np.zeros_like(matrix)
    if support.size > 0:
        thresholded[support, :] = matrix[support, :]
    return thresholded, support


__all__ = ["detect_support", "hard_threshold_rows", "row_l2_norms"]
