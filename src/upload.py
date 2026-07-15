from datetime import datetime
import boto3
import logging
from datetime import datetime
from pathlib import Path

from src.config import Config

logger = logging.getLogger(__name__)


def upload_to_s3(file_name, bucket):
    logger.info("Starting S3 upload.")

    try:
        s3 = boto3.client("s3")

        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        file_name_only = Path(file_name).name

        s3_key = f"processed/year={year}/month={month}/{file_name_only}"

        s3.upload_file(
            file_name,
            bucket,
            s3_key,
        )

        logger.info("Uploaded file to s3://%s/%s", bucket, s3_key)

    except Exception as e:
        logger.exception("S3 upload failed: %s", e)
        raise


if __name__ == "__main__":
    from src.logger import configure_logging

    configure_logging()

    upload_to_s3(
        Config.CLEANED_FILE,
        Config.S3_BUCKET,
    )