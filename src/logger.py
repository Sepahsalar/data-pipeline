import logging
from pathlib import Path


def configure_logging():
	if logging.getLogger().handlers:
		return

	logging.getLogger("botocore").setLevel(logging.WARNING)
	logging.getLogger("boto3").setLevel(logging.WARNING)
	logging.getLogger("snowflake").setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)
	
	log_dir = Path(__file__).resolve().parent.parent / "logs"
	log_dir.mkdir(exist_ok=True)

	log_file = log_dir / "pipeline.log"

	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S",
		handlers=[
			logging.FileHandler(log_file, encoding="utf-8"),
			logging.StreamHandler(),
		],
	)