from airflow.operators.email_operator import EmailOperator
from airflow.configuration import conf
from airflow.models import Variable

import logging
import pendulum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rb_status_plugin.core.report_instance import ReportInstance
from rb_status_plugin.core.views import StatusView
from rb_status_plugin.core.flask_admin_packages import v_admin_status_package


def get_details_link():
    base_url = conf.get("webserver", "BASE_URL")
    # If you don't override route_base, Flask BaseView uses class name
    rbac = conf.getboolean("webserver", "rbac")
    if rbac:
        route_base = StatusView.route_base
        if not route_base:
            route_base = StatusView.__name__.lower()
    else:
        route_base = f"/admin/{v_admin_status_package.endpoint}"
        logging.info("url......." + str(base_url + route_base))

    return base_url + str(route_base)


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
    timezone = pendulum.timezone(conf.get("core", "default_timezone"))
    updated_time.replace(tzinfo=timezone)
    passed = ri.passed
    status = get_status(passed)
    details_link = get_details_link()
    use_sendgrid = True if Variable.get("use_sendgrid", "true").lower() == 'true' else False

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
            "title": report.report_title,
            "details_link": details_link,
        }
        send_email.render_template_fields(
            context=params, jinja_env=context["dag"].get_template_env()
        )

        if use_sendgrid:
            logging.info(f'Sending "{send_email.subject}" email...')
            send_email.execute(context)
        else:
            subject = send_email.subject
            message = send_email.html_content
            dag_id = context["dag"].dag_id
            composer_instance_name = conf.get('webserver', 'web_server_name')
            smtp_server = Variable.get("email_server", "smtp.raybeam.com")
            sender_email = Variable.get(
                f"{ dag_id }_sender_email",
                f"no-reply@{ composer_instance_name }.raybeam.com",
            )
            receivers = ", ".join(report.subscribers)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receivers
            mime_message = MIMEText(message, "html")
            msg.attach(mime_message)

            logging.info("Establishing connection with SMTP server..")
            server = smtplib.SMTP(f"{ smtp_server }:25")
            server.sendmail(sender_email, report.subscribers, msg.as_string())
            server.quit()

