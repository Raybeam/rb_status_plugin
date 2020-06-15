from rb_status_plugin.core.views_no_rbac import (
    StatusViewAdmin,
    ReportsViewAdmin,
    ReportMgmtViewAdmin,
)
from rb_status_plugin.core.report import Report
from airflow.settings import Session

v_admin_status_package = StatusViewAdmin(
    category="Status", name="Status Page", endpoint="rb/status"
)

v_admin_reports_package = ReportsViewAdmin(
    category="Status", name="Reports", endpoint="rb/reports"
)

v_admin_reports_mgmt_package = ReportMgmtViewAdmin(
    Report,
    Session,
    category="Status",
    name="Report Management View",
    url="rb/report_mgmt",
)
