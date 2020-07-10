from rb_status_plugin.core.report_repo import VariablesReportRepo
from rb_status_plugin.core.report import Report

import json
import unittest
import pytest


@pytest.mark.compatibility
class VariablesReportRepoTest(unittest.TestCase):
    dummy_test = """
            {
                "report_title": "my report title",
                "report_title_id": "my-report-title",
                "description": "my report description",
                "owner_name": "my name",
                "owner_email": "email_owner@mail.com",
                "subscribers":
                [
                    "email1@mail.com",
                    "email2@mail.com",
                    "email3@mail.com"
                ],
                "tests":
                [
                    "example_dag.python_print_date_0",
                    "example_dag.python_random_0"
                ],
                "schedule_type": "custom",
                "schedule": "* * * 1 *",
                "report_id": "rb_status_my report title"
            }
            """

    def test_parse_variable_value(self):
        parsed = VariablesReportRepo.parse_variable_val(self.dummy_test)
        self.assertEqual(
            parsed["tests"],
            ["example_dag.python_print_date_0", "example_dag.python_random_0"],
        )

    def test_parse_variable_value_no_json(self):
        parsed = VariablesReportRepo.parse_variable_val("not_json")
        self.assertIsNone(parsed)

    def test_parse_variable_name(self):
        parsed = VariablesReportRepo.parse_variable_name("rb_status_bob")
        self.assertEqual(parsed, "bob")

    def test_parse_variable_name_ci(self):
        parsed = VariablesReportRepo.parse_variable_name("RB_STATUS_BOB")
        self.assertEqual(parsed, "BOB")

    def test_parse_variable_name_none(self):
        parsed = VariablesReportRepo.parse_variable_name("not_correct")
        self.assertIsNone(parsed)

    def test_return_report(self):
        parsed = json.loads(self.dummy_test)
        r = VariablesReportRepo.to_report("bob", parsed)
        self.assertIsInstance(r, Report)


if __name__ == "__main__":
    unittest.main()
