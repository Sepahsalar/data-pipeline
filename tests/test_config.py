from pathlib import Path
from src.common.config import Config


def test_default_raw_source_file():
    assert Config.RAW_SOURCE_FILE.endswith(".csv")


def test_default_cleaned_file():
    assert Config.CLEANED_FILE.endswith(".csv")


def test_snowflake_private_key_path():
    assert isinstance(Config.SNOWFLAKE_PRIVATE_KEY, str)
    assert Path(Config.SNOWFLAKE_PRIVATE_KEY).suffix == ".p8"


def test_optional_environment_variables_are_strings_or_none():
    assert Config.SNOWFLAKE_USER is None or isinstance(Config.SNOWFLAKE_USER, str)
    assert Config.S3_BUCKET is None or isinstance(Config.S3_BUCKET, str)