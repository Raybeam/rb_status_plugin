from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask import flash

from lumen_plugin.report_repo import VariablesReportRepo
from lumen_plugin.report_instance import ReportInstance

import logging

# Creating a flask appbuilder BaseView
class LumenStatusView(AppBuilderBaseView):
    """
    LumenStatusView is responsible for Lumen Status Page
    """

    route_base = "/lumen"

    def reports_data(self):
        """
        Generate reports data.
        It retrieves a list of reports, generates summary status
        and pass it all down to the template
        """
        reports = []
        passed = True
        updated = None
        logging.debug("Loading reports")
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

                logging.info(r)
                reports.append(r)
            except Exception as e:
                logging.exception(e)
                logging.error("Failed to generate report: " + str(e))
                flash("Failed to generate report: " + str(e), "error")

        data = {"summary": {"passed": passed, "updated": updated}, "reports": reports}
        return data

    @expose("/status")
    def list(self):
        return self.render_template("status.html", content=self.reports_data())
