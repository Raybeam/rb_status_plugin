from flask_admin import BaseView, expose
from flask_admin.form import rules

from flask import flash, redirect, url_for, request

from rb_status_plugin.core.report_model import ReportModel
from rb_status_plugin.core.report_repo import VariablesReportRepo
from rb_status_plugin.core.report import Report
from rb_status_plugin.core.views import (
    StatusView,
    ReportsView,
)

status_view_rbac = StatusView()
reports_view_rbac = ReportsView()


class StatusViewAdmin(BaseView):
    @expose("/")
    def test(self):
        return self.render(
            "no_rbac/status.html", content=status_view_rbac.reports_data()
        )


class ReportsViewAdmin(BaseView):
    @expose("/")
    def list(self):
        return self.render("no_rbac/reports.html", content=VariablesReportRepo.list())

    @expose("/<string:report_name>/trigger/", methods=["GET"])
    def trigger(self, report_name):
        r = Report(report_name)
        r.trigger_dag()
        flash(f"Triggered report: {report_name}", "info")
        return redirect(url_for("rb/reports.list"))

    @expose("/<string:report_name>/delete/", methods=["POST"])
    def delete(self, report_name):
        r = Report(report_name)
        r.delete_report_variable(VariablesReportRepo.report_prefix)
        r.delete_dag()
        flash(f"Deleted report: {report_name}", "info")
        return redirect(url_for("rb/reports.list"))

    @expose("/paused", methods=["POST"])
    def pause_dag(self):
        r_args = request.args
        report_name = r_args.get("report_name")
        r = Report(report_name)
        if r_args.get("is_paused") == "true":
            r.activate_dag()
        else:
            r.pause_dag()
        return "OK"


class ReportMgmtViewAdmin(ReportModel):
    can_delete = False
    create_template = "no_rbac/report_create_form.html"
    edit_template = "no_rbac/report_edit_form.html"
    form_rules = [
        rules.FieldSet(("report_id",), ""),
        rules.FieldSet(
            ("report_title", "description", "owner_name", "owner_email", "subscribers"),
            "General",
        ),
        rules.FieldSet(
            ("schedule_type", "schedule_time", "schedule_week_day", "schedule_custom"),
            "Schedule",
        ),
        rules.FieldSet(("tests",), "Tests"),
    ]

    # We're doing this to hide the view from the main
    # menu and keep access in the /reports/ endpoint
    def is_visible(self):
        return False
