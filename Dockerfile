FROM apache/airflow:2.8.1

RUN pip install --no-cache-dir --user --upgrade pip

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --user -r /requirements.txt

COPY data /data

COPY dags /opt/airflow/dags