"""Marketing banners component for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class MarketingBannersComponent:
    """Marketing banners component"""

    def __init__(self, page: Page):
        self.page = page
        self.banners = page.locator('[class*="banner"], [class*="marketing"], footer')

    def get_count(self, timeout: int = 5000) -> int:
        """Get count of marketing banners using Playwright's count API

        Args:
            timeout: Maximum time to wait for banners in milliseconds

        Returns:
            Number of marketing banners found
        """
        try:
            self.banners.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.debug("No marketing banners found within timeout, returning count anyway")
        return self.banners.count()

    def scroll_to_bottom(self, timeout: int = 10000) -> None:
        """Scroll to page bottom using Playwright's scroll API

        Args:
            timeout: Maximum time to wait for banners after scroll in milliseconds
        """
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # Wait for banners to be visible after scroll
        try:
            self.banners.first.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.debug("Banners may not exist after scroll, continuing")

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if at least one banner is visible using Playwright's auto-wait"""
        try:
            self.banners.first.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False
