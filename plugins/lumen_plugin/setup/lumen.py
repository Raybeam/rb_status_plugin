from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from lumen_plugin.report_repo import VariablesReportRepo
from lumen_plugin.sensors.lumen_sensor import LumenSensor

# Default settings applied to all tests
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
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
                test_dag_id=test.split(".")[0],
                test_task_id=test.split(".")[1],
            )
            start >> t1 >> send_report

    return dag


report = []
for report in VariablesReportRepo.list():
    globals()[report.name] = create_dag(report, default_args)
