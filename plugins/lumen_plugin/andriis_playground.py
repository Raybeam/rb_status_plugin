# from airflow.utils.email import send_email
from airflow.models.baseoperator import BaseOperator
import datetime


def report_notify_email(contextDict, **kwargs):
    """Send custom email alerts."""

    b = BaseOperator(task_id="custom_email_notification")
    with open("templates/emails/single_report.html") as file:
        template = file.read()
        templated = b.render_template(content=template, context=contextDict)
        report_status = "Passed" if contextDict["passed"] else "Failed"
        title = "[{0}] {1}".format(report_status, contextDict["title"])
        print(title, templated)
        # send_email("you_email@address.com", title, templated)


report = {
    "passed": False,
    "updated": datetime.datetime.now(),
    "title": "Diary of a Madman",
    "details_link": "#",
}
report_notify_email(report)
