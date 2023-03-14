from distutils.util import execute
from airflow.operators.python import PythonOperator
from airflow import DAG
import datetime as dt
from tasks import file1
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

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

start_dag = EmptyOperator(
    task_id='start_dag',
    dag=dag
)

end_dag = EmptyOperator(
    task_id='end_dag',
    dag=dag
)


t1 = BashOperator(
    task_id='print_start_datetime',
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id=f"auto-stock-trader",
    bash_command=f"docker run invest-to-stock:0.1",
    dag=dag
)

t3 = BashOperator(
    task_id=f"auto-bitcoin-trader",
    bash_command=f"docker run invest-to-bitcoin:0.5",
    dag=dag
)

t4 = BashOperator(
    task_id='print_end_datetime',
    bash_command='date',
    dag=dag
)

start_dag >> t1

t1 >> t2 >> t4
t1 >> t3 >> t4

t4 >> end_dag
