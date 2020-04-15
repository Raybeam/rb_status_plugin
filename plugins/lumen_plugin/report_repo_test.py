from plugins.lumen_plugin.report_repo import VariablesReportRepo
from plugins.lumen_plugin.report import Report

import json
import unittest

class VariablesReportRepoTest(unittest.TestCase):
    dummy_test = """
            {
            "tests": [
                "dag_name.operator_1", 
                "dag_name.operator_3"
            ],
            "emails": ["bbriski@raybeam.com", "msadler@raybeam.com"],
            "schedule": "0 7 * * *"
            }
            """

    def test_parse_variable_value(self):
        parsed = VariablesReportRepo.parse_variable_val(self.dummy_test)
        self.assertEqual(parsed['tests'], ['dag_name.operator_1', 'dag_name.operator_3'])

    def test_parse_variable_value_no_json(self):
        parsed = VariablesReportRepo.parse_variable_val("not_json")
        self.assertIsNone(parsed)
    
    def test_parse_variable_name(self):
        parsed =VariablesReportRepo.parse_variable_name("lumen_report_bob")
        self.assertEqual(parsed, 'bob')

    def test_parse_variable_name_ci(self):
        parsed =VariablesReportRepo.parse_variable_name("LUMEN_REPORT_BOB")
        self.assertEqual(parsed, 'BOB')
    
    def test_parse_variable_name_none(self):
        parsed =VariablesReportRepo.parse_variable_name("not_correct")
        self.assertIsNone(parsed)

    def test_return_report(self):
        vrr = VariablesReportRepo(None)

        parsed = json.loads(self.dummy_test)
        r = vrr.to_report('bob', parsed)
        self.assertIsInstance(r, Report)
        


if __name__ == '__main__':
    unittest.main()