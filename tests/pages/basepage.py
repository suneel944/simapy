from typing import Literal

from playwright.sync_api import (
    Locator,
    Page,
)

from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Base page object class with common navigation and waiting methods"""

    def __init__(self, page: Page) -> None:
        """Initialize base page with Playwright page object

        Args:
            page: Playwright page object
        """
        self.page = page

    def goto(
        self,
        url: str,
        wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] = "load",
        timeout: int = 30000,
    ) -> None:
        """Navigate to URL with Playwright's built-in waiting

        Args:
            url: URL to navigate to
            wait_until: Load state to wait for (load, domcontentloaded, networkidle)
            timeout: Maximum time to wait in milliseconds

        Raises:
            ValueError: If URL is invalid
        """
        if not url.startswith("http"):
            error_msg = f"Invalid URL: {url}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug(f"Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
        # Wait for DOM to be ready, but don't wait for networkidle as it may timeout
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

    def wait_for_navigation(self, timeout: int = 30000) -> None:
        """Wait for navigation to complete

        Args:
            timeout: Maximum time to wait in milliseconds
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator | None:
        """Wait for element using Playwright's auto-wait

        Args:
            selector: CSS selector or other locator string
            timeout: Maximum time to wait in milliseconds

        Returns:
            Locator if found, None otherwise
        """
        element_handle = self.page.wait_for_selector(selector, timeout=timeout)
        if element_handle is None:
            return None
        # Convert ElementHandle to Locator by using query_selector result
        # wait_for_selector returns ElementHandle, but we return Locator for consistency
        return self.page.locator(selector)

    def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> None:
        """Wait for URL to match pattern

        Args:
            url_pattern: URL pattern to match (string or regex)
            timeout: Maximum time to wait in milliseconds
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)
