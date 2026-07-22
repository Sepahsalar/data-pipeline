import logging
from pathlib import Path

from src.common.logger import configure_logging


def test_logs_directory_exists():
	"""
	configure_logging() should create the logs directory if it
	does not already exist.
	"""

	configure_logging()

	log_dir = Path("logs")

	assert log_dir.exists()


def test_logger_levels():
	"""Third-party loggers should be reduced to WARNING level."""

	configure_logging()

	assert logging.getLogger("botocore").getEffectiveLevel() == logging.WARNING
	assert logging.getLogger("boto3").getEffectiveLevel() == logging.WARNING
	assert logging.getLogger("snowflake").getEffectiveLevel() == logging.WARNING
	assert logging.getLogger("urllib3").getEffectiveLevel() == logging.WARNING


def test_root_logger_has_handlers():
	"""Logging should configure at least one handler."""

	configure_logging()

	assert len(logging.getLogger().handlers) > 0


def test_configure_logging_is_idempotent():
    """Calling configure_logging() multiple times should not raise errors or remove handlers."""

    configure_logging()
    initial_handler_count = len(logging.getLogger().handlers)

    configure_logging()

    assert len(logging.getLogger().handlers) == initial_handler_count


def test_can_write_log_message():
	"""Writing a log message should not raise an exception."""

	configure_logging()

	logger = logging.getLogger("test")

	logger.info("Hello logger")