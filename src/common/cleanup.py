import logging
import os
from src.common.config import Config

logger = logging.getLogger(__name__)

def cleanup_generated_files():
	"""Remove generated files from previous pipeline runs."""
	for file_path in [Config.RAW_INGESTED_FILE, Config.CLEANED_FILE]:
		if os.path.exists(file_path):
			os.remove(file_path)
			logger.info("Removed old generated file: %s", file_path)