from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
from sqlalchemy.orm.exc import NoResultFound
from airflow.utils.db import provide_session

class LumenSensor(BaseSensorOperator):
    """
    This operator will check whether a test
    (task_instance) succeeded or failed, and
    will reflect that result as it's state.

    :param test_name: Name of task_instance to be tested
    :type test_name: str
    """

    template_fields = (
        "test_dag_id",
        "test_task_id"
    )

    @apply_defaults
    def __init__(
        self,
        test_dag_id,
        test_task_id,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_dag_id = test_dag_id
        self.test_task_id = test_task_id

    def push_test_status(self, ti, test_status):
        xcom_key = f"{ti.dag_id}.{ti.task_id}"
        ti.xcom_push(key=xcom_key, value=test_status)

    @provide_session
    def poke(self, context, session=None):
        self.log.info(f"Querying for {self.test_dag_id}.{self.test_task_id}'s result...")
        try:
            ti = session.query(TaskInstance).filter(
                TaskInstance.task_id == self.test_task_id,
                TaskInstance.dag_id == self.test_dag_id,
            ).order_by(TaskInstance.execution_date.desc()).first()

            terminal_failure_states = [State.FAILED, State.UPSTREAM_FAILED, State.SHUTDOWN, State.REMOVED]
            terminal_success_states = [State.SUCCESS, State.SKIPPED]

            state = ti.state
            self.log.info(
                f"{self.test_dag_id}.{self.test_task_id} is in state {ti.state}"
            )
            if state in terminal_success_states:
                self.push_test_status(ti=context['ti'], test_status=True)
                return True
            if state in terminal_failure_states:
                self.push_test_status(ti=context['ti'], test_status=False)
                return True

            return False

        except Exception e:
            self.push_test_status(ti=context['ti'], test_status=None)
            raise e
