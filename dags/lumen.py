from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from airflow.utils.db import create_session

from plugins.lumen_plugin.report_repo import VariablesReportRepo
from plugins.lumen_plugin.sensors.lumen_sensor import LumenSensor

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

        for test in report.tests:
            t1 = LumenSensor(
                task_id="test_%s" % test,
                test_dag_id=test.split('.')[0],
                test_task_id=test.split('.')[1]
            )
            start >> t1 >> send_report

    return dag


report = []
with create_session() as session:
    repos = VariablesReportRepo(session)
    for report in repos.list():
        globals()[report.name] = create_dag(report, default_args)
