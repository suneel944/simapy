"""Logging configuration and utilities with structured logging, correlation IDs, and performance metrics"""

import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar
from pathlib import Path
from typing import Any

# Context variable for correlation ID (thread-safe for parallel execution)
correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def setup_logging(
    log_level: str = "INFO",
    log_file: str | None = None,
    log_format: str | None = None,
    structured: bool = False,
) -> logging.Logger:
    """
    Setup logging configuration for the test framework

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs only to console
        log_format: Optional custom log format. If None, uses default format
        structured: If True, use JSON structured logging format

    Returns:
        Configured logger instance
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create logs directory if log file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Choose formatter based on structured flag
    if structured:
        formatter: logging.Formatter = StructuredFormatter()
    else:
        if log_format is None:
            log_format = (
                "%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(filename)s:%(lineno)d - %(message)s"
            )
        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if log file specified)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger


class StructuredFormatter(logging.Formatter):
    """JSON structured formatter for logs"""

    def __init__(self, datefmt: str | None = None):
        """Initialize structured formatter"""
        super().__init__(datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add correlation ID if available
        corr_id = correlation_id.get()
        if corr_id:
            log_data["correlation_id"] = corr_id

        # Add performance metrics if available
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "test_name"):
            log_data["test_name"] = record.test_name

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    # Add correlation ID filter
    logger.addFilter(CorrelationIDFilter())
    return logger


class CorrelationIDFilter(logging.Filter):
    """Filter to add correlation ID to log records"""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation ID to log record"""
        corr_id = correlation_id.get()
        if corr_id:
            setattr(record, "correlation_id", corr_id)
        else:
            setattr(record, "correlation_id", "N/A")
        return True


def set_correlation_id(corr_id: str | None = None) -> str:
    """
    Set correlation ID for current context (thread-safe)

    Args:
        corr_id: Correlation ID to set. If None, generates a new UUID

    Returns:
        The correlation ID that was set
    """
    if corr_id is None:
        corr_id = str(uuid.uuid4())
    correlation_id.set(corr_id)
    return corr_id


def get_correlation_id() -> str | None:
    """Get current correlation ID"""
    return correlation_id.get()


def clear_correlation_id() -> None:
    """Clear correlation ID from current context"""
    correlation_id.set(None)


class PerformanceLogger:
    """Context manager for logging performance metrics"""

    def __init__(self, logger: logging.Logger, operation: str, **extra: Any):
        """
        Initialize performance logger

        Args:
            logger: Logger instance
            operation: Name of the operation being measured
            **extra: Additional context to log
        """
        self.logger = logger
        self.operation = operation
        self.extra = extra
        self.start_time: float | None = None

    def __enter__(self) -> "PerformanceLogger":
        """Start timing"""
        self.start_time = time.time()
        self.logger.debug(f"Starting {self.operation}", extra=self.extra)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """End timing and log duration"""
        if self.start_time is not None:
            duration_ms = (time.time() - self.start_time) * 1000
            extra = {**self.extra, "duration_ms": duration_ms}
            if exc_type is None:
                self.logger.info(
                    f"Completed {self.operation} in {duration_ms:.2f}ms",
                    extra=extra,
                )
            else:
                self.logger.error(
                    f"Failed {self.operation} after {duration_ms:.2f}ms: {exc_val}",
                    extra=extra,
                )


# Initialize logging on module import
# This will be overridden by pytest configuration if needed
_initialized = False

if not _initialized:
    # Try to get log level from environment
    import os

    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log_file = os.environ.get("LOG_FILE")
    setup_logging(log_level=log_level, log_file=log_file)
    _initialized = True
