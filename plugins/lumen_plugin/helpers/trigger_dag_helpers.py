from airflow.utils.db import provide_session
from airflow.models.dag import DAG, DAGModel


@provide_session
def trigger_dag_id(dag_id, session=None):
    dag = session.query(DAGModel).filter(
        DAGModel.dag_id == dag_id
    ).first()
    dag.run()
