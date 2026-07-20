FROM apache/airflow:2.10.5

USER root

COPY requirements/ /tmp/requirements/
WORKDIR /opt/airflow/project

USER airflow

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements/airflow.txt