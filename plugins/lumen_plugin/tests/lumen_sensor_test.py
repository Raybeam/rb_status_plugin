from airflow import DAG
from airflow.utils.db import create_session
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from lumen_plugin.sensors.lumen_sensor import LumenSensor
from airflow.utils.db import create_session

import unittest


class CreateLumenSensorsTestDag:
    # create and run temporary dag
    def __init__(self):
        self.dag_name = "lumen_sensor_test"
        self.default_args = {
            "owner": "airflow",
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "schedule_interval": None,
            "retries": 1,
            "start_date": datetime(2019, 1, 1),
            "retry_delay": timedelta(minutes=5),
        }

    def test_success_fail(self, state):
        # helper to pass or fail a task instance
        if state:
            return True
        else:
            raise ValueError('Task instance failed successfully!')


    def create_dag(self, task_state):
        # create dag with success and failure instances
        dag = DAG(self.dag_name, default_args=self.default_args)

        with dag:
            start = DummyOperator(task_id="start_dag")
            example_test = PythonOperator(
                task_id="test_expected_to_%s" % "succeed" if task_state else "fail",
                python_callable=self.test_success_fail,
                op_kwargs={"state": task_state},
            )
            start >> example_test

        return dag


def run_lumen_sensor(task_state):
    # run Lumen sensor against temporary dag and show results
    my_sensor =  LumenSensor(
        task_id="test_%s" % task_state,
        test_name="lumen_sensor_test.%s" % ("test_expected_to_%s" % "succeed" if task_state else "fail"),
    )
    return my_sensor.execute(context={})


# class DeleteLumenSensorsTestDag(unittest.TestCase):
#     # delete temporary dag
#     dag_name = "lumen_sensor_test"
#     query = {'delete from xcom where dag_id = "' + dag_name + '"',
#             'delete from task_instance where dag_id = "' + dag_name + '"',
#             'delete from sla_miss where dag_id = "' + dag_name + '"',
#             'delete from log where dag_id = "' + dag_name + '"',
#             'delete from job where dag_id = "' + dag_name + '"',
#             'delete from dag_run where dag_id = "' + dag_name + '"',
#             'delete from dag where dag_id = "' + dag_name + '"' 
#     }
#     def delete_dag(self):
#         with create_session() as curr_session:
#             curr_session.delete(Dag)


class LumenSensorTest(unittest.TestCase):
    def test_success(self):
        # test that LumenSensor correctly interprets successful test
        task_state = True
        expected_response = True
        success_dag = CreateLumenSensorsTestDag()
        success_dag.create_dag(task_state=task_state)
        lumen_sensor_response = run_lumen_sensor(task_state=task_state)
        self.assertEqual(expected_response, lumen_sensor_response)

    def test_failure(self):
        # test that LumenSensor correctly interprets failed test
        task_state = False
        expected_response = False
        failure_dag = CreateLumenSensorsTestDag()
        failure_dag.create_dag(task_state=task_state)
        lumen_sensor_response = run_lumen_sensor(task_state=task_state)
        self.assertEqual(expected_response, lumen__response)
