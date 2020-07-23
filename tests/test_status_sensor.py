from datetime import datetime, timedelta
import pytest

from airflow.operators.dummy_operator import DummyOperator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
from airflow import DAG

from rb_status_plugin.sensors.status_sensor import StatusSensor

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


@pytest.mark.compatibility
class TestSensor:
    rb_status_dag = DAG(
        "rb_status_dag", schedule_interval=None, default_args=default_args
    )
    test_dag = DAG("test_dag", schedule_interval=None, default_args=default_args)

    def __create_dummy_op(self, state, dag):
        dummy = DummyOperator(task_id=f"dummy_{state}", dag=dag)
        return dummy

    def __create_sensor(self, test, dag):
        sensor = StatusSensor(
            task_id=f"test_{test.dag_id}.{test.task_id}",
            test_dag_id=f"{test.dag_id}",
            test_task_id=f"{test.task_id}",
            dag=dag,
        )
        return sensor

    def __create_invalid_test_sensor(self, dag):
        sensor = StatusSensor(
            task_id="test_does_not_exist.imaginary_task",
            test_dag_id="does_not_exist",
            test_task_id="imaginary_task",
            dag=dag,
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
        # test that StatusSensor processes a successful test operation
        # and returns an operational success and test success
        expected_test_response = True
        expected_operational_response = True
        state = State.SUCCESS

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_sensor(dummy_success, self.rb_status_dag)

        self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        op_result = sensor.poke(context=sensor_ti.get_template_context())

        test_result = sensor_ti.xcom_pull(key="rb_status_test_task_status")

        assert expected_test_response == test_result
        assert expected_operational_response == op_result

    def test_failure(self):
        # test that StatusSensor processes a failed test operation
        # and returns an operational success and test failure
        expected_test_response = False
        expected_operational_response = True
        state = State.FAILED

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_sensor(dummy_success, self.rb_status_dag)

        self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        op_result = sensor.poke(context=sensor_ti.get_template_context())
        test_result = sensor_ti.xcom_pull(key="rb_status_test_task_status")

        assert expected_test_response == test_result
        assert expected_operational_response == op_result

    def test_intermittant_state(self):
        # tests that StatusSensor processes a test with
        # an intermittant state and will continue poking
        # until test is terminal
        expected_response = False
        state = State.RUNNING

        dummy_success = self.__create_dummy_op(state, self.test_dag)
        sensor = self.__create_sensor(dummy_success, self.rb_status_dag)

        self.__create_task_instance_with_state(dummy_success, state)
        sensor_ti = self.__create_task_instance(sensor)

        op_result = sensor.poke(context=sensor_ti.get_template_context())

        assert expected_response == op_result

    def test_unknown(self):
        # Testing that an operational failure results in an Unknown
        # test status and an exception from the operator
        # (returning exception for operator and Unknown for test)
        expected_test_response = None

        sensor = self.__create_invalid_test_sensor(self.rb_status_dag)
        sensor_ti = self.__create_task_instance(sensor)

        test_result = sensor_ti.xcom_pull(key="rb_status_test_task_status")

        with pytest.raises(AttributeError):
            sensor.poke(sensor_ti.get_template_context())
        assert expected_test_response == test_result
