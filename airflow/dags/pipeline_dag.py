from datetime import timedelta
import os
import sys

import pendulum
from airflow.decorators import dag, task

from src.common.cleanup import cleanup_generated_files
from src.common.config import Config
from src.etl.ingest import ingest_data
from src.etl.transform import transform_file
from src.etl.upload import upload_to_s3
from src.warehouse.load_to_snowflake import load_users

PROJECT_ROOT = os.path.abspath(
	os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

default_args = {
	"owner": "Alireza",
	"retries": 2,
	"retry_delay": timedelta(minutes=5),
}

@task
def cleanup():
	cleanup_generated_files()

@task
def ingest():
	ingest_data(
		Config.RAW_SOURCE_FILE,
		Config.RAW_INGESTED_FILE,
	)


@task
def transform():
	transform_file(
		Config.RAW_INGESTED_FILE,
		Config.CLEANED_FILE,
	)


@task
def upload():
	upload_to_s3(
		Config.CLEANED_FILE,
		Config.S3_BUCKET,
	)


@task
def snowflake():
	load_users(
		Config.CLEANED_FILE,
		Config.SNOWFLAKE_TABLE,
	)


@dag(
	dag_id="data_pipeline",
	description="End-to-end ETL pipeline from CSV to Snowflake",
	default_args=default_args,
	start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
	schedule=None,
	catchup=False,
	tags=["portfolio", "etl"],
)
def data_pipeline():

	cleanup_task = cleanup()
	ingest_task = ingest()
	transform_task = transform()
	upload_task = upload()
	snowflake_task = snowflake()

	cleanup_task >> ingest_task >> transform_task >> upload_task >> snowflake_task


pipeline = data_pipeline()