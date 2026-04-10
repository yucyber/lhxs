"""Strong phase-transition curve solver."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from joint_sparse_recovery.theory.arip_bounds import MU_MODELS


def solve_strong_transition_rho(
    delta: float,
    mu_function: Callable[[float, float], float],
    rho_upper: float = 0.5,
    max_iter: int = 80,
    tol: float = 1e-8,
) -> tuple[float, float]:
    """Solve mu(delta, rho)=1 by bisection on rho."""

    lo = 0.0
    hi = float(rho_upper)
    mu_lo = float(mu_function(delta, lo))
    mu_hi = float(mu_function(delta, hi))

    if not np.isfinite(mu_lo):
        return 0.0, float("nan")
    if mu_lo >= 1.0:
        return 0.0, mu_lo
    if np.isfinite(mu_hi) and mu_hi <= 1.0:
        return hi, mu_hi

    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        mu_mid = float(mu_function(delta, mid))
        if not np.isfinite(mu_mid):
            hi = mid
            continue
        if mu_mid <= 1.0:
            lo = mid
            mu_lo = mu_mid
        else:
            hi = mid
        if hi - lo <= tol:
            break

    return float(lo), float(mu_lo)


def solve_strong_transition_curve(
    algorithm: str,
    delta_grid: list[float] | np.ndarray,
    rho_upper: float = 0.5,
    bound_model: str = "surrogate_arip_v1",
) -> list[dict[str, float | str]]:
    """Compute rho_S(delta) for one algorithm on a delta grid."""

    if bound_model not in MU_MODELS:
        raise ValueError(f"unsupported bound_model={bound_model}")
    mu_functions = MU_MODELS[bound_model]
    if algorithm not in mu_functions:
        raise ValueError(f"unsupported algorithm={algorithm}")
    mu_function = mu_functions[algorithm]

    rows: list[dict[str, float | str]] = []
    for delta in np.asarray(delta_grid, dtype=float):
        rho_s, mu_value = solve_strong_transition_rho(
            delta=float(delta),
            mu_function=mu_function,
            rho_upper=rho_upper,
        )
        rows.append(
            {
                "algorithm": algorithm,
                "bound_model": bound_model,
                "delta": float(delta),
                "rho": float(rho_s),
                "mu_at_rho": float(mu_value),
            }
        )
    return rows


__all__ = ["solve_strong_transition_curve", "solve_strong_transition_rho"]
