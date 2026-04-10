import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.algorithms.shtp import snhtp
from joint_sparse_recovery.experiments.weak_phase import (
    evaluate_success_rate,
    fit_weak_transition_curve,
    sample_transition_band,
)


class WeakPhasePipelineTest(unittest.TestCase):
    def test_sample_transition_band(self):
        np.testing.assert_array_equal(sample_transition_band(2, 5, 10), np.array([2, 3, 4, 5]))
        self.assertLessEqual(sample_transition_band(1, 100, 12).size, 12)

    def test_fit_weak_transition_curve(self):
        records = []
        for rho, success in [(0.1, 1), (0.15, 1), (0.2, 1), (0.3, 0), (0.4, 0)]:
            records.extend({"rho": rho, "success": success} for _ in range(5))
        rho_w, status = fit_weak_transition_curve(records)
        self.assertTrue(0.1 <= rho_w <= 0.4)
        self.assertIsInstance(status, str)

    def test_evaluate_success_rate_smoke(self):
        rate, records = evaluate_success_rate(
            solver=snhtp,
            solver_kwargs={"max_iterations": 50},
            m=20,
            n=40,
            k=3,
            l=2,
            matrix_ensemble="gaussian",
            n_trials=2,
            rng=np.random.default_rng(0),
            success_tol=1e-3,
        )
        self.assertTrue(0.0 <= rate <= 1.0)
        self.assertEqual(len(records), 2)


if __name__ == "__main__":
    unittest.main()
