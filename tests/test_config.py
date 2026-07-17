from src.common.config import Config


def test_default_raw_source_file():
    assert Config.RAW_SOURCE_FILE.endswith(".csv")


def test_default_cleaned_file():
    assert Config.CLEANED_FILE.endswith(".csv")


def test_snowflake_user_exists():
    assert Config.SNOWFLAKE_USER is not None


def test_s3_bucket_exists():
    assert Config.S3_BUCKET is not None