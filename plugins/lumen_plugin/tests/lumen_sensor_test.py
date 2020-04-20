from plugins.lumen_plugin.sensors.lumen_sensor import LumenSensor
from airflow.utils.db import create_session
from airflow.models.taskinstance import TaskInstance
from datetime import datetime
import unittest
from airflow.utils.state import State

class LumenSensorTest(unittest.TestCase):

    def __add_to_task_instance(self, task, state):
        ti = TaskInstance(
            task=task,
            execution_date=datetime(2020, 4, 20)
        )
        ti.set_state(state)
        with create_session() as curr_session:
            ti = curr_session.add(ti)

    def __create_context(self, task_id):
        with create_session() as curr_session:
            ti = curr_session.query(TaskInstance).filter(
                TaskInstance.task_id == self.task_id
            ).order_by(TaskInstance.execution_date.desc()).first()

    def test_success(self):
        # test that LumenOperator correctly interprets successful test
        task_state = True
        expected_response = True
        sensor = LumenSensor(
            task_id="test_%s" % task_state,
            test_name=f"lumen_operator_test.test_expected_to_{task_state}"
        )
        self.__add_to_task_instance(sensor, State.SUCCESS)
        context = self.__create_context("test_%s" % task_state,).get_template_context()
        result = LumenSensor.execute(context)
        self.assertEqual(expected_response, result)

    def test_failure(self):
        # test that LumenOperator correctly interprets failed test
        task_state = False
        expected_response = False
        sensor = LumenSensor(
            task_id="test_%s" % task_state,
            test_name=f"lumen_operator_test.test_expected_to_{task_state}"
        )
        self.__add_to_task_instance(sensor, State.FAILED)
        context = self.__create_context("test_%s" % task_state).get_template_context()
        result = LumenSensor.execute(context)
        self.assertEqual(expected_response, result)


if __name__ == "__main__":
    unittest.main()
