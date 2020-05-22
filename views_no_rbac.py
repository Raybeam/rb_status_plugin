from flask_admin import BaseView, expose
from flask_admin.form import rules
from lumen_plugin.report_model import ReportModel

from lumen_plugin.views import (
    LumenStatusView,
    LumenReportsView,
)
from lumen_plugin.report_repo import VariablesReportRepo


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
    def test(self):
        return self.render('no_rbac/reports.html', content=VariablesReportRepo.list())


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
