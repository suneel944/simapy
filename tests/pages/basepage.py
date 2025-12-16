from typing import Literal

from playwright.sync_api import Page

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
