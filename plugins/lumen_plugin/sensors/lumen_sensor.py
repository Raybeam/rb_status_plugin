from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.models.taskinstance import TaskInstance
from airflow.utils.db import create_session
from airflow.utils.state import State
from sqlalchemy.orm.exc import NoResultFound


class LumenSensor(BaseSensorOperator):
    """
    This operator will check whether a test
    (task_instance) succeeded or failed, and
    will reflect that result as it's state.

    :param test_name: Name of task_instance to be tested
    :type test_name: str
    """

    template_fields = (
        "test_name",
    )

    @apply_defaults
    def __init__(
        self,
        test_name,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_name = test_name
        self.test_dag_id = test_name.split('.')[0]
        self.test_task_id = test_name.split('.')[1]

    def poke(self, context):
        self.log.info("Querying postgres for %s's result.." % (self.test_name))
        # Query postgres and save to test_result
        with create_session() as curr_session:
            ti = curr_session.query(TaskInstance).filter(
                TaskInstance.task_id == self.test_task_id,
                TaskInstance.dag_id == self.test_dag_id,
            ).order_by(TaskInstance.execution_date.desc()).first()

            if not ti:
                self.log.info(
                    "No task instance was for for this dag_id and task_id"
                )
                raise NoResultFound

            state = ti.state
            terminal_failure_states = [
                State.FAILED, State.UPSTREAM_FAILED,
                State.SHUTDOWN, State.REMOVED
            ]
            terminal_success_states = [State.SUCCESS, State.SKIPPED]

            self.log.info(ti)
            self.log.info(ti.state)

            if state in terminal_failure_states:
                self.log.error('Test was in a terminal failed state')
                raise ValueError()
            elif state in terminal_success_states:
                return True
            else:
                return False
