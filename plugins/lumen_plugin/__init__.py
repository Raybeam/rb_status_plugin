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

# from airflow import appbuilder


# Creating a flask appbuilder BaseView
class LumenStatusView(AppBuilderBaseView):
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

    @expose("/")
    def list(self):
        return self.render_template("status.html", content=self.reports_data())


v_appbuilder_status_view = LumenStatusView()
v_appbuilder_status_package = {
    "name": "Status Page",
    "category": "Lumen",
    "view": v_appbuilder_status_view,
}


class LumenReportsView(AppBuilderBaseView):
    @expose("/reports")
    def list(self):
        return self.render_template("reports.html", content=test_data.dummy_reports)


v_appbuilder_reports_view = LumenReportsView()
v_appbuilder_reports_package = {
    "name": "Reports",
    "category": "Lumen",
    "view": v_appbuilder_reports_view,
}


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
        choices=[(1, "Test 1"), (2, "Test 2")],
        widget=Select2ManyWidget(),
    )


class ReportFormView(SimpleFormView):
    form = ReportForm
    form_title = "Report Form"
    message = "My form submitted"

    def form_get(self, form):
        form.title.data = "This was prefilled"

    def form_post(self, form):
        # post process form
        flash(self.message, "info")


# appbuilder.add_view_no_menu(ReportFormView())
v_appbuilder_report_form_view = ReportFormView()
v_appbuilder_report_form_package = {
    # "name": None,
    # "category": None,
    "name": "Report Form",
    "category": "Lumen",
    "view": v_appbuilder_report_form_view,
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
    operators = []
    flask_blueprints = [bp]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    menu_links = []
    appbuilder_views = [
        v_appbuilder_status_package,
        v_appbuilder_reports_package,
        v_appbuilder_report_form_package,
        # v_appbuilder_report_form_view,
    ]
    appbuilder_menu_items = []
