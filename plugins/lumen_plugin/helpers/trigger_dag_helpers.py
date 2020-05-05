from airflow.utils.db import provide_session
from airflow.models.dag import DagModel


@provide_session
def trigger_dag_id(dag_id, session=None):
    dag = session.query(DagModel).filter(
        DagModel.dag_id == dag_id
    ).first()
    dag.run()
