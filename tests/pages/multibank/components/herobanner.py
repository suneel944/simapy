"""Hero banner component for MultiBank.io homepage"""

from playwright.sync_api import Page

from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class HeroBannerComponent:
    """Hero banner component at the top of the homepage"""

    def __init__(self, page: Page):
        self.page = page
        self.banner_section = page.locator("#hero-banner-container")
        self.text_container = page.locator("#hero-banner-1-text-container")

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if hero banner is visible at the top of the page"""
        try:
            self.banner_section.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_heading_text(self, timeout: int = 10000) -> str:
        """Get hero banner heading text

        Args:
            timeout: Maximum time to wait for text container to be visible

        Returns:
            Heading text or empty string if not found
        """
        return self.text_container.inner_text().strip()

    def is_in_top_section(self, timeout: int = 5000) -> bool:
        """Verify banner is in the top section of the page"""
        if not self.is_visible(timeout=timeout):
            return False
        banner_box = self.banner_section.bounding_box()
        if not banner_box:
            return False
        # Banner should be in top 50% of viewport
        viewport_height = self.page.viewport_size["height"] if self.page.viewport_size else 1080
        return banner_box["y"] < viewport_height * 0.5
