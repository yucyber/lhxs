import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from joint_sparse_recovery.reporting import write_reproduction_audit


class ReproductionAuditTest(unittest.TestCase):
    def test_write_quick_audit(self):
        report_path = write_reproduction_audit()
        self.assertTrue(report_path.exists())
        content = report_path.read_text(encoding="utf-8")
        self.assertIn("复现状态对照表", content)
        self.assertIn("Strong phase exact ARIP 边界", content)

    def test_write_paper_audit(self):
        report_path = write_reproduction_audit(profile="paper")
        self.assertTrue(report_path.exists())
        self.assertIn("outputs\\profiles\\paper".replace("\\", "/"), str(report_path).replace("\\", "/"))


if __name__ == "__main__":
    unittest.main()
