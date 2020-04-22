from airflow.utils.db import provide_session
from airflow.utils.state import State

import airflow.models.dag as dag


class ReportInstance:
    """
    An instance of a Lumen report.  This is currently a basic wrapper for a DagRun
    with a few Lumen-specific helpers
    """

    def __init__(self, report, dag_run):
        self.report = report
        self.dag_run = dag_run

    @property
    def id(self):
        return self.dag_run.id

    @property
    def passed(self):
        return self.dag_run.get_state() == State.SUCCESS

    @property
    def updated(self):
        return self.dag_run.execution_date

    @property
    def title(self):
        return f"Lumen report : {self.report.name}"

    def failed_task_instances(self):
        if self.passed:
            return []

        return self.dag_run.get_task_instances(state=State.FAILED)

    @classmethod
    @provide_session
    def get_latest(cls, report, include_externally_triggered=True, session=None):
        """
        Gets the last ReportInstance for a Report.

        NOTE: The include_externally_triggered is set to True, which is
        the opposite of the Dag object method of the same name.
        """

        retries = 3
        dag_run = dag.get_last_dagrun(
            report.dag_id, session, include_externally_triggered
        )

        # Retry 3 times if the DAG is still running
        while True:
            if dag_run is None:
                raise LookupError(f"Could not find finished DagRun for {report.dag_id}")
            if retries < 0:
                raise LookupError(f"Could not find finished DagRun for {report.dag_id}")
            if dag_run.get_state() in State.finished():
                break
            dag_run = dag_run.get_previous_dagrun
            retries -= 1

        return cls(report, dag_run)
