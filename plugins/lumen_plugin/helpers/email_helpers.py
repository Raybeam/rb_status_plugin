from airflow.operators.email_operator import EmailOperator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
from datetime import datetime
import re


def get_test_status(test_prefix, context):
    """
    Uses the context dictionary passed via the Python Operator
    to iterate over all the test tasks (identified by the test prefix)
    and create a dict with all test status values
    """
    status_dict = {}

    dag_instance = context["dag"]
    execution_date = context["execution_date"]
    tasks = dag_instance.task_ids

    for task in tasks:
        # Evaluate only test tasks via regex
        if re.match(test_prefix, task) is not None:
            operator_instance = dag_instance.get_task(task)
            task_status = TaskInstance(
                operator_instance, execution_date
            ).current_state()
            status_dict[task] = task_status
    return status_dict


def are_all_tasks_successful(status_dict):
    """
    Iterate over all the test tasks status and return True if all pass
    and False if otherwise
    """
    for test_id in status_dict:
        if status_dict[test_id] == State.FAILED:
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
    status_dict = get_test_status(test_prefix, context)
    report_passed = are_all_tasks_successful(status_dict)
    status = "Success" if report_passed else "Failed"

    dag_name = context["ti"].dag_id
    updated_time = datetime.now()
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
