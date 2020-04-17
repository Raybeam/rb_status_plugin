from airflow import AirflowException
from airflow.utils.db import create_session

from airflow.operators.python_operator import PythonOperator
from plugins.lumen_plugin.operators.lumen_operator import LumenOperator

import json
import unittest


class CreateLumenOperatorsTestDag:
	# create and run temporary dag
	dag_name = "lumen_operator_test"
	default_args = {
	    "owner": "airflow",
	    "depends_on_past": False,
	    "email_on_failure": False,
	    "email_on_retry": False,
	   	"schedule_interval": None,
	    "retries": 1,
	    "start_date": datetime(2019, 1, 1),
	    "retry_delay": timedelta(minutes=5),
	}

	def test_succes_fail(self, state):
		# helper to pass or fail a task instance
		if state:
			return True
		else:
			raise ValueError('Task instance failed successfully!')



	def create_dag(self, task_state):
		# create dag with success and failure instances
	    dag = DAG(dag_name=self.dag_name, default_args=self.default_args)

	    with dag:
	        start = DummyOperator(task_id="start_dag")
	        example_test = PythonOperator(
	        	task_id="test_expected_to_%s" % "succeed" if task_state else "fail",
	        	python_callable=test_succes_fail,
	        	op_kwargs={"state":task_state},
	        )
	        start >> example_test

	    return dag


def run_lumen_operator(task_state):
	# run Lumen operator against temporary dag and show results
    return LumenOperator.execute(
        task_id="test_%s" % task_state,
        test_name="lumen_operator_test.%s" % ("test_expected_to_%s" % "succeed" if task_state else "fail"),
    )


class DeleteLumenOperatorsTestDag:
	# delete temporary dag
	dag_name = "lumen_operator_test"
	query = {'delete from xcom where dag_id = "' + self.dag_name + '"',
	        'delete from task_instance where dag_id = "' + self.dag_name + '"',
	        'delete from sla_miss where dag_id = "' + self.dag_name + '"',
	        'delete from log where dag_id = "' + self.dag_name + '"',
	        'delete from job where dag_id = "' + self.dag_name + '"',
	        'delete from dag_run where dag_id = "' + self.dag_name + '"',
	        'delete from dag where dag_id = "' + self.dag_name + '"' }
	def delete_dag(self):
		curr_session.query(self.query)


class LumenOperatorTest(unittest.TestCase):
    def test_success(self):
    	# test that LumenOperator correctly interprets successful test
    	task_state = True
    	expected_response = True
    	CreateLumenOperatorsTestDag.create_dag(task_state=task_state)
        lumen_operator_response = run_lumen_operator(task_state=task_state)
        DeleteLumenOperatorsTestDag.delete_dag()
        self.assertEqual(expected_response, lumen_operator_response)

    def test_failure(self):
    	# test that LumenOperator correctly interprets failed test
    	task_state = False
    	expected_response = False
    	CreateLumenOperatorsTestDag.create_dag(task_state=task_state)
        lumen_operator_response = run_lumen_operator(task_state=task_state)
        DeleteLumenOperatorsTestDag.delete_dag()
        self.assertEqual(expected_response, lumen_operator_response)