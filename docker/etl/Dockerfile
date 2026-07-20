FROM python:3.12-slim

WORKDIR /app


COPY requirements/ /tmp/requirements/


RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements/etl.txt

COPY . /app

CMD ["python", "run_pipeline.py"]