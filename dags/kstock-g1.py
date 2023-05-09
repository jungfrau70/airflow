import pendulum
import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# tz = pendulum.timezone("America/New_York")
tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'email': ['inhwan.jung@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),

}


dag = DAG(
    dag_id='kstock-g1-v0.34',
    schedule="50 8 * * *",
    start_date=dt.datetime(2023, 3, 1, tzinfo=tz),
    default_args=default_args,
    catchup=False,
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
    task_id=f"go-trader-g1",
    bash_command=f'docker run --mount type=bind,source=/home/ian/work/airflow/dags/kstock-g1.env,target=/app/.env,readonly \
        -v /home/ian/work/stock/app/reports:/app/reports \
        -v /home/ian/work/stock/app/trade.log:/app/trade.log invest-to-stock:0.34',
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
