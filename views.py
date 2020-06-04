from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask import flash, redirect, url_for, request
from flask_appbuilder import SimpleFormView
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    BS3TextAreaFieldWidget,
    Select2ManyWidget,
    Select2Widget,
)
from flask_appbuilder.security.decorators import has_access

from wtforms import (
    StringField,
    TextAreaField,
    SelectMultipleField,
    SelectField,
    HiddenField,
)
from wtforms.validators import DataRequired, Email
from wtforms_components import TimeField

from rb_status_plugin.report import Report
from rb_status_plugin.report_repo import VariablesReportRepo
from rb_status_plugin.report_instance import ReportInstance
from rb_status_plugin.report_form_saver import ReportFormSaver
from rb_status_plugin.helpers.list_tasks_helper import get_all_test_choices
from airflow.configuration import conf
import logging
import pendulum

form_fieldsets_config = [
    (
        "General",
        {
            "fields": [
                "report_title",
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
                "schedule_timezone",
                "schedule_custom",
            ]
        },
    ),
    ("Tests", {"fields": ["tests"]}),
]

# Creating a flask appbuilder BaseView
class StatusView(AppBuilderBaseView):
    """
    StatusView is responsible for Status Page
    """

    route_base = "/rb/status"

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
                    "updated": ri.updated.isoformat(),
                    "report_title": report.report_title,
                    "report_title_id": report.report_title_id,
                    "owner_name": report.owner_name,
                    "owner_email": report.owner_email,
                    "description": report.description,
                    "subscribers": report.subscribers,
                }

                r["errors"] = ri.errors()
                if len(r["errors"]) > 0:
                    passed = False
                reports.append(r)
            except Exception as e:
                logging.exception(e)
                logging.error("Failed to generate report: " + str(e))
                flash("Failed to generate report: " + str(e), "error")

        rbac_val = conf.getboolean("webserver", "rbac")
        data = {
            "summary": {"passed": passed, "updated": updated.isoformat()},
            "reports": reports,
            "rbac": rbac_val,
        }
        return data

    @expose("/")
    def list(self):
        return self.render_template("status.html", content=self.reports_data())


class ReportsView(AppBuilderBaseView):
    route_base = "/rb/reports"

    @expose("/")
    def list(self):
        return self.render_template("reports.html", content=VariablesReportRepo.list())

    @expose("/<string:report_name>/trigger/", methods=["GET"])
    def trigger(self, report_name):
        r = Report(report_name)
        r.trigger_dag()
        flash(f"Triggered report: {report_name}", "info")
        return redirect(url_for("ReportsView.list"))

    @expose("/<string:report_name>/delete/", methods=["POST"])
    def delete(self, report_name):
        r = Report(report_name)
        r.delete_report_variable(VariablesReportRepo.report_prefix)
        r.delete_dag()
        flash(f"Deleted report: {report_name}", "info")
        return redirect(url_for("ReportsView.list"))

    @expose("/paused", methods=["POST"])
    def pause_dag(self):
        r_args = request.args
        report_name = r_args.get("report_name")
        r = Report(report_name)
        if r_args.get("is_paused") == "true":
            r.activate_dag()
        else:
            r.pause_dag()
        return "OK"


