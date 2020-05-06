#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Triggering DAG runs APIs."""
import json
from datetime import datetime
from typing import List, Optional, Union

from airflow.exceptions import DagNotFound, DagRunAlreadyExists
from airflow.models import DagBag, DagModel, DagRun
from airflow.utils import timezone
from airflow.utils.state import State


def _trigger_dag(dag_id: str, dag_bag: DagBag, dag_run: DagRun) -> DagRun:
    """
    Triggers DAG run.
    :param dag_id: DAG ID
    :param dagbag: dagbag
    :return: triggered dag
    """
    dag = dag_bag.get_dag(dag_id)  # prefetch dag if it is stored serialized

    if dag_id not in dag_bag.dags:
        raise DagNotFound("Dag id {} not found".format(dag_id))

    execution_date = timezone.utcnow()

    if not timezone.is_localized(execution_date):
        raise ValueError("The execution_date should be localized")

    if dag.default_args and 'start_date' in dag.default_args:
        min_dag_start_date = dag.default_args["start_date"]
        if min_dag_start_date and execution_date < min_dag_start_date:
            raise ValueError(
                "The execution_date [{0}] should be >= start_date [{1}] from DAG's default_args".format(
                    execution_date.isoformat(),
                    min_dag_start_date.isoformat()))

    run_id = f"manual__{execution_date.isoformat()}"
    dag_run_id = dag_run.find(dag_id=dag_id, run_id=run_id)
    if dag_run_id:
        raise DagRunAlreadyExists("Run id {} already exists for dag id {}".format(
            run_id,
            dag_id
        ))

    run_conf = None

    dags_to_trigger = dag
    trigger = dag.create_dagrun(
        run_id=run_id,
        execution_date=execution_date,
        state=State.RUNNING,
        conf=run_conf,
        external_trigger=True,
    )
    return trigger


def trigger_dag(dag_id: str) -> Optional[DagRun]:
    """Triggers execution of DAG specified by dag_id
    :param dag_id: DAG ID
    :return: dag run triggered
    """
    dag_model = DagModel.get_current(dag_id)
    if dag_model is None:
        raise DagNotFound("Dag id {} not found in DagModel".format(dag_id))

    def read_store_serialized_dags():
        from airflow.configuration import conf
        return conf.getboolean('core', 'store_serialized_dags')
    dagbag = DagBag(
        dag_folder=dag_model.fileloc,
        store_serialized_dags=read_store_serialized_dags()
    )
    dag_run = DagRun()
    triggered_dag = _trigger_dag(dag_id=dag_id, dag_bag=dagbag, dag_run=dag_run)

    return triggered_dag