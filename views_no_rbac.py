from flask_admin import BaseView, expose

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
        return self.render('no_rbac/reports.html', context=VariablesReportRepo.list())
