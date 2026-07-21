import logging
import os

from src.common.logger import configure_logging
from src.common.config import Config

from src.etl.ingest import ingest_data
from src.etl.transform import transform_file
from src.etl.upload import upload_to_s3
from src.warehouse.load_to_snowflake import load_users

logger = logging.getLogger("pipeline")


def cleanup_generated_files():
	"""Remove generated files from previous pipeline runs."""
	for file_path in [Config.RAW_INGESTED_FILE, Config.CLEANED_FILE]:
		if os.path.exists(file_path):
			os.remove(file_path)
			logger.info("Removed old generated file: %s", file_path)



# Orchestrates the complete ETL pipeline.
def main():
	configure_logging()

	logger.info("Starting ETL pipeline.")
	cleanup_generated_files()

	ingest_data(
		Config.RAW_SOURCE_FILE,
		Config.RAW_INGESTED_FILE,
	)

	transform_file(
		Config.RAW_INGESTED_FILE,
		Config.CLEANED_FILE,
	)

	upload_to_s3(
		Config.CLEANED_FILE,
		Config.S3_BUCKET,
	)

	load_users(
	Config.CLEANED_FILE,
	Config.SNOWFLAKE_TABLE,
	)

	logger.info("ETL pipeline completed successfully.")


if __name__ == "__main__":
	main()