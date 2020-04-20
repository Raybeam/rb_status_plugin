from plugins.lumen_plugin.sensors.lumen_sensor import LumenSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.db import create_session
from airflow.models.taskinstance import TaskInstance
from datetime import datetime, timedelta
import unittest
from airflow.utils.state import State

from airflow import DAG

# Default settings applied to all tests
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "start_date": datetime(2020, 4, 19),
    "retry_delay": timedelta(minutes=5),
}

class LumenSensorTest(unittest.TestCase):
    def test_success(self):
        # test that LumenOperator correctly interprets successful test
        task_state = True
        expected_response = True
        dag = DAG('adhoc_Airflow', schedule_interval=None, default_args=default_args)
        dummy_success = DummyOperator(
            task_id='dummy_success',
            dag=dag
        )
        sensor = LumenSensor(
            task_id="test_%s" % task_state,
            test_name=f"adhoc_Airflow.dummy_success"
        )
        ti = TaskInstance(task=dummy_success, execution_date=datetime(2020, 4, 20))
        context = ti.get_template_context()
        result = sensor.poke(context=context)
        self.assertEqual(expected_response, result)

    def test_failure(self):
        # test that LumenOperator correctly interprets failed test
        task_state = False
        expected_response = False
        dag = DAG('adhoc_Airflow', schedule_interval=None, default_args=default_args)
        dummy_failure = DummyOperator(
            task_id='dummy_failure',
            dag=dag
        )
        sensor = LumenSensor(
            task_id="test_%s" % task_state,
            test_name=f"adhoc_Airflow.dummy_failure"
        )
        ti = TaskInstance(task=dummy_failure, execution_date=datetime(2020, 4, 20))
        context = ti.get_template_context()
        result = sensor.poke(context=context)
        self.assertEqual(expected_response, result)


if __name__ == "__main__":
    unittest.main()
