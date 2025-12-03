"""About Us page object for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.pages.basepage import BasePage
from tests.pages.multibank.mixins import ContentPageMixin, SubPageNavigationMixin


class AboutUsPage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    """About Us / Why MultiLink page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading = page.locator('h1, [role="heading"]').first
        self.content_sections = page.locator('section, [class*="content"], [class*="about"]')
        self.images = page.locator("img")
        self.lists = page.locator('ul, ol, [role="list"]')
        self.cta_buttons = page.locator('button, a[class*="button"], [role="button"]')

    def goto_about_us(self, base_url: str, timeout: int = 30000) -> None:
        """Navigate to About Us page with Playwright's built-in waiting"""
        if not base_url:
            raise ValueError("base_url is required")
        self.goto(f"{base_url}/about-us", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def goto_why_multilink(self, base_url: str, timeout: int = 30000) -> None:
        """Navigate to Why MultiLink page with Playwright's built-in waiting"""
        if not base_url:
            raise ValueError("base_url is required")
        self.goto(f"{base_url}/about-us/why-multilink", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def goto_sub_page(self, base_url: str, sub_page: str, timeout: int = 30000) -> None:  # type: ignore[override]
        """Navigate to a specific About Us sub-page

        Args:
            base_url: Base URL of the application
            sub_page: Name of the sub-page to navigate to
            timeout: Maximum time to wait for navigation
        """
        SubPageNavigationMixin.goto_sub_page(self, base_url, sub_page, "about-us", timeout)

    def get_images_count(self, timeout: int = 5000) -> int:
        """Get count of images using Playwright's count API"""
        try:
            self.images.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            pass
        return self.images.count()

    def get_all_headings(self, timeout: int = 5000) -> list[str]:
        """Get all headings on the page using Playwright's locator API"""
        headings: list[str] = []
        heading_locator = self.page.locator('h1, h2, h3, h4, h5, h6, [role="heading"]')
        try:
            heading_locator.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            return headings

        heading_elements = heading_locator.all()
        for heading in heading_elements:
            try:
                text = heading.inner_text()
                if text:
                    headings.append(text.strip())
            except Exception:
                continue
        return headings
