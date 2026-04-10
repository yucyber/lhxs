import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.config_utils import load_config, resolve_run_config


class ConfigProfileTest(unittest.TestCase):
    def test_default_weak_phase_profile_is_quick(self):
        config = load_config("configs/weak_phase.yaml")
        run_cfg = resolve_run_config(config)
        self.assertEqual(run_cfg["profile_name"], "quick")
        self.assertEqual(run_cfg["n"], 128)
        self.assertEqual(run_cfg["output_table"], "outputs/tables/weak_phase_curves.csv")
        self.assertTrue(run_cfg["matrix_options"]["dct"]["normalize_columns"])

    def test_paper_profile_is_namespaced_and_scaled(self):
        config = load_config("configs/weak_phase.yaml")
        run_cfg = resolve_run_config(config, profile="paper")
        self.assertEqual(run_cfg["n"], 1024)
        self.assertTrue(run_cfg["output_table"].startswith("outputs/profiles/paper/"))
        self.assertFalse(run_cfg["matrix_options"]["dct"]["normalize_columns"])
        self.assertGreaterEqual(len(run_cfg["delta_grid"]), 20)


if __name__ == "__main__":
    unittest.main()
