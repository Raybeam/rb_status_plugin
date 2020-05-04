from airflow.models import Variable
import json
import logging
import re


def extract_report_data_into_airflow(form):
    """
    Extract output of report form into a formatted airflow variable.
    """

    log = logging.getLogger(__name__)
    log.info("saving output to airflow variable...")

    report_dict = {}
    report_dict["report_title"] = form.title.data
    report_dict["description"] = form.description.data
    report_dict["owner_name"] = form.owner_name.data
    report_dict["owner_email"] = form.owner_email.data
    report_dict["subscribers"] = form.subscribers.data
    report_dict["tests"] = form.tests.data
    report_dict["schedule_type"] = form.schedule_type.data
    if report_dict["schedule_type"] == "custom":
        report_dict["schedule"] = form.schedule_custom.data
    else:
        convert_schedule_to_cron_expression(report_dict, form)

    ariflow_variable_name = "lumen_report_%s" % (report_dict["report_title"])
    report_json = json.dumps(report_dict)
    Variable.set(key=ariflow_variable_name, value=report_json)


def format_form_for_airflow(form):
    """
    Parse the report form and transform/format the inputted data.
    """

    # Add owner's email to subscribers; dedupe, order, & format subscribers
    emails = form.subscribers.data.split(",")
    emails += form.owner_email.data.split(",")
    emails = list(set([email.replace(" ", "") for email in emails]))
    emails.sort()
    [validate_email(email) for email in emails]
    form.subscribers.data = emails

    return form


def validate_email(email):
    """
    Check that an email is properly formatted.
    """

    email_format = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")

    if not re.search(email_format, email):
        raise Exception(
            "Email (%s) is not valid. Please enter a valid email address." % email
        )


def convert_schedule_to_cron_expression(report_dict, form):
    """
    Convert Weekly and Daily schedules into a cron expression, and
    saves attributes to report_dict
    """
    # add time of day
    time_of_day = form.schedule_time.data.strftime("%H:%M")
    report_dict["schedule_time"] = time_of_day
    hour, minute = time_of_day.split(":")
    cron_expression = "%s %s * * " % (minute, hour)

    # add day of week if applicable
    if form.schedule_type.data == "weekly":
        cron_expression += form.schedule_week_day.data
        report_dict["schedule_week_day"] = form.schedule_week_day.data
    else:
        cron_expression += "*"

    report_dict["schedule"] = cron_expression
