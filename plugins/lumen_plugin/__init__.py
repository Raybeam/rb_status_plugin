from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from plugins.lumen_plugin import test_data


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


# class LumenReportForm():
#     @expose("/reports/<string:id>")
#     def list(self):


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
    appbuilder_views = [v_appbuilder_status_package, v_appbuilder_reports_package]
    appbuilder_menu_items = []
