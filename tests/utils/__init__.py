"""Test utilities package

This package contains utilities organized by purpose:
- core: Core framework utilities (exceptions, retry, wait)
- reporting: Test reporting utilities (Allure integration)
- config: Configuration management
- data: Test data handling
- helpers: Test-specific helper functions
- logging: Logging utilities
"""

# Re-export commonly used items for convenience
from tests.utils.core.exceptions import (
    ElementNotFoundError,
    FrameworkError,
)
from tests.utils.core.retry import retry_element_interaction, retry_on_failure
from tests.utils.reporting.decorators import attach_data

__all__ = [
    "ElementNotFoundError",
    "FrameworkError",
    "retry_element_interaction",
    "retry_on_failure",
    "attach_data",
]
