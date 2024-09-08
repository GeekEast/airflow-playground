from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


def print_hello():
    return "Hello World!"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 9, 6),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

dag = DAG(
    dag_id="hello_world",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=timedelta(days=1),
)


t1 = PythonOperator(
    task_id="print_hello",
    python_callable=print_hello,
    dag=dag,
)

t1
