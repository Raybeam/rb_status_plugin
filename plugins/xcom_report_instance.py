from airflow.utils.db import provide_session
import re
from airflow import models
import logging


class XCOMReportInstance:
    """
    An instance of a Lumen report.  This is currently a basic wrapper for a DagRun
    with a few Lumen-specific helpers
    """
    def __init__(self, xcom):
        self.xcom = xcom

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