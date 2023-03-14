from airflow.operators.python import PythonOperator
from airflow import DAG
import datetime as dt
from tasks import file1

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime.now(),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG('simple', default_args=default_args)

python_task = PythonOperator(
    task_id='python_task',
    python_callable=file1.main,
    dag=dag
)