"""Core framework utilities"""

from tests.utils.core.exceptions import (
    ConfigurationError,
    ElementNotFoundError,
    FrameworkError,
    PageLoadError,
    TestDataError,
    TimeoutError,
)
from tests.utils.core.retry import retry_element_interaction, retry_on_failure
from tests.utils.core.wait import (
    ElementState,
    wait_for_dropdown,
    wait_for_element_state,
    wait_for_network_idle,
)

__all__ = [
    # Exceptions
    "FrameworkError",
    "ElementNotFoundError",
    "PageLoadError",
    "ConfigurationError",
    "TestDataError",
    "TimeoutError",
    # Retry
    "retry_on_failure",
    "retry_element_interaction",
    # Wait
    "ElementState",
    "wait_for_dropdown",
    "wait_for_element_state",
    "wait_for_network_idle",
]
