from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask import flash
from flask_appbuilder import SimpleFormView
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    BS3TextAreaFieldWidget,
    Select2ManyWidget,
    Select2Widget,
)
from flask_appbuilder.security.decorators import has_access

import datetime

from wtforms import StringField, TextAreaField, SelectMultipleField, SelectField
from wtforms_components import TimeField

from lumen_plugin.report_repo import VariablesReportRepo
from lumen_plugin.report_instance import ReportInstance
from lumen_plugin.helpers.report_save_helpers import (
    extract_report_data_into_airflow,
    format_form,
)
from lumen_plugin import test_data

import logging

test_choices = []
for test in test_data.dummy_tests:
    test_choices.append((test["id"], test["name"]))

form_fieldsets_config = [
    (
        "General",
        {
            "fields": [
                "title",
                "description",
                "owner_name",
                "owner_email",
                "subscribers",
            ]
        },
    ),
    (
        "Schedule",
        {
            "fields": [
                "schedule_type",
                "schedule_week_day",
                "schedule_time",
                "schedule_custom",
            ]
        },
    ),
    ("Tests", {"fields": ["tests"]}),
]

# Creating a flask appbuilder BaseView
class LumenStatusView(AppBuilderBaseView):
    """
    LumenStatusView is responsible for Lumen Status Page
    """

    route_base = "/lumen"

    def reports_data(self):
        """
        Generate reports data.
        It retrieves a list of reports, generates summary status
        and pass it all down to the template
        """
        reports = []
        passed = True
        updated = None
        logging.info("Loading reports")
        for report in VariablesReportRepo.list():
            try:
                ri = ReportInstance.get_latest(report)

                if not updated:
                    updated = ri.updated

                if updated < ri.updated:
                    updated = ri.updated

                r = {
                    "id": ri.id,
                    "passed": ri.passed,
                    "updated": ri.updated,
                    "title": report.name,
                    "owner_email": report.owner_email,
                }

                r["errors"] = ri.errors()
                if len(r["errors"]) > 0:
                    passed = False

                logging.info(r)
                reports.append(r)
            except Exception as e:
                logging.exception(e)
                logging.error("Failed to generate report: " + str(e))
                flash("Failed to generate report: " + str(e), "error")

        data = {"summary": {"passed": passed, "updated": updated}, "reports": reports}
        return data

    @expose("/status")
    def list(self):
        return self.render_template("status.html", content=self.reports_data())


class LumenReportsView(AppBuilderBaseView):
    route_base = "/lumen"

    @expose("/reports")
    def list(self):
        return self.render_template("reports.html", content=VariablesReportRepo.list())


class ReportForm(DynamicForm):
    title = StringField(("Title"), widget=BS3TextFieldWidget())
    description = TextAreaField(("Description"), widget=BS3TextAreaFieldWidget())
    owner_name = StringField(("Owner Name"), widget=BS3TextFieldWidget())
    owner_email = StringField(("Owner Email"), widget=BS3TextFieldWidget())
    subscribers = StringField(
        ("Subscribers"),
        description=(
            "List of comma separeted emails that should receive email notifications"
        ),
        widget=BS3TextFieldWidget(),
    )
    tests = SelectMultipleField(
        ("Tests"),
        description=("List of the tests to include in the report"),
        choices=test_choices,
        widget=Select2ManyWidget(),
    )
    schedule_type = SelectField(
        ("Schedule"),
        description=("Select how you want to schedule the report"),
        choices=[("daily", "Daily"), ("weekly", "Weekly"), ("custom", "Custom (Cron)")],
        widget=Select2Widget(),
    )
    schedule_time = TimeField("Time", render_kw={"class": "form-control"})
    schedule_week_day = SelectField(
        ("Day of week"),
        description=("Select day of a week you want to schedule the report"),
        choices=[
            ("0", "Sunday"),
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
        ],
        widget=Select2Widget(),
    )
    schedule_custom = StringField(("Cron schedule"), widget=BS3TextFieldWidget())


class NewReportFormView(SimpleFormView):
    route_base = "/lumen/report"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "New Report"
    form_fieldsets = form_fieldsets_config
    message = "My form submitted"

    @expose("/new", methods=["GET"])
    @has_access
    def this_form_get(self):
        return super().this_form_get()

    @expose("/new", methods=["POST"])
    @has_access
    def form_post(self):
        form = self.form.refresh()
        logging.info("Saving reports...\n\n")
        form = format_form(form)
        extract_report_data_into_airflow(form)
        # post process form
        flash(self.message, "info")
        return super().this_form_get()


class EditReportFormView(SimpleFormView):
    route_base = "/lumen/report"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "New Report"
    form_fieldsets = form_fieldsets_config
    message = "My form submitted"

    @expose("/<string:report_title>/edit", methods=["GET"])
    @has_access
    def this_form_get(self, report_title):
        self._init_vars()
        form = self.form.refresh()

        self.form_get(form, report_title)
        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    def form_get(self, form, report_title):
        # !get report by report_title and prefill form with its values
        requested_report = {}
        for report in VariablesReportRepo.list():
            if str(report.report_title) == report_title:
                requested_report = report

        if requested_report:
            form.title.data = requested_report.report_title
            form.description.data = requested_report.description
            form.owner_name.data = requested_report.owner_name
            form.owner_email.data = requested_report.owner_email
            form.subscribers.data = ", ".join(requested_report.subscribers)
            form.schedule_type.data = requested_report.schedule_type
            if (form.schedule_type.data == "custom"):
                form.schedule_custom.data = requested_report.schedule
            if (form.schedule_type.data == "daily"):
                form.schedule_time.data = datetime.datetime.strptime(requested_report.schedule_time, "%H:%M")
            if (form.schedule_type.data == "weekly"):
                form.schedule_time.data = datetime.datetime.strptime(requested_report.schedule_time, "%H:%M")
                form.schedule_week_day.data = requested_report.schedule_week_day
            form.tests.data = requested_report.tests

    @expose("/<string:report_title>/edit", methods=["POST"])
    @has_access
    def form_post(self, report_title):
        form = self.form.refresh()
        logging.info("Saving reports...\n\n")
        form = format_form(form)
        extract_report_data_into_airflow(form)
        # post process form
        flash(self.message, "info")
        return self.this_form_get(report_title)