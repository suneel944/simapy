"""Retry mechanism for flaky operations"""

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from tests.utils.core.exceptions import FrameworkError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (PlaywrightTimeoutError, FrameworkError),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to retry a function on failure with exponential backoff

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Backoff multiplier for delay (default: 2.0)
        exceptions: Tuple of exceptions to catch and retry on

    Returns:
        Decorated function with retry logic
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {str(e)}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {str(e)}")

            # If we get here, all retries failed
            raise last_exception  # type: ignore[misc]

        return wrapper

    return decorator


def retry_element_interaction(
    max_attempts: int = 3,
    delay: float = 0.5,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator specifically for element interaction retries (shorter delays)

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Delay between retries in seconds (default: 0.5)

    Returns:
        Decorated function with retry logic
    """
    return retry_on_failure(
        max_attempts=max_attempts,
        delay=delay,
        backoff=1.5,
        exceptions=(PlaywrightTimeoutError, FrameworkError),
    )
