from airflow.utils.db import provide_session
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State


@provide_session
def get_all_test_choices(session=None):
    TI = TaskInstance
    tis = session.query(TI).filter(
        ~TI.dag_id.like(f"lumen_%"),
        TI.state != State.REMOVED
    ).with_entities(TI.dag_id, TI.task_id).distinct().all()
    test_choices = [(i, f"{ti.dag_id}.{ti.task_id}") for (i, ti) in enumerate(tis)]
    return test_choices
