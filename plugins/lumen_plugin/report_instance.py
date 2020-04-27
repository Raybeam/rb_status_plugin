from airflow.utils.db import provide_session
from airflow.utils.state import State
import re
from airflow import models
import logging


class ReportInstance:
    """
    An instance of a Lumen report.  This is currently a basic wrapper for a DagRun
    with a few Lumen-specific helpers
    """
    def __init__(self, dag_run, test_prefix):
        self.dag_run = dag_run
        self.test_prefix = test_prefix
        self._passed = None

    @property
    def id(self):
        return self.dag_run.id

    @property
    def dag_id(self):
        return self.dag_run.dag_id

    @property
    def passed(self):
        if self._passed is None:
            self._passed = (self.errors(task_prefix=self.test_prefix) == 0)
        return self._passed

    @property
    def status(self):
        return "Passed" if self.passed else "Failed"

    @property
    def updated(self):
        return self.dag_run.execution_date

    def errors(self, task_prefix=".*"):
        """
        Gets errors that match task_prefix
        By default it accepts any test name
        """

        failed = []
        for ti in self.dag_run.get_task_instances(state=State.FAILED):
            matched = re.match(task_prefix, ti.task_id) is not None
            if matched:
                ti.refresh_from_db()

                failed.append(
                    {"id": ti.job_id, "name": ti.task_id, "description": ti.log_url}
                )

        return failed

    @classmethod
    @provide_session
    def get_latest(cls, report, include_externally_triggered=True, session=None):
        """
        Gets the last ReportInstance for a Report.

        NOTE: The include_externally_triggered is set to True, which is
        the opposite of the Dag object method of the same name.
        """

        dag_run = models.dag.get_last_dagrun(
            report.dag_id, session, include_externally_triggered
        )

        # Retry until we find a finished DAG or there are no more
        while True:
            if dag_run is None:
                raise LookupError(f"Could not find finished DagRun for {report.dag_id}")
            if dag_run.get_state() in State.finished():
                break
            logging.info(
                f"DagRun {dag_run.id} is {dag_run.get_state()} ... trying again."
            )
            dag_run = dag_run.get_previous_dagrun()

        return cls(dag_run, report.test_prefix)
