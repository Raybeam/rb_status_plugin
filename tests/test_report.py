from rb_status_plugin.core.report import Report

import pytest


@pytest.mark.compatibility
class ReportTest:
    def test_task_id_naming(self):
        r = Report("dummy name")
        self.assertEqual(r.dag_id, "rb_status_dummy_name")
