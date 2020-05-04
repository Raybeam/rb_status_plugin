from airflow.models import Variable
from plugins.lumen_plugin.helpers.report_save_helpers import (
    extract_report_data_into_airflow,
    format_form_for_airflow,
    validate_email,
)
import unittest


class AttributeDict(dict):
    """
    Class for mirroring ReportForm's data field
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


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
            "schedule_custom": AttributeDict({"data": "* * * 1 *"}),
        }
    )

    @classmethod
    def setUpClass(self):
        """
        Extract report_form_sample into airflow variable.
        """
        print("Creating airflow variable...")
        extract_report_data_into_airflow(self.report_form_sample)

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
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True
        )
        self.assertEqual(
            self.report_form_sample.title.data, report_airflow_variable["report_title"]
        )

    def test_saved_description(self):
        """
        Test that the report's description attribute is correct
        """
        report_airflow_variable = Variable.get(
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True
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
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True
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
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True
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
            "lumen_report_" + self.report_form_sample.title.data, deserialize_json=True
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
        self.report_form_sample = format_form_for_airflow(self.report_form_sample)
        self.setUpClass()
        self.assertEqual(
            self.report_form_sample.subscribers.data,
            ["email1@raybeam.com", "email2@raybeam.com", "jdoe@raybeam.com"],
        )

    def test_valid_email(self):
        """
        Test that no errors are thrown with a correct email.
        """
        valid_email = "jdoe@raybeam.com"
        self.assertEqual(None, validate_email(valid_email))

    def test_invalid_email(self):
        """
        Test that errors are thrown with an invalid email.
        """
        invalid_email = "not an email"
        with self.assertRaises(Exception) as context:
            validate_email(invalid_email)

        self.assertTrue(
            "Email (%s) is not valid. Please enter a valid email address."
            % (invalid_email)
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
