from airflow.models import Variable
import json
import logging
import re
from flask import flash
from inflection import parameterize

from lumen_plugin.report_repo import VariablesReportRepo


def extract_report_data_into_airflow(form, report_exists):
    """
    Extract output of report form into a formatted airflow variable.

    :param form: report being parsed and saved
    :type form: ReportForm

    :param report_exists: whether the report exists
    :type report_exists: Boolean

    Return whether form submitted.
    """

    # format email list
    form = format_emails(form)

    logging.info("saving output to airflow variable...")

    # save form's fields to python dictionary
    report_dict = {}
    report_dict["report_title"] = form.title.data
    report_dict["report_title_url"] = parameterize(form.title.data)
    report_dict["description"] = form.description.data
    report_dict["owner_name"] = form.owner_name.data
    report_dict["owner_email"] = form.owner_email.data
    report_dict["subscribers"] = form.subscribers.data
    report_dict["tests"] = form.tests.data
    report_dict["schedule_type"] = form.schedule_type.data
    if report_dict["schedule_type"] == "custom":
        report_dict["schedule"] = form.schedule_custom.data
    elif report_dict["schedule_type"] == "manual":
        report_dict["schedule"] = None
    else:
        report_dict["schedule_time"] = None
        convert_schedule_to_cron_expression(report_dict, form)

    # verify input for each field (except subscribers)
    form_completed = True
    for field_name in report_dict.keys():
        if field_name != "subscribers":
            form_completed = form_completed and check_empty(report_dict, field_name)

    if form_completed:
        if report_exists:
            report_dict["report_id"] = form.report_id.data
        else:
            report_dict["report_id"] = "%s%s" % (
                VariablesReportRepo.report_prefix,
                report_dict["report_title"],
            )
            if not check_unique_field(report_exists, "report_id", report_dict):
                return False
        if check_unique_field(report_exists, "report_title_url", report_dict):
            report_json = json.dumps(report_dict)
            Variable.set(key=report_dict["report_id"], value=report_json)
            return True
    return False

def check_unique_field(report_exists, field_name, report_dict):
    """
    Chack if field is already exists

    :param report_exists: whether the report exists
    :type report_exists: Boolean

    :param field_name: name of report attribute
    :type field_name: String

    :param report_dict: a mapping of form attributes to inputted values
    :type report_dict: Dict

    Return boolean on whether entry is unique
    """

    for report in VariablesReportRepo.list():
        if report_exists and getattr(report, "report_id") == report_dict["report_id"]:
            continue
        else:
            if str(getattr(report, field_name)) == report_dict[field_name]:
                logging.exception(
                    "Error: %s (%s) already taken."
                    % (field_name, report_dict[field_name])
                )
                logging.error(
                    "Error: %s (%s) already taken."
                    % (field_name, report_dict[field_name])
                )
                flash(
                    "Error: %s (%s) already taken."
                    % (field_name, report_dict[field_name])
                )
                return False
    return True

def check_empty(report_dict, field_name):
    """
    Check for empty data in field
    Return boolean on whether field is filled
    """
    if report_dict[field_name] or (
        field_name == "schedule" and report_dict["schedule_type"] == "manual"
    ):
        return True
    else:
        logging.exception("Error: %s can not be empty." % (field_name))
        logging.error("Error: %s can not be empty." % (field_name))
        flash("Error: %s can not be empty." % (field_name))
        return False


def format_emails(form):
    """
    Parse, transform, and vaildate emails.
    """

    # Add owner's email to subscribers; dedupe, order, & format subscribers
    emails = form.owner_email.data.split(",")
    if len(emails) != 1:
        logging.exception("Error: Exactly one email is required for Owner Email field.")
        logging.error("Error: Exactly one email is required for Owner Email field.")
        flash("Error: Exactly one email is required for Owner Email field.")

    emails += form.subscribers.data.split(",")
    emails = list(set([email.replace(" ", "") for email in emails]))
    emails = [email for email in emails if email]
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
        logging.exception(
            "Email (%s) is not valid. Please enter a valid email address." % email
        )
        logging.error(
            "Email (%s) is not valid. Please enter a valid email address." % email
        )
        flash("Email (%s) is not valid. Please enter a valid email address." % email)


def convert_schedule_to_cron_expression(report_dict, form):
    """
    Convert Weekly and Daily schedules into a cron expression, and
    saves attributes to report_dict
    """
    # add time of day
    try:
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
    except AttributeError:
        logging.exception("Error: Schedule's time is invalid.")
        logging.error("Error: Schedule's time is invalid.")
        flash("Error: Schedule's time is invalid.")
