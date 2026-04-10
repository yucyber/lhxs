import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.core.metrics import (
    is_exact_recovery,
    nmse,
    recovery_area_ratio,
    support_recovery_rate,
)
from joint_sparse_recovery.core.stopping import ResidualHistory, should_stop


class MetricsAndStoppingTest(unittest.TestCase):
    def test_is_exact_recovery_and_nmse(self):
        X_true = np.array([[1.0, -1.0], [0.0, 0.0]])
        X_hat = X_true + 1e-4
        self.assertTrue(is_exact_recovery(X_hat, X_true, tol=1e-3))
        self.assertLess(nmse(X_hat, X_true), 1e-6)

    def test_support_recovery_rate(self):
        self.assertEqual(support_recovery_rate(np.array([3, 1]), np.array([1, 3])), 1.0)
        self.assertEqual(support_recovery_rate(np.array([2, 1]), np.array([1, 3])), 0.0)

    def test_recovery_area_ratio(self):
        ratio = recovery_area_ratio(
            np.array([0.0, 1.0]),
            np.array([0.0, 2.0]),
            np.array([0.0, 1.0]),
            np.array([0.0, 1.0]),
        )
        self.assertAlmostEqual(ratio, 2.0, places=6)

    def test_should_stop_residual_small(self):
        history = ResidualHistory([0.1])
        stop, reason = should_stop(
            iteration=1,
            residual_norm=1e-5,
            y_norm=1.0,
            m=10,
            n=100,
            max_iterations=100,
            history=history,
        )
        self.assertTrue(stop)
        self.assertEqual(reason, "residual_small")

    def test_should_stop_stagnation(self):
        history = ResidualHistory([1.0] * 17)
        stop, reason = should_stop(
            iteration=20,
            residual_norm=1.0,
            y_norm=1.0,
            m=50,
            n=100,
            max_iterations=100,
            history=history,
            residual_small_factor=1e-6,
            stagnation_window=16,
            stagnation_tol=1e-6,
        )
        self.assertTrue(stop)
        self.assertEqual(reason, "stagnation")


if __name__ == "__main__":
    unittest.main()
