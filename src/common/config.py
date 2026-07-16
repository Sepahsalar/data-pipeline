import os

from dotenv import load_dotenv

load_dotenv()


class Config:
	# Files
	RAW_SOURCE_FILE = os.getenv("RAW_SOURCE_FILE", "data/users.csv")
	RAW_INGESTED_FILE = os.getenv("RAW_INGESTED_FILE", "data/users_raw.csv")
	CLEANED_FILE = os.getenv("CLEANED_FILE", "data/users_cleaned.csv")

	# AWS
	S3_BUCKET = os.getenv("S3_BUCKET")

	# Snowflake
	SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
	SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
	SNOWFLAKE_PRIVATE_KEY = os.getenv(
		"SNOWFLAKE_PRIVATE_KEY",
		os.path.expanduser("~/.snowflake/rsa_key.p8"),
	)
	SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
	SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
	SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
	SNOWFLAKE_TABLE = os.getenv("SNOWFLAKE_TABLE")