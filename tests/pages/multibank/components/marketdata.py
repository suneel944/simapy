"""Market data component for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.core.exceptions import ElementNotFoundError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class MarketDataComponent:
    """Market data component"""

    def __init__(self, page: Page):
        self.page = page
        self.top_gainer_button = page.get_by_role("button", name="Top Gainers", exact=True)
        self.top_loser_button = page.get_by_role("button", name="Top Losers", exact=True)

    def is_top_gainer_visible(self, timeout: int = 5000) -> bool:
        """Check if Top Gainer button is visible using Playwright's auto-wait"""
        try:
            self.top_gainer_button.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_top_loser_visible(self, timeout: int = 5000) -> bool:
        """Check if Top Loser button is visible using Playwright's auto-wait"""
        try:
            self.top_loser_button.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def click_top_gainer(self, timeout: int = 10000) -> None:
        """Click Top Gainer button with auto-wait

        Args:
            timeout: Maximum time to wait in milliseconds

        Raises:
            ElementNotFoundError: If button is not found or clickable
        """
        try:
            self.top_gainer_button.wait_for(state="visible", timeout=timeout)
            self.top_gainer_button.click()
            # Verify button is still attached after click
            self.top_gainer_button.wait_for(state="attached", timeout=timeout)
            logger.debug("Top Gainer button clicked successfully")
        except PlaywrightTimeoutError as e:
            error_msg = f"Top Gainer button not found or not clickable within {timeout}ms"
            logger.error(error_msg)
            raise ElementNotFoundError(error_msg) from e

    def click_top_loser(self, timeout: int = 10000) -> None:
        """Click Top Loser button with auto-wait

        Args:
            timeout: Maximum time to wait in milliseconds

        Raises:
            ElementNotFoundError: If button is not found or clickable
        """
        try:
            self.top_loser_button.wait_for(state="visible", timeout=timeout)
            self.top_loser_button.click()
            # Verify button is still attached after click
            self.top_loser_button.wait_for(state="attached", timeout=timeout)
            logger.debug("Top Loser button clicked successfully")
        except PlaywrightTimeoutError as e:
            error_msg = f"Top Loser button not found or not clickable within {timeout}ms"
            logger.error(error_msg)
            raise ElementNotFoundError(error_msg) from e
