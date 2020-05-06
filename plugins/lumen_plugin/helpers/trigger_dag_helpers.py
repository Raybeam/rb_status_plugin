from airflow.configuration import conf
from airflow.exceptions import DagNotFound, DagRunAlreadyExists
from airflow.models import DagBag, DagModel, DagRun
from airflow.utils import timezone
from airflow.utils.state import State


def _trigger_dag(
    dag_id: str,
    dag_bag: DagBag,
    dag_run: DagRun
):
    """
    Triggers DAG run.
    :param dag_id: DAG ID
    :param dagbag: dagbag
    :return: triggered dag
    """
    dag = dag_bag.get_dag(dag_id)  # prefetch dag if it is stored serialized

    if dag_id not in dag_bag.dags:
        raise DagNotFound(f"Dag id {dag_id} not found")

    execution_date = timezone.utcnow()

    run_id = f"lumen_manual__{execution_date.isoformat()}"
    dag_run_id = dag_run.find(dag_id=dag_id, run_id=run_id)
    if dag_run_id:
        raise DagRunAlreadyExists(
            f"Run id {run_id} already exists for dag id {dag_id}"
        )

    dag.create_dagrun(
        run_id=run_id,
        execution_date=execution_date,
        state=State.RUNNING,
        external_trigger=True,
    )

def trigger_dag(dag_id: str):
    """Triggers execution of DAG specified by dag_id
    :param dag_id: DAG ID
    :return: dag run triggered
    """
    dag_model = DagModel.get_current(dag_id)
    if dag_model is None:
        raise DagNotFound("Dag id {} not found in DagModel".format(dag_id))

    dagbag = DagBag(
        dag_folder=dag_model.fileloc,
        store_serialized_dags=conf.getboolean('core', 'store_serialized_dags')
    )
    dag_run = DagRun()
    _trigger_dag(
        dag_id=dag_id,
        dag_bag=dagbag,
        dag_run=dag_run
    )
