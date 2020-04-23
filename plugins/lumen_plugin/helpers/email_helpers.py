from airflow.operators.email_operator import EmailOperator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
from datetime import datetime
import re

def are_all_tasks_successful(context):
    '''
    Uses the context dictionary passed via the Python Operator
    to iterate over all the test tasks and return True if all pass
    and False if otherwise
    '''
    dag_instance = context["dag"]
    execution_date = context["execution_date"]
    tasks = dag_instance.task_ids
    for task in tasks:
        # Evaluate only test tasks via regex
        if re.match('\btest_', task):
            operator_instance = dag_instance.get_task(task)
            task_status = TaskInstance(operator_instance, execution_date).current_state()
            if task_status == State.FAILED:
                return False
    return True


def report_notify_email(email_template_location, emails, **context):
    """Send custom email alerts."""
    report_passed = are_all_tasks_successful(context)
    dag_name = context['ti'].dag_id
    email_subject = f"[{report_passed}] {report_name}"

    with open(email_template_location) as file:
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=emails,
            subject=email_subject,
            html_content=file.read()
        )
        params = {
            "passed": report_passed,
            "updated": datetime.now(),
            "title": dag_name,
            "details_link": "#"
        }
        send_email.render_template_fields(
            context=params,
            jinja_env=context['dag'].get_template_env()
        )
        send_email.execute(context)
