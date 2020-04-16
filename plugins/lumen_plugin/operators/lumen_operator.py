from airflow.operators import BaseOperator
from airflow.utils.decorators import apply_defaults

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
        conn_id="kenshoo_default",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_name = test_name

    def execute(self, context):
        self.log.info("Querying postgres for %s's result.." % (self.test_name))
        # Query postgres and save to test_result
        with create_session() as curr_session:
            output = curr_session.query(self.test_name).all()
            self.log.info("\n\n\nQuery output:\n%s\n\n\n" % output)
        return True