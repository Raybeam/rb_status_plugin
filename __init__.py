from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from airflow.settings import Session
from lumen_plugin.views import (
    LumenStatusView,
    LumenReportsView,
    NewReportFormView,
    EditReportFormView,
)
from lumen_plugin.sensors.lumen_sensor import LumenSensor
from lumen_plugin.views_no_rbac import (
    LumenStatusViewAdmin,
    LumenReportsViewAdmin,
    LumenReportMgmtViewAdmin,
)
from lumen_plugin.report import Report


v_appbuilder_status_view = LumenStatusView()
v_appbuilder_status_package = {
    "name": "Status Page",
    "category": "Lumen",
    "view": v_appbuilder_status_view,
}

v_appbuilder_reports_view = LumenReportsView()
v_appbuilder_reports_package = {
    "name": "Reports",
    "category": "Lumen",
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
    "lumen",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/lumen",
)

v_admin_status_package = LumenStatusViewAdmin(
    category="Lumen",
    name="Status Page",
    endpoint='lumen/status'
)

v_admin_reports_package = LumenReportsViewAdmin(
    category="Lumen",
    name="Reports",
    endpoint='lumen/reports'
)

v_admin_my_model_view = LumenReportMgmtViewAdmin(
    Report,
    Session,
    category="Lumen",
    name="Report Management View",
    url="lumen/report_mgmt",
)

class LumenPlugin(AirflowPlugin):
    name = "lumen_plugin"
    operators = []
    sensors = [LumenSensor]
    flask_blueprints = [bp]
    hooks = []
    executors = []
    macros = []
    admin_views = [
        v_admin_status_package,
        v_admin_reports_package,
        v_admin_my_model_view
    ]
    menu_links = []
    appbuilder_views = [
        v_appbuilder_status_package,
        v_appbuilder_reports_package,
        v_appbuilder_new_report_form_package,
        v_appbuilder_edit_report_form_package,
    ]
    appbuilder_menu_items = []
