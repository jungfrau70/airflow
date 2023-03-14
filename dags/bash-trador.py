from distutils.util import execute
from airflow.operators.python import PythonOperator
from airflow import DAG
import datetime as dt
from tasks import file1
from airflow.models import Variable
from airflow.operators.bash import BashOperator

WORKSPACE = '/home/ian/work/invest-to-stock'

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

dag = DAG(
    'invest-to-stock',
    start_date=dt.datetime(2017, 1, 1),
    catchup=False,
    schedule=dt.timedelta(days=1)
)

t1 = BashOperator(
    task_id='invest-to-stock',
    bash_command=f'{WORKSPACE}/venv/bin/python {WORKSPACE}/app/main.py',
    dag=dag)

t1