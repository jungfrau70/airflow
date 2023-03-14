from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.docker_operator import DockerOperator
# from airflow.operators.python_operator import BranchPythonOperator
# from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'description': 'Use of the DockerOperator',
    'depend_on_past': False,
    'start_date': datetime(2021, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('docker_operator_demo', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    start_dag = EmptyOperator(
        task_id='start_dag'
    )

    end_dag = EmptyOperator(
        task_id='end_dag'
    )

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )

    t2 = DockerOperator(
        task_id='docker_command_sleep',
        image='linuxserver/netbox:latest',
        container_name='task___command_sleep',
        api_version='auto',
        auto_remove=True,
        command="/bin/cat .env",
        env_file=".env",
        # docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    t3 = DockerOperator(
        task_id='docker_command_hello',
        image='linuxserver/netbox:latest',
        container_name='task___command_hello',
        api_version='auto',
        auto_remove=True,
        command="/bin/sleep 40",
        # docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    t4 = BashOperator(
        task_id='print_hello',
        bash_command='echo "hello world"'
    )

    start_dag >> t1

    t1 >> t2 >> t4
    t1 >> t3 >> t4

    t4 >> end_dag
