import logging
import csv
import snowflake.connector
from cryptography.hazmat.primitives import serialization

from src.common.config import Config

logger = logging.getLogger(__name__)


def load_private_key():
	key_path = Config.SNOWFLAKE_PRIVATE_KEY

	with open(key_path, "rb") as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password=None
		)

	return private_key.private_bytes(
		encoding=serialization.Encoding.DER,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption()
	)


def connect_to_snowflake():
	private_key = load_private_key()
	conn = snowflake.connector.connect(
		user=Config.SNOWFLAKE_USER,
		account=Config.SNOWFLAKE_ACCOUNT,
		private_key=private_key,
		warehouse=Config.SNOWFLAKE_WAREHOUSE,
		database=Config.SNOWFLAKE_DATABASE,
		schema=Config.SNOWFLAKE_SCHEMA
	)

	return conn


def read_csv(file_path):

	with open(file_path, "r", encoding="utf-8") as file:

		reader = csv.DictReader(file)

		return list(reader)


def load_users(file_path, table):
	conn = None
	cursor = None
	try:
		logger.info("Starting Snowflake load.")
		conn = connect_to_snowflake()
		cursor = conn.cursor()

		users = read_csv(file_path)

		logger.info("Loading records into Snowflake.")

		for user in users:
			cursor.execute(
				f"""
				INSERT INTO {table}
				(ID, NAME, AGE, AGE_GROUP)
				VALUES (%s, %s, %s, %s)
				""",
				(
					int(user["id"]),
					user["name"],
					int(user["age"]),
					user["age_group"]
				)
			)

		conn.commit()
		logger.info("Loaded %d users into Snowflake.", len(users))
	except Exception as e:
		logger.exception("Snowflake load failed: %s", e)
		raise
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()


if __name__ == "__main__":
	from src.common.logger import configure_logging

	configure_logging()
	load_users(
		Config.CLEANED_FILE,
		Config.SNOWFLAKE_TABLE,
	)