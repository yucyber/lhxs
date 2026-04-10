import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.data.matrix_ensembles import (
    dct_subsample_matrix,
    gaussian_matrix,
    normalize_columns,
)
from joint_sparse_recovery.data.signal_models import (
    sample_joint_sparse_matrix,
    sample_problem_instance,
    sample_row_support,
)


class MatrixAndSignalGenerationTest(unittest.TestCase):
    def test_normalize_columns(self):
        A = np.array([[3.0, 0.0], [4.0, 0.0]])
        A_norm = normalize_columns(A)
        np.testing.assert_allclose(np.linalg.norm(A_norm[:, 0]), 1.0)
        np.testing.assert_allclose(A_norm[:, 1], np.array([0.0, 0.0]))

    def test_gaussian_matrix_shape_and_scale(self):
        rng = np.random.default_rng(0)
        A = gaussian_matrix(20, 30, rng=rng)
        self.assertEqual(A.shape, (20, 30))
        self.assertLess(abs(np.var(A) - 1.0 / 20.0), 0.05)

    def test_dct_subsample_matrix(self):
        rng = np.random.default_rng(0)
        A = dct_subsample_matrix(16, 32, rng=rng, normalize=True)
        self.assertEqual(A.shape, (16, 32))
        np.testing.assert_allclose(np.linalg.norm(A, axis=0), np.ones(32), atol=1e-8)

    def test_sample_row_support_and_joint_sparse_matrix(self):
        rng = np.random.default_rng(0)
        support = sample_row_support(10, 3, rng=rng)
        self.assertEqual(support.size, 3)
        X = sample_joint_sparse_matrix(10, 4, support, rng=rng, value_ensemble="rademacher")
        self.assertEqual(X.shape, (10, 4))
        np.testing.assert_array_equal(np.where(np.linalg.norm(X, axis=1) > 0)[0], support)
        self.assertTrue(np.all(np.isin(X[support, :], [-1.0, 1.0])))

    def test_sample_problem_instance(self):
        rng = np.random.default_rng(0)
        problem = sample_problem_instance(16, 32, 4, 3, "gaussian", rng=rng)
        self.assertEqual(problem.A.shape, (16, 32))
        self.assertEqual(problem.X_true.shape, (32, 3))
        self.assertEqual(problem.Y.shape, (16, 3))
        self.assertEqual(problem.support_true.size, 4)
        np.testing.assert_allclose(problem.A @ problem.X_true, problem.Y)


if __name__ == "__main__":
    unittest.main()
