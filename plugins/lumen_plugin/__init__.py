from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from plugins.lumen_plugin import test_data


# Creating a flask appbuilder BaseView
class LumenBuilderBaseView(AppBuilderBaseView):
    # !temporary method
    def reports_data(self):
        data = {
            # TODO: summary must be calculated
            "summary": {
                "passed": test_data.dummy_reports[0]["passed"],
                "updated": test_data.dummy_reports[0]["updated"],
            },
            "reports": test_data.dummy_reports,
        }
        return data

    @expose("/")
    def list(self):
        return self.render_template("index.html", content=self.reports_data())


v_appbuilder_view = LumenBuilderBaseView()
v_appbuilder_package = {
    "name": "Status Page",
    "category": "Lumen",
    "view": v_appbuilder_view,
}

# Creating a flask appbuilder BaseView
class LumenBuilderMgmtView(AppBuilderBaseView):
    @expose("/mgmt")
    def list(self):
        return self.render_template("management.html", content="Hello Galaxy!")


v_appbuilder_mgmt_view = LumenBuilderMgmtView()
v_appbuilder_mgmt_package = {
    "name": "Reports Management",
    "category": "Lumen",
    "view": v_appbuilder_mgmt_view,
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
    appbuilder_views = [v_appbuilder_package, v_appbuilder_mgmt_package]
    appbuilder_menu_items = []
