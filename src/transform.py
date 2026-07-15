import csv
import logging

from src.config import Config

logger = logging.getLogger(__name__)


def transform_users(input_file, output_file):
	logger.info("Starting data transformation.")

	try:
		with open(input_file, "r", encoding="utf-8") as infile, \
			open(output_file, "w", newline="", encoding="utf-8") as outfile:

			reader = csv.DictReader(infile)
			fieldnames = reader.fieldnames + ["age_group"]

			writer = csv.DictWriter(outfile, fieldnames=fieldnames)
			writer.writeheader()

			for row in reader:
				age = int(row["age"])

				if age < 30:
					row["age_group"] = "young"
				else:
					row["age_group"] = "adult"

				writer.writerow(row)

		logger.info("Data transformation completed successfully.")

	except Exception as e:
		logger.exception("Data transformation failed: %s", e)
		raise


if __name__ == "__main__":
	from src.logger import configure_logging

	configure_logging()

	transform_users(
		Config.RAW_INGESTED_FILE,
		Config.CLEANED_FILE,
	)