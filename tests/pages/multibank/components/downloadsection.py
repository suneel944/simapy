"""Download section component for MultiBank.io"""

import re

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class DownloadSectionComponent:
    """Download section component"""

    def __init__(self, page: Page):
        self.page = page
        self.section_heading = page.get_by_role("heading", name="Trade on the Go", exact=True)
        # Use text matching that handles newlines - find by partial text
        self.app_store_link = page.locator("a").filter(has_text=re.compile(r"app store", re.IGNORECASE)).first
        self.google_play_link = page.locator("a").filter(has_text=re.compile(r"google play", re.IGNORECASE)).first
        self.qr_code = page.locator('img[alt*="qr" i], [class*="qr" i]').first

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if download section is visible using Playwright's auto-wait"""
        try:
            self.section_heading.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def scroll_into_view(self, timeout: int = 5000) -> None:
        """Scroll download section into view using Playwright's scroll API"""
        self.section_heading.wait_for(state="attached", timeout=timeout)
        self.section_heading.scroll_into_view_if_needed()
        # Wait for section to be visible after scroll
        self.section_heading.wait_for(state="visible", timeout=timeout)

    def get_app_store_url(self, timeout: int = 5000) -> str:
        """Get App Store link URL using Playwright's attribute API

        Args:
            timeout: Maximum time to wait for link in milliseconds

        Returns:
            App Store URL or empty string if not found
        """
        try:
            self.app_store_link.wait_for(state="attached", timeout=timeout)
            url = self.app_store_link.get_attribute("href") or ""
            if not url:
                logger.warning("App Store link found but href attribute is empty")
            return url
        except PlaywrightTimeoutError:
            logger.warning(f"App Store link not found within {timeout}ms")
            return ""

    def get_google_play_url(self, timeout: int = 5000) -> str:
        """Get Google Play link URL using Playwright's attribute API

        Args:
            timeout: Maximum time to wait for link in milliseconds

        Returns:
            Google Play URL or empty string if not found
        """
        try:
            self.google_play_link.wait_for(state="attached", timeout=timeout)
            url = self.google_play_link.get_attribute("href") or ""
            if not url:
                logger.warning("Google Play link found but href attribute is empty")
            return url
        except PlaywrightTimeoutError:
            logger.warning(f"Google Play link not found within {timeout}ms")
            return ""

    def get_heading_text(self, timeout: int = 5000) -> str:
        """Get section heading text using Playwright's inner_text API

        Args:
            timeout: Maximum time to wait for heading in milliseconds

        Returns:
            Heading text or empty string if not found
        """
        try:
            self.section_heading.wait_for(state="visible", timeout=timeout)
            text = self.section_heading.inner_text() or ""
            if not text:
                logger.warning("Download section heading found but text is empty")
            return text
        except PlaywrightTimeoutError:
            logger.warning(f"Download section heading not found within {timeout}ms")
            return ""

    def has_qr_code(self, timeout: int = 2000) -> bool:
        """Check if QR code is present using Playwright's count API"""
        try:
            self.qr_code.wait_for(state="attached", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return self.page.locator('img[alt*="qr"], [class*="qr"]').count() > 0

    def verify_heading_contains_keywords(self, keywords: list[str], timeout: int = 5000) -> bool:
        """Verify heading contains expected keywords

        Args:
            keywords: List of keywords to check for
            timeout: Maximum time to wait for heading

        Returns:
            True if heading contains at least one keyword
        """
        heading_text = self.get_heading_text(timeout=timeout).lower()
        return any(keyword.lower() in heading_text for keyword in keywords)

    def verify_descriptive_text_visible(self, pattern: str, timeout: int = 5000) -> bool:
        """Verify descriptive text matching pattern is visible in download section

        Args:
            pattern: Regex pattern to match descriptive text
            timeout: Maximum time to wait

        Returns:
            True if descriptive text is visible
        """
        download_section = self.section_heading.locator("..")
        descriptive_text = download_section.filter(has_text=re.compile(pattern, re.IGNORECASE)).first
        try:
            descriptive_text.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False
