"""Trade page object for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.pages.basepage import BasePage
from tests.pages.multibank.mixins import ContentPageMixin, SubPageNavigationMixin
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class TradePage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    """Trade page for MultiBank.io"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading = page.locator('h1, [role="heading"]').first
        self.content_sections = page.locator('section, [class*="content"], [class*="trade"]')
        self.trading_interface = page.locator('[class*="trading"], [class*="exchange"], [class*="spot"]')
        self.images = page.locator("img")

    def goto_trade(self, base_url: str, timeout: int = 30000) -> None:
        """Navigate to Trade page"""
        if not base_url:
            raise ValueError("base_url is required")
        self.goto(f"{base_url}/trade", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def goto_sub_page(self, base_url: str, sub_page: str, timeout: int = 30000) -> None:  # type: ignore[override]
        """Navigate to a specific Trade sub-page

        Args:
            base_url: Base URL of the application
            sub_page: Name of the sub-page to navigate to
            timeout: Maximum time to wait for navigation
        """
        SubPageNavigationMixin.goto_sub_page(self, base_url, sub_page, "trade", timeout)

    def verify_trading_interface_visible(self, timeout: int = 5000) -> bool:
        """Verify trading interface is visible

        Args:
            timeout: Maximum time to wait for interface

        Returns:
            True if trading interface is visible, False otherwise
        """
        try:
            self.trading_interface.first.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            logger.debug("Trading interface not visible within timeout")
            return False
