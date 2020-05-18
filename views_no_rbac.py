from flask_admin import BaseView, expose

from lumen_plugin.views import (
    LumenStatusView,
    LumenReportsView,
    NewReportFormView,
)
from lumen_plugin.report_repo import VariablesReportRepo


lumen_status_view_rbac = LumenStatusView()
lumen_reports_view_rbac = LumenReportsView()
lumen_new_report_form_view_rbac = NewReportFormView()

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

class NewReportFormViewAdmin(BaseView):
    @expose("/", methods=["GET"])
    def this_form_get(self):
        return lumen_new_report_form_view_rbac.this_form_get()

    @expose("/", methods=["POST"])
    def form_post(self):
        return lumen_new_report_form_view_rbac.this.form_post()
