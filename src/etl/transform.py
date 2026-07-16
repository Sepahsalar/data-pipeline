import csv
import logging

logger = logging.getLogger(__name__)


def read_users(input_file):
    """Read users from a CSV file."""
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        return list(reader)


def transform_user(user):
    """Transform a single user record."""
    user = user.copy()

    age = int(user["age"])

    if age < 30:
        user["age_group"] = "young"
    else:
        user["age_group"] = "adult"

    return user


def transform_users(users):
    """Transform a list of users."""
    return [transform_user(user) for user in users]


def write_users(users, output_file):
    """Write users to a CSV file."""

    if not users:
        return

    fieldnames = users[0].keys()

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)


def transform_file(input_file, output_file):
    """Transform an input CSV into an output CSV."""
    try:
        logger.info("Starting data transformation.")

        users = read_users(input_file)
        users = transform_users(users)
        write_users(users, output_file)

        logger.info("Data transformation completed successfully.")

    except Exception:
        logger.exception("Data transformation failed.")
        raise


if __name__ == "__main__":
    from src.common.logger import configure_logging
    from src.common.config import Config

    configure_logging()

    transform_file(
        Config.RAW_INGESTED_FILE,
        Config.CLEANED_FILE,
    )