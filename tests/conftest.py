"""Pytest configuration and plugin registration"""

import os

from tests.utils.logging.logger import setup_logging

# Initialize logging early
log_level = os.environ.get("LOG_LEVEL", "INFO")
log_file = os.environ.get("LOG_FILE")
structured = os.environ.get("LOG_STRUCTURED", "false").lower() == "true"
setup_logging(log_level=log_level, log_file=log_file, structured=structured)

pytest_plugins = [
    "tests.fixtures.configload",
    "tests.fixtures.playwright",
    "tests.fixtures.multibankpages",
    "tests.fixtures.testdata",
    "tests.hooks.allure_hooks",
    "tests.hooks.pytest_hooks",
]
