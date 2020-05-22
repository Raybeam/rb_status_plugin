from airflow.models import Variable
from lumen_plugin.report_form_saver import ReportFormSaver
import datetime
import copy

import unittest


class AttributeDict(dict):
    """
    Class for mirroring ReportForm's data field
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __deepcopy__(self, memo):
        return AttributeDict(copy.deepcopy(dict(self)))


class ReportSaveTest(unittest.TestCase):
    """
    Class for testing the ability to save report forms.
    """

    report_form_sample = AttributeDict(
        {
            "title": AttributeDict({"data": "test report title"}),
            "description": AttributeDict({"data": "test description"}),
            "owner_name": AttributeDict({"data": "John Doe"}),
            "owner_email": AttributeDict({"data": "jdoe@raybeam.com"}),
            "subscribers": AttributeDict(
                {"data": "email1@raybeam.com,email2@raybeam.com"}
            ),
            "tests": AttributeDict(
                {
                    "data": [
                        "example_dag.python_print_date_0",
                        "example_dag.python_random_0",
                    ]
                }
            ),
            "schedule_type": AttributeDict({"data": "custom"}),
            "schedule_custom": AttributeDict({"data": "* * * 1 *"}),
        }
    )

    report_form_sample_duplicate = AttributeDict(
        {
            "title": AttributeDict({"data": "new test report title"}),
            "description": AttributeDict({"data": "new test description"}),
            "owner_name": AttributeDict({"data": "Jake Doe"}),
            "owner_email": AttributeDict({"data": "jakedoe@raybeam.com"}),
            "subscribers": AttributeDict(
                {"data": "email1@raybeam.com,email2@raybeam.com"}
            ),
            "tests": AttributeDict(
                {
                    "data": [
                        "example_dag.python_print_date_0",
                        "example_dag.python_random_0",
                    ]
                }
            ),
            "schedule_type": AttributeDict({"data": "custom"}),
            "schedule_custom": AttributeDict({"data": "* * * 1 1"}),
            "report_id": AttributeDict({"data": "lumen_report_new test report title"}),
        }
    )

    report_form_sample_daily = AttributeDict(
        {
            "title": AttributeDict({"data": "test report title daily"}),
            "description": AttributeDict({"data": "test description"}),
            "owner_name": AttributeDict({"data": "John Doe"}),
            "owner_email": AttributeDict({"data": "jdoe@raybeam.com"}),
            "subscribers": AttributeDict(
                {"data": "email1@raybeam.com,email2@raybeam.com"}
            ),
            "tests": AttributeDict(
                {
                    "data": [
                        "example_dag.python_print_date_0",
                        "example_dag.python_random_0",
                    ]
                }
            ),
            "schedule_type": AttributeDict({"data": "daily"}),
            "schedule_time": AttributeDict(
                {"data": datetime.datetime(year=2000, month=1, day=1, hour=5, minute=0)}
            ),
        }
    )

    report_form_sample_weekly = AttributeDict(
        {
            "title": AttributeDict({"data": "test report title weekly"}),
            "description": AttributeDict({"data": "test description"}),
            "owner_name": AttributeDict({"data": "John Doe"}),
            "owner_email": AttributeDict({"data": "jdoe@raybeam.com"}),
            "subscribers": AttributeDict(
                {"data": "email1@raybeam.com,email2@raybeam.com"}
            ),
            "tests": AttributeDict(
                {
                    "data": [
                        "example_dag.python_print_date_0",
                        "example_dag.python_random_0",
                    ]
                }
            ),
            "schedule_type": AttributeDict({"data": "weekly"}),
            "schedule_time": AttributeDict(
                {
                    "data": datetime.datetime(
                        year=2000, month=1, day=1, hour=3, minute=30
                    )
                }
            ),
            "schedule_week_day": AttributeDict({"data": "0"}),
        }
    )

    @classmethod
    def setUpClass(self):
        """
        Extract report_form_sample into airflow variable.
        """
        print("Creating airflow variable...")
        report_saver = ReportFormSaver(self.report_form_sample)
        report_saver.extract_report_data_into_airflow(report_exists=False)

    @classmethod
    def tearDownClass(self):
        """
        Delete the airflow variable.
        """
        print("Removing airflow variable...")
        Variable.delete("lumen_report_" + self.report_form_sample.title.data)

    def test_saved_title(self):
        """
        Test that the report's title attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True,
        )
        self.assertEqual(
            self.report_form_sample.title.data, report_airflow_variable["report_title"]
        )

    def test_saved_description(self):
        """
        Test that the report's description attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True,
        )
        self.assertEqual(
            self.report_form_sample.description.data,
            report_airflow_variable["description"],
        )

    def test_saved_owner_name(self):
        """
        Test that the report's owner_name attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True,
        )
        self.assertEqual(
            self.report_form_sample.owner_name.data,
            report_airflow_variable["owner_name"],
        )

    def test_saved_owner_email(self):
        """
        Test that the report's owner_email attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True,
        )
        self.assertEqual(
            self.report_form_sample.owner_email.data,
            report_airflow_variable["owner_email"],
        )

    def test_saved_subscribers(self):
        """
        Test that the report's subscribers attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True,
        )
        self.assertEqual(
            self.report_form_sample.subscribers.data,
            report_airflow_variable["subscribers"],
        )

    def test_format_report(self):
        """
        Test that the subscribers was properly formatted.
        This will also update the report_form_sample and airflow varible.
        """
        self.assertEqual(
            self.report_form_sample.subscribers.data,
            ["email1@raybeam.com", "email2@raybeam.com", "jdoe@raybeam.com"],
        )

    def test_valid_email(self):
        """
        Test that no errors are thrown with a correct email.
        """
        valid_email = "jdoe@raybeam.com"
        self.assertEqual(
            None, ReportFormSaver.validate_email(ReportFormSaver, valid_email)
        )

    def test_invalid_email(self):
        """
        Test that errors are thrown with an invalid email.
        """
        invalid_email = "not an email"
        with self.assertRaises(Exception) as context:
            ReportFormSaver.validate_email(ReportFormSaver, invalid_email)
            self.assertTrue(
                (f"Email ({invalid_email}) is not valid."
                 "Please enter a valid email address.")
                in str(context.exception)
            )

    def test_daily_schedule_conversion(self):
        """
        Test that daily schedule is converted properly into cron expression.
        """
        report_saver = ReportFormSaver(self.report_form_sample_daily)
        report_saver.extract_report_data_into_airflow(report_exists=False)
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample_daily.title.data,
            deserialize_json=True,
        )
        Variable.delete("lumen_report_" + self.report_form_sample_daily.title.data)
        self.assertEqual("00 05 * * *", report_airflow_variable["schedule"])

    def test_weekly_schedule_conversion(self):
        """
        Test that weekly schedule is converted properly into cron expression.
        """
        report_saver = ReportFormSaver(self.report_form_sample_weekly)
        report_saver.extract_report_data_into_airflow(report_exists=False)
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample_weekly.title.data,
            deserialize_json=True,
        )
        Variable.delete("lumen_report_" + self.report_form_sample_weekly.title.data)
        self.assertEqual("30 03 * * 0", report_airflow_variable["schedule"])

    def test_duplicate_report(self):
        """
        Test that two reports can't be created with same name.
        """
        duplicate_report = copy.deepcopy(self.report_form_sample_duplicate)
        with self.assertRaises(Exception) as context:
            report_saver = ReportFormSaver(duplicate_report)
            report_saver.extract_report_data_into_airflow(report_exists=False)

            self.assertTrue(
                "Error: report_id (lumen_report_test report title) already taken."
                in str(context.exception)
            )

    def test_editing_report(self):
        """
        Test that report can be edited.
        """
        updated_report = copy.deepcopy(self.report_form_sample_duplicate)
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample_duplicate.title.data,
            deserialize_json=True,
        )
        report_saver = ReportFormSaver(updated_report)
        report_saver.extract_report_data_into_airflow(report_exists=True)

        self.assertEqual(
            updated_report.schedule_custom.data, report_airflow_variable["schedule"]
        )


if __name__ == "__main__":
    unittest.main()
