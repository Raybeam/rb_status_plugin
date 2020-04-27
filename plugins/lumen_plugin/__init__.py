from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint, flash
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from plugins.lumen_plugin.report_repo import VariablesReportRepo
from plugins.lumen_plugin.report_instance import ReportInstance


from lumen_plugin.sensors.lumen_sensor import LumenSensor
import logging

log = logging.getLogger(__name__)

# Creating a flask appbuilder BaseView
class LumenBuilderBaseView(AppBuilderBaseView):
    # !temporary method
    def reports_data(self):
        reports = []
        passed = True
        updated = None
        log.debug("Loading reports")
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

    @expose("/")
    def list(self):
        return self.render_template("index.html", content=self.reports_data())


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
