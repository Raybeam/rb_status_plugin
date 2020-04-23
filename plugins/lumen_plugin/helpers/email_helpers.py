from airflow.operators.email_operator import EmailOperator
from airflow.models.taskinstance import TaskInstance
from plugins.lumen_plugin.report_instance import ReportInstance
from airflow.utils.state import State
from datetime import datetime
import re


def create_report_instance(context):
    return ReportInstance(context["dag_run"])


def get_test_status(report_instance):
    """
    Uses the report_instance passed via the Python Operator
    and create a list with all test status values
    """
    return report_instance.errors()


def are_all_tasks_successful(test_prefix, errors):
    """
    Iterate over all the test tasks status and return True if all pass
    and False if otherwise
    """

    if len(errors) == 0:
        return True

    for failed_task in errors:
        # If the failed task is a test task
        if re.match(test_prefix, task) is not None:
            return False

    return True


def report_notify_email(
    emails,
    email_template_location,
    test_prefix,
    **context
):
    """
    :param emails: emails to send report status to
    :type emails: list

    :param email_template_location: location of html template to use for status
    :type email_template_location: str

    :param test_prefix: the prefix that precedes all test tasks
    :type test_prefix: str
    """
    ri = create_report_instance(context)

    errors = get_test_status(ri)
    report_passed = are_all_tasks_successful(test_prefix, errors)
    status = "Success" if report_passed else "Failed"

    dag_name = ri.id
    updated_time = ri.updated
    email_subject = f"[{status}] {dag_name}"

    with open(email_template_location) as file:
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=emails,
            subject=email_subject,
            html_content=file.read(),
        )
        params = {
            "passed": report_passed,
            "updated": updated_time,
            "title": dag_name,
            "details_link": "#",
        }
        send_email.render_template_fields(
            context=params, jinja_env=context["dag"].get_template_env()
        )
        send_email.execute(context)
