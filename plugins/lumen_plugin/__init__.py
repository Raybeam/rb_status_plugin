from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint, flash
from flask_appbuilder import SimpleFormView
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    BS3TextAreaFieldWidget,
    Select2ManyWidget,
    Select2Widget,
)
from wtforms import (
    StringField,
    TextAreaField,
    SelectMultipleField,
    SelectField,
    FormField,
)
from wtforms_components import TimeField
from plugins.lumen_plugin import test_data
from plugins.lumen_plugin.report_repo import VariablesReportRepo
from plugins.lumen_plugin.report_instance import ReportInstance
from lumen_plugin.sensors.lumen_sensor import LumenSensor

from flask_appbuilder.security.decorators import has_access

import logging

log = logging.getLogger(__name__)

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
        log.info("Loading reports")
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
                    "owner_email": report.emails,
                }

                r["errors"] = ri.errors()
                if len(r["errors"]) > 0:
                    passed = False

                log.info(r)
                reports.append(r)
            except Exception as e:
                log.exception(e)
                log.error("Failed to generate report: " + str(e))
                flash("Failed to generate report: " + str(e), "error")

        data = {"summary": {"passed": passed, "updated": updated}, "reports": reports}
        return data

    @expose("/status")
    def list(self):
        return self.render_template("status.html", content=self.reports_data())


v_appbuilder_status_view = LumenStatusView()
v_appbuilder_status_package = {
    "name": "Status Page",
    "category": "Lumen",
    "view": v_appbuilder_status_view,
}


class LumenReportsView(AppBuilderBaseView):
    route_base = "/lumen"

    @expose("/reports")
    def list(self):
        return self.render_template("reports.html", content=test_data.dummy_reports)


v_appbuilder_reports_view = LumenReportsView()
v_appbuilder_reports_package = {
    "name": "Reports",
    "category": "Lumen",
    "view": v_appbuilder_reports_view,
}

test_choices = []
for test in test_data.dummy_tests:
    test_choices.append((test["id"], test["name"]))


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
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        widget=Select2Widget(),
    )
    schedule_custom = StringField(("Cron schedule"), widget=BS3TextFieldWidget())


class NewReportFormView(SimpleFormView):
    route_base = "/lumen/report"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "New Report"
    message = "My form submitted"

    @expose("/new", methods=["GET"])
    @has_access
    def this_form_get(self):
        return super().this_form_get()

    def form_post(self, form):
        # post process form
        flash(self.message, "info")


v_appbuilder_new_report_form_view = NewReportFormView()
v_appbuilder_new_report_form_package = {
    "name": None,
    "category": None,
    "view": v_appbuilder_new_report_form_view,
}


class EditReportFormView(SimpleFormView):
    route_base = "/lumen/report"
    form_template = "report_form.html"
    form = ReportForm
    form_title = "New Report"
    form_fieldsets = [
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
    message = "My form submitted"

    @expose("/<string:report_id>/edit", methods=["GET"])
    @has_access
    def this_form_get(self, report_id):
        self._init_vars()
        form = self.form.refresh()

        self.form_get(form, report_id)
        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    def form_get(self, form, report_id):
        # !get report by report_id and prefill form with its values
        requested_report = {}
        for report in test_data.dummy_reports:
            if str(report["id"]) == report_id:
                requested_report = report

        if requested_report:
            form.title.data = requested_report["title"]
            form.description.data = requested_report["description"]
            form.schedule.data = requested_report["schedule"]
            form.subscribers.data = ", ".join(requested_report["subscribers"])
            form.owner_name.data = requested_report["owner_name"]
            form.owner_email.data = requested_report["owner_email"]
            form.tests.data = [str(test["id"]) for test in requested_report["tests"]]

    def form_post(self, form):
        # post process form
        flash(self.message, "info")


v_appbuilder_edit_report_form_view = EditReportFormView()
v_appbuilder_edit_report_form_package = {
    "name": None,
    "category": None,
    "view": v_appbuilder_edit_report_form_view,
}


# Creating a flask blueprint to intergrate the templates and static folder
bp = Blueprint(
    "lumen",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/lumen_plugin/static",
)


class LumenPlugin(AirflowPlugin):
    name = "lumen"
    operators = []
    sensors = [LumenSensor]
    flask_blueprints = [bp]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    menu_links = []
    appbuilder_views = [
        v_appbuilder_status_package,
        v_appbuilder_reports_package,
        v_appbuilder_new_report_form_package,
        v_appbuilder_edit_report_form_package,
    ]
    appbuilder_menu_items = []
