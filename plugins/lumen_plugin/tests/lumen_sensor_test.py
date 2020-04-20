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

    dag = DAG('adhoc_Airflow', schedule_interval=None, default_args=default_args)

    def __create_dummy_op(self, state, dag):
        dummy = DummyOperator(
            task_id=f'dummy_{state}',
            dag=dag
        )
        return dummy

    def __create_sensor(self, state):
        sensor = LumenSensor(
            task_id="test_%s" % state,
            test_name=f"{self.dag.dag_id}.dummy_{state}"
        )
        return sensor

    def __create_context_with_state(self, task, state):
        ti = TaskInstance(task=task, execution_date=datetime.now())
        ti.set_state(state)
        context = ti.get_template_context()
        return context

    def test_success(self):
        # test that LumenOperator correctly interprets successful test
        expected_response = True
        state = State.SUCCESS

        dummy_success = self.__create_dummy_op(state, self.dag)
        sensor = self.__create_sensor(state)

        context = self.__create_context_with_state(dummy_success, state)
        result = sensor.poke(context=context)
        self.assertEqual(expected_response, result)

    def test_failures(self):
        # test that LumenOperator correctly interprets failed test
        expected_response = ValueError
        state = State.FAILED

        dummy_failure = self.__create_dummy_op(state, self.dag)
        sensor = self.__create_sensor(state)

        context = self.__create_context_with_state(dummy_failure, state)
        self.assertRaises(ValueError, sensor.poke, context)

    def test_intermittant_states(self):
        expected_response = False
        state = State.RUNNING

        dummy_failure = self.__create_dummy_op(state, self.dag)
        sensor = self.__create_sensor(state)

        context = self.__create_context_with_state(dummy_failure, state)
        result = sensor.poke(context=context)
        self.assertEqual(expected_response, result)


if __name__ == "__main__":
    unittest.main()