"""Features page object for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.pages.basepage import BasePage
from tests.pages.multibank.mixins import ContentPageMixin, SubPageNavigationMixin
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class FeaturesPage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    """Features page for MultiBank.io"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading = page.locator('h1, [role="heading"]').first
        self.content_sections = page.locator('section, [class*="content"], [class*="feature"]')
        self.images = page.locator("img")
        self.feature_cards = page.locator('[class*="feature"], [class*="card"]')

    def goto_features(self, base_url: str, timeout: int = 30000) -> None:
        """Navigate to Features page"""
        if not base_url:
            raise ValueError("base_url is required")
        self.goto(f"{base_url}/features", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def goto_sub_page(self, base_url: str, sub_page: str, timeout: int = 30000) -> None:  # type: ignore[override]
        """Navigate to a specific Features sub-page

        Args:
            base_url: Base URL of the application
            sub_page: Name of the sub-page to navigate to
            timeout: Maximum time to wait for navigation
        """
        SubPageNavigationMixin.goto_sub_page(self, base_url, sub_page, "features", timeout)

    def get_feature_cards_count(self, timeout: int = 5000) -> int:
        """Get count of feature cards

        Args:
            timeout: Maximum time to wait for cards

        Returns:
            Number of feature cards found
        """
        try:
            self.feature_cards.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.debug("No feature cards found within timeout, returning count anyway")
        return self.feature_cards.count()
