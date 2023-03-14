from distutils.util import execute
from airflow.operators.python import PythonOperator
from airflow import DAG
import datetime as dt
from tasks import file1
from airflow.models import Variable
from airflow.operators.bash import BashOperator


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
    # schedule=dt.timedelta(days=1)
    schedule="30 20 * * *"
)

t1 = BashOperator(
    task_id=f"stock-auto-trader",
    bash_command=f"docker run invest-to-stock:0.1",
    dag=dag
)

t1
