"""Measurement matrix generators for Gaussian and DCT ensembles."""

from __future__ import annotations

import numpy as np
from scipy.fft import dct


def normalize_columns(A: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Normalize each column to unit Euclidean norm."""

    A = np.asarray(A, dtype=float)
    if A.ndim != 2:
        raise ValueError(f"A must be 2D, got shape={A.shape}")
    norms = np.linalg.norm(A, axis=0)
    norms = np.maximum(norms, eps)
    return A / norms


def gaussian_matrix(
    m: int,
    n: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Draw A with iid N(0, 1/m) entries, matching the paper's Gaussian ensemble."""

    if m <= 0 or n <= 0:
        raise ValueError("m and n must be positive")
    rng = np.random.default_rng() if rng is None else rng
    return rng.normal(loc=0.0, scale=1.0 / np.sqrt(m), size=(m, n))


def dct_subsample_matrix(
    m: int,
    n: int,
    rng: np.random.Generator | None = None,
    normalize: bool = True,
) -> np.ndarray:
    """Sample m rows from the n x n orthonormal DCT matrix.

    The target paper defines the DCT ensemble as random row subsampling of
    an n x n DCT matrix. We additionally apply column normalization by
    default to keep fixed-step methods numerically stable in this Python
    implementation.
    """

    if m <= 0 or n <= 0:
        raise ValueError("m and n must be positive")
    if m > n:
        raise ValueError(f"m cannot exceed n for row subsampling: m={m}, n={n}")

    rng = np.random.default_rng() if rng is None else rng
    full_dct = dct(np.eye(n), norm="ortho", axis=0)
    row_indices = np.sort(rng.choice(n, size=m, replace=False))
    A = np.asarray(full_dct[row_indices, :], dtype=float)
    if normalize:
        A = normalize_columns(A)
    return A


__all__ = ["dct_subsample_matrix", "gaussian_matrix", "normalize_columns"]
