from airflow.operators.email_operator import EmailOperator
from plugins.lumen_plugin.report_instance import ReportInstance
import re
import logging
from airflow import configuration
from plugins.lumen_plugin import LumenBuilderBaseView


def get_details_link():
    base_url = configuration.get('webserver', 'BASE_URL')
    # If you don't override route_base, Flask BaseView uses class name
    if LumenBuilderBaseView.route_base:
        route_base = LumenBuilderBaseView.route_base
    else:
        route_base = LumenBuilderBaseView.__name__.lower()
    return f"{base_url}/{route_base}/"


def report_notify_email(report, email_template_location, **context):
    """
    :param report: report being notified on
    :type report: Report

    :param email_template_location: location of html template to use for status
    :type email_template_location: str

    :param test_prefix: the prefix that precedes all test tasks
    :type test_prefix: str
    """
    ri = ReportInstance(context["dag_run"], report.test_prefix)

    updated_time = ri.updated
    passed = ri.passed
    status = ri.status
    details_link = get_details_link()

    with open(email_template_location) as file:
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=report.emails,
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