class ReportForm(DynamicForm):
    report_id = HiddenField()
    report_title = StringField(
        ("Title"),
        description="Title will be used as the report's name",
        widget=BS3TextFieldWidget(),
        validators=[DataRequired()],
    )
    description = TextAreaField(
        ("Description"), widget=BS3TextAreaFieldWidget(), validators=[DataRequired()]
    )
    owner_name = StringField(
        ("Owner Name"), widget=BS3TextFieldWidget(), validators=[DataRequired()]
    )
    owner_email = StringField(
        ("Owner Email"),
        description="Owner email will be added to the subscribers list",
        widget=BS3TextFieldWidget(),
        validators=[DataRequired(), Email()],
    )
    subscribers = StringField(
        ("Subscribers"),
        description=(
            "List of comma separeted emails that should receive email\
             notifications. Automatically adds owner email to this list."
        ),
        widget=BS3TextFieldWidget(),
    )
    tests = SelectMultipleField(
        ("Tests"),
        description=(
            "List of the tests to include in the report. Only includes\
         tasks that have ran in airflow."
        ),
        choices=get_all_test_choices(),
        widget=Select2ManyWidget(),
        validators=[DataRequired()],
    )
    schedule_type = SelectField(
        ("Schedule"),
        description=("Select how you want to schedule the report"),
        choices=[
            ("manual", "None (Manual triggering)"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("custom", "Custom (Cron)"),
        ],
        widget=Select2Widget(),
        validators=[DataRequired()],
    )
    schedule_time = TimeField(
        "Time",
        description="Note that time zone being used is navBar's Timezone.",
        render_kw={"class": "form-control"},
        validators=[DataRequired()],
    )
    schedule_timezone = SelectField(
        "Timezone",
        description="Note that time zone being used is your navBar's Timezone.",
        choices=[(elem, elem) for elem in pendulum.timezones],
        widget=Select2Widget(),
        validators=[DataRequired()],
    )
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
        validators=[DataRequired()],
    )
    schedule_custom = StringField(
        ("Cron schedule"),
        description=(
            'Enter cron schedule (e.g. "0 0 * * *").\
         Note that time zone being used is UTC.'
        ),
        widget=BS3TextFieldWidget(),
        validators=[DataRequired()],
    )


class NewReportFormView(SimpleFormView):
    route_base = "/rb/report/new"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "New Report"
    form_fieldsets = form_fieldsets_config
    message = "Report submitted"

    # We're going to override form_get to preprocess
    # the form and refresh all its test choices
    def form_get(self, form):
        form.tests.choices = get_all_test_choices()
        return form

    @expose("/", methods=["GET"])
    @has_access
    def this_form_get(self):
        return super().this_form_get()

    @expose("/", methods=["POST"])
    @has_access
    def form_post(self):
        form = self.form.refresh()
        report_saver = ReportFormSaver(form)
        form_submitted = report_saver.extract_report_data_into_airflow(
            report_exists=False
        )
        # post process form
        if form_submitted:
            flash(self.message, "info")
            if request.args.get("next"):
                return redirect(url_for(request.args.get("next")))
            return redirect(url_for("ReportsView.list"))
        else:
            return self.this_form_get()


class EditReportFormView(SimpleFormView):
    route_base = "/rb/report"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "Edit Report"
    form_fieldsets = form_fieldsets_config
    message = "Report submitted"

    @expose("/<string:report_title>/edit", methods=["GET"])
    @has_access
    def this_form_get(self, report_title):
        self._init_vars()
        form = self.form.refresh()
        form = self.form_get(form, report_title)
        form.tests.choices = get_all_test_choices()
        if form:
            widgets = self._get_edit_widget(form=form)
            self.update_redirect()
            return self.render_template(
                self.form_template,
                title=self.form_title,
                widgets=widgets,
                appbuilder=self.appbuilder,
            )
        flash(f"report title ({report_title}) not found.", "error")
        return redirect(url_for("ReportsView.list"))

    def form_get(self, form, report_title):
        # !get report by report_title and prefill form with its values
        requested_report = {}
        for report in VariablesReportRepo.list():
            if str(report.report_title_id) == report_title:
                requested_report = report

        if requested_report:
            form = ReportFormSaver.load_form(form, requested_report)
            return form
        return None

    @expose("/<string:report_title>/edit", methods=["POST"])
    @has_access
    def form_post(self, report_title):
        form = self.form.refresh()
        report_saver = ReportFormSaver(form)
        form_submitted = report_saver.extract_report_data_into_airflow(
            report_exists=True
        )
        # post process form
        if form_submitted:
            flash(self.message, "info")
            return redirect(url_for("ReportsView.list", filename="reports"))
        else:
            return self.this_form_get(report_title)
