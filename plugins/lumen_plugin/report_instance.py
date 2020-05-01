from airflow.utils.db import provide_session
from airflow.utils.state import State
from airflow import models
import logging


class ReportInstance:
    """
    An instance of a Lumen report.  This is currently a basic wrapper for a DagRun
    with a few Lumen-specific helpers
    """
    def __init__(self, dag_run):
        self.dag_run = dag_run
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
            self._passed = self.calculatePassed(self.errors())
        return self._passed

    @property
    def updated(self):
        return self.dag_run.execution_date

    def calculatePassed(self, errs):
        if len(errs) == 0:
            return True

        # We now know there's at least one failure so we make sure
        # that there's no unknown statuses before returning failed
        for err in errs:
            if err["error_type"] is None:
                return None
        return False


    def errors(self):
        """
        Gets XCOM test_status from each test task instance and returns
        a list of error dict objects...

        Error type is either failed or unknown. Unknown
        denotes an operational failure which prevented task instance
        evaluation.

        :return: returns a list containing error dicts with [id, name,
            description, error_type]
        :rtype: list
        """
        failed = []
        for ti in self.dag_run.get_task_instances():
            if (ti.operator != 'LumenSensor'):
                continue

            xcom_key = f"{ti.dag_id}.{ti.task_id}"
            test_status = ti.xcom_pull(key=xcom_key)

            if not test_status:
                ti.refresh_from_db()

                failed.append({
                    "id": ti.job_id,
                    "name": ti.task_id,
                    "description": ti.log_url,
                    "error_type": test_status
                })

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

        return cls(dag_run)
