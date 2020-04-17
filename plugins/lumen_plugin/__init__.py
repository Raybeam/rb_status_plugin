from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

from lumen_plugin.sensors.lumen_sensor import (
    LumenSensor,
)

# Creating a flask appbuilder BaseView
class LumenBuilderBaseView(AppBuilderBaseView):
    @expose("/")
    def list(self):
        return self.render_template("index.html", content="Hello galaxy!")


v_appbuilder_view = LumenBuilderBaseView()
v_appbuilder_package = {
    "name": "Lumen View",
    "category": "Lumen",
    "view": v_appbuilder_view,
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
    sensors = [LumenSensor]
    flask_blueprints = [bp]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    menu_links = []
    appbuilder_views = [v_appbuilder_package]
    appbuilder_menu_items = []
