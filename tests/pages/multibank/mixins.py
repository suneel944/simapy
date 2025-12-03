"""Mixins for common page object functionality"""

from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.core.exceptions import ElementNotFoundError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class ContentPageMixin:
    """Mixin providing common content page methods to eliminate code duplication"""

    page: Page
    page_heading: Locator
    content_sections: Locator

    def get_page_heading(self, timeout: int = 5000) -> str:
        """Get page heading text using Playwright's inner_text API

        Args:
            timeout: Maximum time to wait for heading to be visible

        Returns:
            Heading text or empty string if not found

        Raises:
            ElementNotFoundError: If heading cannot be found within timeout
        """
        try:
            self.page_heading.wait_for(state="visible", timeout=timeout)
            heading_text = self.page_heading.inner_text() or ""
            if not heading_text:
                logger.warning("Page heading element found but text is empty")
            return heading_text
        except PlaywrightTimeoutError as e:
            error_msg = f"Page heading not found within {timeout}ms"
            logger.error(error_msg)
            raise ElementNotFoundError(error_msg) from e

    def get_all_text_content(self, timeout: int = 5000) -> str:
        """Get all text content from page using Playwright's text_content API

        Args:
            timeout: Maximum time to wait for body element

        Returns:
            All text content from page body
        """
        body_locator = self.page.locator("body")
        try:
            body_locator.wait_for(state="attached", timeout=timeout)
            return body_locator.inner_text() or ""
        except PlaywrightTimeoutError:
            error_msg = f"Body element not found within {timeout}ms"
            logger.warning(error_msg)
            return ""

    def get_content_sections_count(self, timeout: int = 5000) -> int:
        """Get count of content sections using Playwright's count API

        Args:
            timeout: Maximum time to wait for sections

        Returns:
            Number of content sections found
        """
        try:
            self.content_sections.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.debug("No content sections found within timeout, returning count anyway")
        return self.content_sections.count()

    def verify_no_placeholder_text(self, placeholder_keywords: list[str] | None = None, timeout: int = 5000) -> bool:
        """Verify no placeholder text is displayed using Playwright's text API

        Args:
            placeholder_keywords: List of keywords to check for. If None, uses defaults
            timeout: Maximum time to wait for body element

        Returns:
            True if no placeholder text found, False otherwise
        """
        body_text = self.get_all_text_content(timeout=timeout).lower()
        if placeholder_keywords is None:
            placeholder_keywords = [
                "lorem ipsum",
                "placeholder",
                "sample text",
                "coming soon",
            ]
        return not any(keyword in body_text for keyword in placeholder_keywords)


class SubPageNavigationMixin:
    """Mixin providing common sub-page navigation methods"""

    page: Page

    def goto_sub_page(self, base_url: str, sub_page: str, base_path: str, timeout: int = 30000) -> None:
        """Navigate to a specific sub-page

        Args:
            base_url: Base URL of the application
            sub_page: Name of the sub-page to navigate to
            base_path: Base path for the section (e.g., "about-us", "features")
            timeout: Maximum time to wait for navigation

        Raises:
            ValueError: If base_url is not provided
        """
        if not base_url:
            raise ValueError("base_url is required")

        # Convert sub-page name to URL-friendly format
        url_path = sub_page.lower().replace(" ", "-").replace("&", "and").replace("?", "")

        # Handle special cases if needed
        url_mapping = {
            "why-multibank": "why-multibank",
            "global-presence": "global-presence",
            "management": "management",
            "awards": "awards",
            "sponsorship": "sponsorship",
            "blog": "blog",
            "milestones": "milestones",
        }
        url_path = url_mapping.get(url_path, url_path)

        full_url = f"{base_url}/{base_path}/{url_path}"
        logger.debug(f"Navigating to sub-page: {full_url}")
        # self.goto is provided by BasePage (via MRO)
        self.goto(full_url, timeout=timeout)  # type: ignore[attr-defined]
        self.page.wait_for_load_state("networkidle", timeout=timeout)
