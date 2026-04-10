"""Stopping criteria matching the weak phase-transition experiments."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class ResidualHistory:
    """Store Frobenius residual norms across iterations."""

    values: list[float] = field(default_factory=list)

    def append(self, residual_norm: float) -> None:
        self.values.append(float(residual_norm))

    def latest(self) -> float:
        return float("inf") if not self.values else self.values[-1]

    def has_stagnated(self, window: int, tol: float) -> bool:
        if window <= 0 or len(self.values) < window + 1:
            return False
        recent = np.asarray(self.values[-(window + 1):], dtype=float)
        return bool(np.max(np.abs(np.diff(recent))) < tol)

    def late_rate_close_to_one(self, iteration: int, late_start: int, lag: int, threshold: float) -> bool:
        if iteration <= late_start or lag <= 0 or len(self.values) < lag + 1:
            return False
        current = self.values[-1]
        previous = self.values[-(lag + 1)]
        if current <= 0.0 or previous <= 0.0:
            return False
        rate = ((previous * previous) / (current * current)) ** (1.0 / lag)
        return bool(rate > threshold)


def should_stop(
    iteration: int,
    residual_norm: float,
    y_norm: float,
    m: int,
    n: int,
    max_iterations: int,
    history: ResidualHistory,
    residual_small_factor: float = 1e-3,
    diverging_factor: float = 100.0,
    stagnation_window: int = 16,
    stagnation_tol: float = 1e-6,
    late_start: int = 125,
    late_rate_lag: int = 15,
    late_rate_threshold: float = 0.999,
) -> tuple[bool, str]:
    """Return whether an algorithm should stop and the reason label."""

    residual_norm = float(residual_norm)
    y_norm = float(y_norm)
    if not np.isfinite(residual_norm):
        return True, "residual_not_finite"

    residual_threshold = float(residual_small_factor) * float(m) / float(max(n, 1))
    if residual_norm < residual_threshold:
        return True, "residual_small"
    if iteration >= int(max_iterations):
        return True, "max_iterations"
    if residual_norm > float(diverging_factor) * max(y_norm, 1e-12):
        return True, "diverging"
    if history.has_stagnated(window=int(stagnation_window), tol=float(stagnation_tol)):
        return True, "stagnation"
    if history.late_rate_close_to_one(
        iteration=int(iteration),
        late_start=int(late_start),
        lag=int(late_rate_lag),
        threshold=float(late_rate_threshold),
    ):
        return True, "slow_late_rate"

    return False, "continue"


__all__ = ["ResidualHistory", "should_stop"]
