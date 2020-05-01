from plugins.lumen_plugin.sensors.lumen_sensor import LumenSensor
from airflow.operators.dummy_operator import DummyOperator
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

    lumen_dag = DAG(
        "lumen_dag",
        schedule_interval=None,
        default_args=default_args
    )
    test_dag = DAG(
        "test_dag",
        schedule_interval=None,
        default_args=default_args
    )

    def __create_dummy_op(self, state, dag):
        dummy = DummyOperator(task_id=f"dummy_{state}", dag=dag)
        return dummy

    def __create_sensor(self, test, dag):
        sensor = LumenSensor(
            task_id=f"test_{test.dag_id}.{test.task_id}",
            test_dag_id=f"{test.dag_id}",
            test_task_id=f"{test.task_id}",
            dag=dag
        )
        return sensor

    def __create_invalid_test_sensor(self, test, dag):
        sensor = LumenSensor(
            task_id=f"test_{test.dag_id}.{test.task_id}",
            test_dag_id=f"does_not_exist",
            test_task_id=f"imaginary_task",
            dag=dag
        )
        return sensor

    def __create_task_instance(self, task):
        ti = TaskInstance(task=task, execution_date=datetime.now())
        return ti

    def __create_task_instance_with_state(self, task, state):
        ti = self.__create_task_instance(task)
        ti.set_state(state)
        return ti

    def test_successful(self):
        # test that LumenSensor processes a successful test operation
        # and stops poking (returning True value for operator and test)
        expected_response = True
        state = State.SUCCESS

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_sensor(dummy_success, self.lumen_dag)

        dummy_ti = self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        op_result = sensor.poke(context=sensor_ti.get_template_context())
        test_result = sensor_ti.xcom_pull(key=f"{sensor_ti.dag_id}.{sensor_ti.task_id}")
        self.assertEqual(expected_response, (test_result and op_result))

    def test_failure(self):
        # test that LumenSensor processes a failed test operation
        # and stops poking (returning True value for operator and test)
        expected_response = False
        state = State.FAILED

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_sensor(dummy_success, self.lumen_dag)

        dummy_ti = self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        op_result = sensor.poke(context=sensor_ti.get_template_context())
        test_result = sensor_ti.xcom_pull(key=f"{sensor_ti.dag_id}.{sensor_ti.task_id}")
        self.assertEqual(expected_response, (test_result and op_result))

    def test_unknown(self):
        # test that LumenSensor processes a unknown test operation
        # (returning False value for operator and Unknown for test)
        expected_response = None
        state = State.SUCCESS

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_invalid_test_sensor(dummy_success, self.lumen_dag)

        dummy_ti = self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        #op_result = sensor.poke(context=sensor_ti.get_template_context())
        test_result = sensor_ti.xcom_pull(key=f"{sensor_ti.dag_id}.{sensor_ti.task_id}")
        self.assertRaises(AttributeError, sensor.poke, sensor_ti.get_template_context())
        self.assertEqual(expected_response, test_result)


if __name__ == "__main__":
    unittest.main()
