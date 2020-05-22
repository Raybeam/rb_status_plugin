from flask_admin import BaseView, expose
from flask_admin.form import rules
from lumen_plugin.report_model import ReportModel

from lumen_plugin.views import (
    LumenStatusView,
    LumenReportsView,
)
from lumen_plugin.report_repo import VariablesReportRepo
from lumen_plugin.report import Report
from flask import flash, redirect, url_for, request

lumen_status_view_rbac = LumenStatusView()
lumen_reports_view_rbac = LumenReportsView()


class LumenStatusViewAdmin(BaseView):
    @expose('/')
    def test(self):
        return self.render(
            "no_rbac/status.html",
            content=lumen_status_view_rbac.reports_data()
        )


class LumenReportsViewAdmin(BaseView):
    @expose('/')
    def list(self):
        return self.render(
            'no_rbac/reports.html',
            content=VariablesReportRepo.list()
        )

    @expose("/<string:report_name>/trigger/", methods=["GET"])
    def trigger(self, report_name):
        r = Report(report_name)
        r.trigger_dag()
        flash(f"Triggered report: {report_name}", "info")
        return redirect(url_for("lumen/reports.list"))

    @expose("/<string:report_name>/delete/", methods=["POST"])
    def delete(self, report_name):
        r = Report(report_name)
        r.delete_report_variable(VariablesReportRepo.report_prefix)
        r.delete_dag()
        flash(f"Deleted report: {report_name}", "info")
        return redirect(url_for("lumen/reports.list"))

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


class LumenReportMgmtViewAdmin(ReportModel):
    can_delete = False
    create_template = 'no_rbac/report_create_form.html'
    edit_template = 'no_rbac/report_edit_form.html'
    form_rules = [
        rules.FieldSet((
            'report_id',
        ), ''),
        rules.FieldSet((
            'report_title',
            'description',
            'owner_name',
            'owner_email',
            'subscribers'
        ), 'General'),
        rules.FieldSet((
            'schedule_type',
            'schedule_time',
            'schedule_week_day',
            'schedule_custom'
        ), 'Schedule'),
        rules.FieldSet((
            'tests',
        ), 'Tests')
    ]
