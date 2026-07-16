import logging
import shutil

from src.common.config import Config

logger = logging.getLogger(__name__)


def ingest_data(source_file, destination_file):
	logger.info("Starting data ingestion.")
	
	try:
		shutil.copy(source_file, destination_file)
		logger.info("Data ingestion completed successfully.")
	except Exception as e:
		logger.exception("Data ingestion failed: %s", e)
		raise


if __name__ == "__main__":
	ingest_data(
		Config.RAW_SOURCE_FILE,
		Config.RAW_INGESTED_FILE,
	)