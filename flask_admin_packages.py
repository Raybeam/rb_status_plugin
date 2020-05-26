from lumen_plugin.views_no_rbac import (
    LumenStatusViewAdmin,
    LumenReportsViewAdmin,
    LumenReportMgmtViewAdmin,
)
from lumen_plugin.report import Report
from airflow.settings import Session

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

v_admin_reports_mgmt_package = LumenReportMgmtViewAdmin(
    Report,
    Session,
    category="Lumen",
    name="Report Management View",
    url="lumen/report_mgmt",
)
