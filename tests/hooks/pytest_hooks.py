"""Pytest configuration hooks"""

import os
import time

import pytest

from tests.utils.logging.logger import get_logger, set_correlation_id, setup_logging

logger = get_logger(__name__)

# Initialize logging when pytest loads
log_level = os.environ.get("LOG_LEVEL", "INFO")
log_file = os.environ.get("LOG_FILE")
structured = os.environ.get("LOG_STRUCTURED", "false").lower() == "true"
setup_logging(log_level=log_level, log_file=log_file, structured=structured)


@pytest.hookimpl
def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command-line options for pytest"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests on (dev, stage, prod)",
    )
    parser.addoption(
        "--log-structured",
        action="store_true",
        default=False,
        help="Use JSON structured logging format",
    )


@pytest.hookimpl
def pytest_runtest_setup(item: pytest.Item) -> None:
    """Set correlation ID for each test"""
    # Generate correlation ID for this test
    corr_id = set_correlation_id()
    test_name = f"{item.nodeid}"
    setattr(item, "_test_start_time", time.time())
    logger.info(f"Starting test: {test_name}", extra={"test_name": test_name, "correlation_id": corr_id})


@pytest.hookimpl
def pytest_runtest_teardown(item: pytest.Item) -> None:
    """Log test completion with performance metrics"""
    test_name = f"{item.nodeid}"
    start_time: float | None = getattr(item, "_test_start_time", None)
    if start_time:
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"Completed test: {test_name}",
            extra={"test_name": test_name, "duration_ms": duration_ms},
        )
