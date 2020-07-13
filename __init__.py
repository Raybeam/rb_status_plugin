from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from rb_status_plugin.core.views import (
    StatusView,
    ReportsView,
    NewReportFormView,
    EditReportFormView,
)
from rb_status_plugin.sensors.status_sensor import StatusSensor
from rb_status_plugin.core.flask_admin_packages import (
    v_admin_status_package,
    v_admin_reports_package,
    v_admin_reports_mgmt_package,
)

v_appbuilder_status_view = StatusView()
v_appbuilder_status_package = {
    "name": "Status Page",
    "category": "Status",
    "view": v_appbuilder_status_view,
}

v_appbuilder_reports_view = ReportsView()
v_appbuilder_reports_package = {
    "name": "Reports",
    "category": "Status",
    "view": v_appbuilder_reports_view,
}

v_appbuilder_new_report_form_view = NewReportFormView()
v_appbuilder_new_report_form_package = {
    "name": "New Report Form",
    "category": None,
    "view": v_appbuilder_new_report_form_view,
}

v_appbuilder_edit_report_form_view = EditReportFormView()
v_appbuilder_edit_report_form_package = {
    "name": "Edit Report Form",
    "category": None,
    "view": v_appbuilder_edit_report_form_view,
}


# Creating a flask blueprint to intergrate the templates and static folder
bp = Blueprint(
    "rb_status",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/rb",
)


class RbStatusPlugin(AirflowPlugin):
    name = "rb_status_plugin"
    operators = []
    sensors = [StatusSensor]
    flask_blueprints = [bp]
    hooks = []
    executors = []
    macros = []
    admin_views = [
        v_admin_status_package,
        v_admin_reports_package,
        v_admin_reports_mgmt_package,
    ]
    menu_links = []
    appbuilder_views = [
        v_appbuilder_status_package,
        v_appbuilder_reports_package,
        v_appbuilder_new_report_form_package,
        v_appbuilder_edit_report_form_package,
    ]
    appbuilder_menu_items = []

