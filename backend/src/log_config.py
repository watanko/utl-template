"""Structured logging configuration."""

import logging

import structlog


class InvalidLogLevelError(ValueError):
    """Raised when the configured log level name is unknown.

    Attributes:
        log_level: Unknown log level name.

    """

    def __init__(self, log_level: str) -> None:
        """Initialize the error.

        Args:
            log_level: Unknown log level name.

        Returns:
            None.

        """
        self.log_level = log_level
        message = f"Unknown log level: {log_level}"
        super().__init__(message)


def configure_logging(log_level: str) -> None:
    """Configure structured logging for the process.

    Args:
        log_level: Standard logging level name.

    Returns:
        None.

    Raises:
        InvalidLogLevelError: If the log level name is unknown.

    """
    levels = logging.getLevelNamesMapping()
    level_name = log_level.upper()
    if level_name not in levels:
        raise InvalidLogLevelError(log_level)

    level = levels[level_name]

    logging.basicConfig(format="%(message)s", level=level)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
