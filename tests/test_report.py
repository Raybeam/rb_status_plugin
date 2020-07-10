from rb_status_plugin.core.report import Report

import unittest
import pytest


@pytest.mark.compatibility
class ReportTest(unittest.TestCase):
    def test_task_id_naming(self):
        r = Report("dummy name")
        self.assertEqual(r.dag_id, "rb_status_dummy_name")


if __name__ == "__main__":
    unittest.main()
