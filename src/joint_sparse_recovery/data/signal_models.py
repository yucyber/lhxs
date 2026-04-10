"""Row-sparse MMV signal generators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from joint_sparse_recovery.data.matrix_ensembles import (
    dct_subsample_matrix,
    gaussian_matrix,
)


@dataclass
class JointSparseProblem:
    """One synthetic MMV problem instance Y = A X_true."""

    A: np.ndarray
    X_true: np.ndarray
    Y: np.ndarray
    support_true: np.ndarray


def sample_row_support(
    n: int,
    k: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Sample a random row support T with |T| = k."""

    if n <= 0:
        raise ValueError("n must be positive")
    if k < 0 or k > n:
        raise ValueError(f"k must satisfy 0 <= k <= n, got k={k}, n={n}")
    rng = np.random.default_rng() if rng is None else rng
    if k == 0:
        return np.array([], dtype=int)
    return np.sort(rng.choice(n, size=k, replace=False)).astype(int)


def sample_joint_sparse_matrix(
    n: int,
    l: int,
    support: np.ndarray | list[int] | tuple[int, ...],
    rng: np.random.Generator | None = None,
    value_ensemble: str = "rademacher",
) -> np.ndarray:
    """Generate X in R^{n x l} with nonzeros only on a given row support."""

    if n <= 0 or l <= 0:
        raise ValueError("n and l must be positive")
    support_array = np.asarray(support, dtype=int)
    if support_array.size and (support_array.min() < 0 or support_array.max() >= n):
        raise ValueError("support contains out-of-range indices")

    rng = np.random.default_rng() if rng is None else rng
    X = np.zeros((n, l), dtype=float)
    if support_array.size == 0:
        return X

    if value_ensemble == "rademacher":
        values = rng.choice(np.array([-1.0, 1.0]), size=(support_array.size, l), replace=True)
    elif value_ensemble == "gaussian":
        values = rng.normal(loc=0.0, scale=1.0, size=(support_array.size, l))
    else:
        raise ValueError(f"unsupported value_ensemble={value_ensemble}")
    X[support_array, :] = values
    return X


def sample_problem_instance(
    m: int,
    n: int,
    k: int,
    l: int,
    matrix_ensemble: str,
    rng: np.random.Generator | None = None,
    value_ensemble: str = "rademacher",
    matrix_options: dict | None = None,
) -> JointSparseProblem:
    """Sample a synthetic joint sparse recovery problem."""

    rng = np.random.default_rng() if rng is None else rng
    ensemble_key = matrix_ensemble.lower()
    matrix_options = {} if matrix_options is None else dict(matrix_options)
    if ensemble_key == "gaussian":
        A = gaussian_matrix(m, n, rng=rng)
    elif ensemble_key == "dct":
        A = dct_subsample_matrix(
            m,
            n,
            rng=rng,
            normalize=bool(matrix_options.get("normalize_columns", True)),
        )
    else:
        raise ValueError(f"unsupported matrix_ensemble={matrix_ensemble}")

    support_true = sample_row_support(n, k, rng=rng)
    X_true = sample_joint_sparse_matrix(
        n=n,
        l=l,
        support=support_true,
        rng=rng,
        value_ensemble=value_ensemble,
    )
    Y = A @ X_true
    return JointSparseProblem(A=A, X_true=X_true, Y=Y, support_true=support_true)


__all__ = [
    "JointSparseProblem",
    "sample_joint_sparse_matrix",
    "sample_problem_instance",
    "sample_row_support",
]
