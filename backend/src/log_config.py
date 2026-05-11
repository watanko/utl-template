import logging

import structlog


def configure_logging(log_level: str) -> None:
    """Configure structured logging for the process.

    Args:
        log_level: Standard logging level name.

    Returns:
        None.

    Raises:
        ValueError: If the log level name is unknown.
    """

    level = logging.getLevelName(log_level.upper())
    if not isinstance(level, int):
        raise ValueError(f"Unknown log level: {log_level}")

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
