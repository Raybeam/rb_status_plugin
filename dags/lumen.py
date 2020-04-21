from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from airflow.utils.db import create_session

from plugins.lumen_plugin.report_repo import VariablesReportRepo

# Default settings applied to all tests
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "start_date": datetime(2019, 1, 1),
    "retry_delay": timedelta(minutes=5),
}


def create_dag(report, default_args):
    dag = DAG(
        report.dag_id, schedule_interval=report.schedule, default_args=default_args
    )

    with dag:
        start = DummyOperator(task_id="start_dag")
        send_report = DummyOperator(task_id="send_report")

        for t in report.tests:
            t1 = DummyOperator(task_id="test_%s" % t)
            start >> t1 >> send_report

    return dag


report = []
repos = VariablesReportRepo()
for report in repos.list():
    globals()[report.name] = create_dag(report, default_args)
