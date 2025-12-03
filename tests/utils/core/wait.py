"""Wait utilities for explicit waiting"""

from typing import Literal

from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    expect,
)

from tests.utils.core.exceptions import ElementNotFoundError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)

# Type alias for element state
ElementState = Literal["attached", "detached", "hidden", "visible"]


def wait_for_dropdown(
    page: Page,
    dropdown_locator: Locator,
    timeout: int = 5000,
    check_interval: int = 100,
) -> Locator:
    """
    Wait for dropdown menu to appear using explicit wait conditions

    Args:
        page: Playwright page object
        dropdown_locator: Locator for the dropdown menu
        timeout: Maximum time to wait in milliseconds
        check_interval: Interval between checks in milliseconds

    Returns:
        Locator for the visible dropdown

    Raises:
        ElementNotFoundError: If dropdown doesn't appear within timeout
    """
    try:
        # Use expect for explicit waiting instead of fixed timeout
        expect(dropdown_locator).to_be_visible(timeout=timeout)
        logger.debug("Dropdown menu appeared successfully")
        return dropdown_locator
    except PlaywrightTimeoutError as e:
        error_msg = f"Dropdown menu did not appear within {timeout}ms"
        logger.error(error_msg)
        raise ElementNotFoundError(error_msg) from e


def wait_for_element_state(
    locator: Locator,
    state: ElementState = "visible",
    timeout: int = 5000,
) -> None:
    """
    Wait for element to reach a specific state using explicit wait

    Args:
        locator: Playwright locator
        state: Desired state (visible, hidden, attached, detached)
        timeout: Maximum time to wait in milliseconds

    Raises:
        ElementNotFoundError: If element doesn't reach state within timeout
    """
    try:
        locator.wait_for(state=state, timeout=timeout)
        logger.debug(f"Element reached state '{state}' successfully")
    except PlaywrightTimeoutError as e:
        error_msg = f"Element did not reach state '{state}' within {timeout}ms"
        logger.error(error_msg)
        raise ElementNotFoundError(error_msg) from e


def wait_for_network_idle(
    page: Page,
    timeout: int = 30000,
    idle_time: int = 500,
) -> None:
    """
    Wait for network to be idle using explicit wait

    Args:
        page: Playwright page object
        timeout: Maximum time to wait in milliseconds
        idle_time: Time network must be idle in milliseconds

    Note:
        This is more reliable than wait_for_load_state("networkidle")
        for modern SPAs that have continuous network activity
    """
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
        logger.debug("Network is idle")
    except PlaywrightTimeoutError:
        # For SPAs, networkidle may never occur, so we use a shorter timeout
        logger.debug("Network idle timeout, continuing with DOM ready state")
        page.wait_for_load_state("domcontentloaded", timeout=5000)
