import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.algorithms.ra_somp_music import ra_somp_music
from joint_sparse_recovery.algorithms.scosamp import scosamp
from joint_sparse_recovery.algorithms.shtp import shtp, snhtp
from joint_sparse_recovery.algorithms.siht import siht, sniht
from joint_sparse_recovery.data.signal_models import sample_problem_instance


class AlgorithmSmokeTest(unittest.TestCase):
    def setUp(self):
        self.problem = sample_problem_instance(
            m=32,
            n=64,
            k=4,
            l=3,
            matrix_ensemble="gaussian",
            rng=np.random.default_rng(0),
        )

    def _assert_solver_result(self, result):
        self.assertEqual(result.x_hat.shape, self.problem.X_true.shape)
        self.assertLessEqual(result.support_hat.size, 4)
        self.assertTrue(np.isfinite(result.residual_norm))
        self.assertGreaterEqual(result.n_iter, 1)
        self.assertIsInstance(result.stop_reason, str)

    def test_siht(self):
        self._assert_solver_result(siht(self.problem.A, self.problem.Y, 4, max_iterations=100))

    def test_sniht(self):
        self._assert_solver_result(sniht(self.problem.A, self.problem.Y, 4, max_iterations=100))

    def test_shtp(self):
        self._assert_solver_result(shtp(self.problem.A, self.problem.Y, 4, max_iterations=100))

    def test_snhtp(self):
        self._assert_solver_result(snhtp(self.problem.A, self.problem.Y, 4, max_iterations=100))

    def test_scosamp(self):
        self._assert_solver_result(scosamp(self.problem.A, self.problem.Y, 4, max_iterations=100))

    def test_ra_somp_music(self):
        self._assert_solver_result(ra_somp_music(self.problem.A, self.problem.Y, 4, max_iterations=100))


if __name__ == "__main__":
    unittest.main()
