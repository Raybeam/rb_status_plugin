from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask import flash
from flask_appbuilder import SimpleFormView
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    BS3TextAreaFieldWidget,
    Select2ManyWidget,
)
from wtforms import StringField, TextAreaField, SelectMultipleField
from plugins.lumen_plugin import test_data


from flask_appbuilder.security.decorators import has_access

# from airflow import appbuilder


from lumen_plugin.operators.lumen_operator import (
    LumenOperator,
)

# Creating a flask appbuilder BaseView
class LumenStatusView(AppBuilderBaseView):
    route_base = "/lumen"

    # !temporary method
    def reports_data(self):
        data = {
            # TODO: summary must be calculated
            "summary": {
                "passed": test_data.dummy_report_runs[0]["passed"],
                "updated": test_data.dummy_report_runs[0]["updated"],
            },
            "reports": test_data.dummy_report_runs,
        }
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
    schedule = StringField(
        ("Schedule"), description=("Cron time string"), widget=BS3TextFieldWidget()
    )
    owner_name = StringField(("Owner Name"), widget=BS3TextFieldWidget())
    owner_email = StringField(("Owner Email"), widget=BS3TextFieldWidget())
    emails = StringField(
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


class NewReportFormView(SimpleFormView):
    route_base = "/lumen/report"
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
    form = ReportForm
    form_title = "New Report"
    message = "My form submitted"

    route_base = "/lumen/report"

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
            form.emails.data = ", ".join(requested_report["emails"])
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
    static_url_path="/lumen/static",
)


class LumenPlugin(AirflowPlugin):
    name = "lumen"
    operators = [LumenOperator]
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
