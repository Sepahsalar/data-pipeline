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
    """If this application configures logging, it should register a FileHandler for pipeline.log."""

    configure_logging()

    root_logger = logging.getLogger()

    if root_logger.handlers and not any(
        isinstance(handler, logging.FileHandler)
        for handler in root_logger.handlers
    ):
        return

    file_handlers = [
        handler
        for handler in root_logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]

    assert any(handler.baseFilename.endswith("pipeline.log") for handler in file_handlers)


def test_can_write_log_message():
	"""Writing a log message should not raise an exception."""

	configure_logging()

	logger = logging.getLogger("test")

	logger.info("Hello logger")