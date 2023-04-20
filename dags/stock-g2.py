import pendulum
import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.timezone import datetime

tz = pendulum.timezone("America/New_York")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['inhwan.jung@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='stock-g2-v0.1',
    schedule="30 9 * * *",
    start_date=datetime(2023, 3, 18, tzinfo=tz),
    default_args=default_args,
    catchup=False
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
    task_id=f"stock-trader-g1",
    bash_command=f'docker run --mount type=bind,source=/home/ian/work/airflow/dags/stock-g2.env,target=/app/.env,readonly \
        -v /home/ian/work/invest-to-stock/app/reports:/app/reports \
        -v /home/ian/work/invest-to-stock/app/trade.log:/app/trade.log invest-to-stock:0.1',
    dag=dag
)

t3 = BashOperator(
    task_id='print_end_datetime',
    bash_command='date',
    dag=dag
)

start_dag >> t1

t1 >> t2 >> t3

t3 >> end_dag
