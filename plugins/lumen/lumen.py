from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

from airflow.executors.base_executor import BaseExecutor
# Importing base classes that we need to derive
from airflow.hooks.base_hook import BaseHook
from airflow.models.baseoperator import BaseOperator
# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
from airflow.sensors.base_sensor_operator import BaseSensorOperator

# Creating a flask appbuilder BaseView
class LumenBuilderBaseView(AppBuilderBaseView):

    @expose("/")
    def list(self):
        return self.render_template("index.html", content="Hello galaxy!")


v_appbuilder_view = LumenBuilderBaseView()
v_appbuilder_package = {"name": "Lumen View",
                        "category": "Lumen",
                        "view": v_appbuilder_view}

# Creating a flask blueprint to intergrate the templates and static folder
bp = Blueprint(
    "lumen", __name__,
    template_folder='templates',  # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/lumen/static')


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "lumen"
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
    # appbuilder_menu_items = []
