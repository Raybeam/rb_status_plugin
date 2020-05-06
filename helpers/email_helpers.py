from airflow.operators.email_operator import EmailOperator
from airflow import configuration
from lumen_plugin.report_instance import ReportInstance
from lumen_plugin.views import LumenStatusView
import logging


def get_details_link():
    base_url = configuration.get("webserver", "BASE_URL")
    # If you don't override route_base, Flask BaseView uses class name
    if LumenStatusView.route_base:
        route_base = LumenStatusView.route_base
    else:
        route_base = LumenStatusView.__name__.lower()
    return f"{base_url}/{route_base}/"


def get_status(passed):
    if passed is None:
        return "Unknown"

    return "Success" if passed else "Failed"


def report_notify_email(report, email_template_location, **context):
    """
    For the given report, sends a notification email in the format given
    in the email_template

    :param report: report being notified on
    :type report: Report

    :param email_template_location: location of html template to use for status
    :type email_template_location: str

    :param test_prefix: the prefix that precedes all test tasks
    :type test_prefix: str
    """
    ri = ReportInstance(context["dag_run"])

    updated_time = ri.updated
    passed = ri.passed
    status = get_status(passed)
    details_link = get_details_link()

    with open(email_template_location) as file:
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=report.subscribers,
            subject="[{{status}}] {{title}}",
            html_content=file.read(),
        )
        params = {
            "passed": passed,
            "status": status,
            "updated": updated_time,
            "title": report.name,
            "details_link": details_link,
        }
        send_email.render_template_fields(
            context=params, jinja_env=context["dag"].get_template_env()
        )
        logging.info(f'Sending "{send_email.subject}" email...')
        send_email.execute(context)