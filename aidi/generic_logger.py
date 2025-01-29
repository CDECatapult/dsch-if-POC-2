"""This module provides functionality for configuring and managing logging.
Classes:
    - GenericLogger: A class for setting up and managing a customizable logger.
Features:
    - Allows specification of logger name, logging level, and log file name.
    - Configures logging with a default format that includes timestamps, logger
    names, and log levels.
    - Provides an easy-to-use interface for logging messages at different
    severity levels.

Example:
    To use the logger in another module or script:

    ```python
    from generic_config import GenericLogger

    # Initialize the logger
    generic_logger = GenericLogger(name="my_logger", level="DEBUG",
    log_file_name="my_log.log")
    logger = generic_logger.logger

    # Log messages
    logger.info("This is an informational message.")
    logger.error("This is an error message.")
    ```

Note:
    The `__main__` block demonstrates usage for testing purposes.
"""  # noqa: D205

import logging


class GenericLogger:
    """A class for configuring and managing logging functionality."""

    def __init__(
        self,
        name: str = "__main__",
        level: str = "INFO",
        log_file_name: str = "applog.log",
    ):
        """Initializes a logger with the specified configuration.

        Args:
            name (str): The name of the logger. Defaults to '__main__'.
            level (str): The logging level (e.g., 'DEBUG', 'INFO', 'WARNING',
            'ERROR', 'CRITICAL'). Defaults to 'INFO'.
            log_file_name (str): The name of the log file.
            Defaults to 'applog.log'.
        """
        self.logger = logging.getLogger(name)
        self.configure_logger(level, log_file_name)

    def configure_logger(self, level: str, log_file_name: str):
        """Configures the logger with the specified level and file handler.

        Args:
            level (str): The logging level.
            log_file_name (str): The name of the log file.
        """
        # Clear existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Configure logging
        log_level = getattr(logging, level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file_name)],
        )
        self.logger.info(
            f"Logger with level '{level}' and log file '{log_file_name}'."
        )


# Example Usage for test purposes
if __name__ == "__main__":
    generic_logger = GenericLogger()
    logger = generic_logger.logger

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
