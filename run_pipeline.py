import logging

from src.common.logger import configure_logging
from src.common.config import Config

from src.etl.ingest import ingest_data
from src.etl.transform import transform_users
from src.etl.upload import upload_to_s3
from src.warehouse.load_to_snowflake import load_users

logger = logging.getLogger("pipeline")

# Orchestrates the complete ETL pipeline.
def main():
	configure_logging()

	logger.info("Starting ETL pipeline.")

	ingest_data(
		Config.RAW_SOURCE_FILE,
		Config.RAW_INGESTED_FILE,
	)

	transform_users(
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