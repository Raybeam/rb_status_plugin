from airflow.operators import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models.taskinstance import TaskInstance
from airflow.utils.db import create_session


class LumenOperator(BaseOperator):
    """
    This operator will check whether a test (task_instance) succeeded or failed, and
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

    def execute(self, context):
        self.log.info("Querying postgres for %s's result.." % (self.test_name))
        # Query postgres and save to test_result
        with create_session() as curr_session:
            output = curr_session.query(TaskInstance).filter(
                TaskInstance.task_id == self.test_task_id,
                TaskInstance.dag_id == self.test_dag_id,
            ).order_by(TaskInstance.execution_date.desc()).first()
            self.log.info("\n\n\nQuery output:\n%s\n\n\n" % output)
        return True