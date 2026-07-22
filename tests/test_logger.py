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


def test_file_handler_is_configured_when_present():
	"""If logging is configured by this application, a FileHandler should point to pipeline.log."""

	configure_logging()

	file_handlers = [
		handler
		for handler in logging.getLogger().handlers
		if isinstance(handler, logging.FileHandler)
	]

	if file_handlers:
		assert any(handler.baseFilename.endswith("pipeline.log") for handler in file_handlers)


def test_can_write_log_message():
	"""Writing a log message should not raise an exception."""

	configure_logging()

	logger = logging.getLogger("test")

	logger.info("Hello logger")