import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.core.support_ops import (
    detect_support,
    hard_threshold_rows,
    row_l2_norms,
)


class SupportOpsTest(unittest.TestCase):
    def test_row_l2_norms(self):
        matrix = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 2.0]])
        np.testing.assert_allclose(row_l2_norms(matrix), [5.0, 0.0, np.sqrt(5.0)])

    def test_detect_support_topk(self):
        matrix = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 2.0]])
        support = detect_support(matrix, 2)
        np.testing.assert_array_equal(np.sort(support), [0, 2])

    def test_detect_support_edge_cases(self):
        matrix = np.eye(3)
        self.assertEqual(detect_support(matrix, 0).size, 0)
        np.testing.assert_array_equal(detect_support(matrix, 5), np.array([0, 1, 2]))

    def test_hard_threshold_rows(self):
        matrix = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 2.0]])
        thresholded, support = hard_threshold_rows(matrix, 1)
        np.testing.assert_array_equal(support, np.array([0]))
        np.testing.assert_allclose(thresholded, np.array([[3.0, 4.0], [0.0, 0.0], [0.0, 0.0]]))


if __name__ == "__main__":
    unittest.main()
