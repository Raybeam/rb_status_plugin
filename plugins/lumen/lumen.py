from flask import Blueprint
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

from airflow.executors.base_executor import BaseExecutor
# Importing base classes that we need to derive
from airflow.hooks.base_hook import BaseHook
from airflow.models.baseoperator import BaseOperator
# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
from airflow.sensors.base_sensor_operator import BaseSensorOperator

# # Will show up under airflow.hooks.test_plugin.PluginHook
# class PluginHook(BaseHook):
#     pass


# # Will show up under airflow.operators.test_plugin.PluginOperator
# class PluginOperator(BaseOperator):
#     pass


# # Will show up under airflow.sensors.test_plugin.PluginSensorOperator
# class PluginSensorOperator(BaseSensorOperator):
#     pass


# # Will show up under airflow.executors.test_plugin.PluginExecutor
# class PluginExecutor(BaseExecutor):
#     pass


# # Will show up under airflow.macros.test_plugin.plugin_macro
# def plugin_macro():
#     pass


# Creating a flask appbuilder BaseView
class PluginTestAppBuilderBaseView(AppBuilderBaseView):

    @expose("/")
    def list(self):
        return self.render_template("index.html", content="Hello galaxy!")


v_appbuilder_view = PluginTestAppBuilderBaseView()
v_appbuilder_package = {"name": "Test View",
                        "category": "Test Plugin",
                        "view": v_appbuilder_view}

# Creating a flask blueprint to intergrate the templates and static folder
bp = Blueprint(
    "lumen", __name__,
    template_folder='templates',  # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/static/lumen')


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "lumen"
    # operators = [PluginOperator]
    # sensors = [PluginSensorOperator]
    # hooks = [PluginHook]
    # executors = [PluginExecutor]
    # macros = [plugin_macro]
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
    # appbuilder_menu_items = []


# class MockPluginA(AirflowPlugin):
#     name = 'plugin-a'


# class MockPluginB(AirflowPlugin):
#     name = 'plugin-b'


# class MockPluginC(AirflowPlugin):
#     name = 'plugin-c'