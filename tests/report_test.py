from rb_status_plugin.report import Report

import unittest


class ReportTest(unittest.TestCase):
    def test_task_id_naming(self):
        r = Report("dummy name")
        self.assertEqual(r.dag_id, "lumen_dummy_name")


if __name__ == "__main__":
    unittest.main()
