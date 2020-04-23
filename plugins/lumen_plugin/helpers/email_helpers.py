from airflow.operators.email_operator import EmailOperator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
import datetime


def are_all_tasks_successful(context):
    dag_instance = context["dag"]
    execution_date = context["execution_date"]
    tasks = dag_instance.task_ids
    for task in tasks:
        operator_instance = dag_instance.get_task(task)
        task_status = TaskInstance(operator_instance, execution_date).current_state()
        if task_status == State.FAILED:
            return False
    return True


def report_notify_email(emails, **context):
    """Send custom email alerts."""
    report_passed = are_all_tasks_successful(context)
    with open("plugins/lumen_plugin/templates/emails/single_report.html") as file:
        subject_line = f"[{report_passed}] {context['ti'].dag_id}"
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=emails,
            subject=subject_line,
            html_content=file.read(),
            params={
                "passed": report_passed,
                "updated": "ts",
                "title": subject_line,
                "details_link": "#"
            }
        )
        send_email.render_template_fields(
            context=context,
            jinja_env=context['dag'].get_template_env()
        )
        send_email.execute(context)
