"""Support page object for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.pages.basepage import BasePage
from tests.pages.multibank.mixins import ContentPageMixin, SubPageNavigationMixin
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class SupportPage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    """Support page for MultiBank.io"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading = page.locator('h1, [role="heading"]').first
        self.content_sections = page.locator('section, [class*="content"], [class*="support"]')
        self.faq_sections = page.locator('[class*="faq"], [class*="question"], [class*="help"]')
        self.contact_forms = page.locator('[class*="contact"], [class*="form"], form')
        self.images = page.locator("img")

    def goto_support(self, base_url: str, timeout: int = 30000) -> None:
        """Navigate to Support page"""
        if not base_url:
            raise ValueError("base_url is required")
        self.goto(f"{base_url}/support", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def goto_sub_page(self, base_url: str, sub_page: str, timeout: int = 30000) -> None:  # type: ignore[override]
        """Navigate to a specific Support sub-page

        Args:
            base_url: Base URL of the application
            sub_page: Name of the sub-page to navigate to
            timeout: Maximum time to wait for navigation
        """
        SubPageNavigationMixin.goto_sub_page(self, base_url, sub_page, "support", timeout)

    def get_faq_sections_count(self, timeout: int = 5000) -> int:
        """Get count of FAQ sections

        Args:
            timeout: Maximum time to wait for sections

        Returns:
            Number of FAQ sections found
        """
        try:
            self.faq_sections.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.debug("No FAQ sections found within timeout, returning count anyway")
        return self.faq_sections.count()
