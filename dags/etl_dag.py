from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import datetime as dt
from scripts.etl import extract, load

# default arguments
default_args = {
    'owner' : 'Cindy',
    'start_date' : dt.datetime(2024, 1, 25),
    'retries' : 2,
    'retry_delay' : dt.timedelta(minutes=2)
}

# define DAG
dag = DAG(
    'etl_dag',
    default_args = default_args,
    description = 'Load and transform data in local with Airflow',
    catchup = False,
    schedule_interval = '@hourly' # set schedule interval
)

# start task
start_task = DummyOperator(
    task_id='start_task', 
    dag=dag)

# end task
end_task = DummyOperator(
    task_id='end_task', 
    dag=dag)

# extract task
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract, # fungsi python yg akan dipakai
    op_kwargs={
        'file_path' : 'data',
        'destination_path' : 'data/raw'
    },
    dag=dag
)

# load task
load_task = PythonOperator(
    task_id='load_task',
    python_callable=load, # fungsi python yg akan dipakai
    op_kwargs={
        'file_path' : 'data/raw/raw.csv',
        'destination_path' : 'data/output'
    },
    dag=dag
)

# define task dependencies
start_task >> extract_task >> load_task >> end_task


# karena di airflow tidak bisa passing dataframe antar task, kita akan modify script etl.py
# modification: extract_task jalan, maka akan muncul data raw di folder data/raw/raw.csv
# modification2: transform_task akan di hilangkan.
# modification3: load_task akan membaca data dari data/raw/raw.csv kemudian melakukan fungsi load(),
# dan menyimpan hasilnya di data/output/output.csv