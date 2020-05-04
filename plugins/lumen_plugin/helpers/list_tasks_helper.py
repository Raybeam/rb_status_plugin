from airflow.utils.db import provide_session
from airflow.models.taskinstance import TaskInstance
from plugins.lumen_plugin.report_repo import VariablesReportRepo
from airflow.utils.state import State

@provide_session
def get_all_test_choices(session=None):
    TI = TaskInstance
    tis = session.query(TI).filter(
        ~TI.dag_id.like(f"{VariablesReportRepo.report_prefix}%"),
        TI.state != State.REMOVED
    ).all()
    test_choices = [{"id": i, "name": ti.task_id} for (i, ti) in enumerate(tis)]
    return test_choices
