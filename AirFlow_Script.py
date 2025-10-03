from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime

with DAG(
        dag_id="uber_dag1",
        start_date=datetime(2025,9,30),
        schedule_interval="@daily"
) as dag:
        sqoop_task=SSHOperator(
                task_id="extract_raw_data",
                ssh_conn_id="ssh_default",
                command="""
                        sqoop import \
                        --connect jdbc:postgresql://external_postgres_db:5432/external \
                        --username external \
                        --password external \
                        --table "raw_rides" \
                        --target-dir /staging_zone/uber_rides \
                        --m 1
                """,
                cmd_timeout=600
        )

        transformation_task=BashOperator(
                task_id="transformations_process",
                bash_command="spark-submit --master local /root/airflow/dags/spark_jobs/uber_p1_transformations.py"
        )

        sqoop_task>> transformation_task
