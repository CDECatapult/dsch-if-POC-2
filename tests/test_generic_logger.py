"""The test function for generic_logger.py.

`test_main_logging_behavior_with_caplog` validates logging behaviour
in a Python test script.

"""

import logging

import pytest

from aidi.generic_logger import GenericLogger


@pytest.fixture
def temp_log_file(tmp_path):
    """Fixture for creating a temporary log file."""
    log_file = tmp_path / "test_log.log"
    return log_file


def test_main_logging_behavior_with_caplog(caplog, temp_log_file):
    """Test logging behavior using caplog."""
    print(str(temp_log_file))
    # Initialize the logger
    generic_logger = GenericLogger(
        level="INFO", log_file_name=str(temp_log_file)
    )

    logger = generic_logger.logger

    with caplog.at_level(logging.INFO):
        # Log messages
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")

    # Validate log messages captured by caplog
    log_messages = caplog.text
    assert (
        "This is a debug message." not in log_messages
    ), "Debug message should not be logged at INFO level."
    assert (
        "This is an info message." in log_messages
    ), "Info message not found in captured logs."
    assert (
        "This is a warning message." in log_messages
    ), "Warning message not found in captured logs."
    assert (
        "This is an error message." in log_messages
    ), "Error message not found in captured logs."
    assert (
        "This is a critical message." in log_messages
    ), "Critical message not found in captured logs."
