FROM apache/airflow:2.10.5

USER root

COPY requirements/airflow.txt /tmp/requirements.txt
WORKDIR /opt/airflow/project

USER airflow

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt