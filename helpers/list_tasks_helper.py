from airflow.utils.db import provide_session
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State


@provide_session
def get_all_test_choices(session=None):
    TI = TaskInstance
    tis = session.query(TI).filter(
        ~TI.dag_id.like(r"lumen\_%".format()),
        TI.state != State.REMOVED
    ).with_entities(TI.dag_id, TI.task_id).distinct().all()
    test_choices = [(f"{ti.dag_id}.{ti.task_id}", f"{ti.dag_id}.{ti.task_id}")
                    for (i, ti) in enumerate(tis)]
    test_choices.sort()
    return test_choices
