from airflow.operators.email_operator import EmailOperator
import datetime


def report_notify_email(emails, context):
    """Send custom email alerts."""

    with open("templates/emails/single_report.html") as file:
        subject_line = f"[{report_status}] {context['ti'].dag_id}"
        send_email = EmailOperator(
            task_id="custom_email_notification",
            to=emails,
            subject=subject_line,
            html_content=file.read(),
            params={
                "passed": True,
                "updated": "{{ts}}",
                "title": "Report Title",
                "details_link": "#"
            }
        )
        send_email.execute(context)
