"""Surrogate ARIP bounds and convergence-factor formulas.

The target paper defines strong phase-transition curves through
mu_alg(delta, rho)=1, with mu_alg built from Gaussian ARIP bounds
L(delta, rho), U(delta, rho) from Blanchard-Cartis-Tanner [21].

The clean markdown in this workspace does not include the closed-form
expressions of those [21] bounds. To keep the experiment pipeline
executable, this module implements a conservative surrogate model with
the same monotonic structure and the exact mu-formulas from Definition 3
of the target paper.
"""

from __future__ import annotations

import numpy as np


def _surrogate_effective_ratio(delta: float, rho: float) -> float:
    delta = float(np.clip(delta, 1e-4, 1.0))
    rho = float(max(rho, 0.0))
    entropy_factor = 1.0 + 2.0 * np.log1p(1.0 / delta)
    return max(0.0, rho * entropy_factor / delta)


def lower_arip_bound(delta: float, rho: float) -> float:
    """Return a conservative surrogate for L(delta, rho)."""

    effective = min(_surrogate_effective_ratio(delta, rho), 0.999999)
    root = np.sqrt(effective)
    return float(np.clip(2.0 * root - effective, 0.0, 0.999999))


def upper_arip_bound(delta: float, rho: float) -> float:
    """Return a conservative surrogate for U(delta, rho)."""

    effective = max(_surrogate_effective_ratio(delta, rho), 0.0)
    root = np.sqrt(effective)
    return float(max(0.0, 2.0 * root + effective))


def rip_bound(delta: float, rho: float) -> float:
    """Return R(delta, rho)=max{L(delta, rho), U(delta, rho)}."""

    return max(lower_arip_bound(delta, rho), upper_arip_bound(delta, rho))


def _psi(delta: float, rho_ordered: float, rho_base: float) -> float:
    numerator = upper_arip_bound(delta, rho_ordered) + lower_arip_bound(delta, rho_ordered)
    denominator = max(1.0 - lower_arip_bound(delta, rho_base), 1e-12)
    return float(numerator / denominator)


def mu_siht(delta: float, rho: float) -> float:
    return float(2.0 * rip_bound(delta, 3.0 * rho))


def mu_sniht(delta: float, rho: float) -> float:
    return float(2.0 * _psi(delta, 3.0 * rho, rho))


def mu_shtp(delta: float, rho: float) -> float:
    r3 = rip_bound(delta, 3.0 * rho)
    r2 = rip_bound(delta, 2.0 * rho)
    denominator = max(1.0 - r2 * r2, 1e-12)
    return float(np.sqrt(2.0 * r3 * r3 / denominator))


def mu_snhtp(delta: float, rho: float) -> float:
    psi3 = _psi(delta, 3.0 * rho, rho)
    psi2 = _psi(delta, 2.0 * rho, rho)
    denominator = max(1.0 - psi2 * psi2, 1e-12)
    return float(np.sqrt(2.0 * psi3 * psi3 / denominator))


def mu_scosamp(delta: float, rho: float) -> float:
    r4 = rip_bound(delta, 4.0 * rho)
    denominator = max(1.0 - r4 * r4, 1e-12)
    return float(np.sqrt(4.0 * r4 * r4 * (1.0 + 3.0 * r4 * r4) / denominator))


SURROGATE_MU_FUNCTIONS = {
    "SIHT": mu_siht,
    "SNIHT": mu_sniht,
    "SHTP": mu_shtp,
    "SNHTP": mu_snhtp,
    "SCoSaMP": mu_scosamp,
}

MU_FUNCTIONS = SURROGATE_MU_FUNCTIONS

MU_MODELS = {
    "surrogate_arip_v1": SURROGATE_MU_FUNCTIONS,
}


__all__ = [
    "MU_MODELS",
    "MU_FUNCTIONS",
    "SURROGATE_MU_FUNCTIONS",
    "lower_arip_bound",
    "mu_scosamp",
    "mu_shtp",
    "mu_siht",
    "mu_snhtp",
    "mu_sniht",
    "rip_bound",
    "upper_arip_bound",
]
