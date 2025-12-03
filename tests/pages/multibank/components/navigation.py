"""Navigation component for MultiBank.io"""

from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.core.retry import retry_element_interaction, retry_on_failure
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class NavigationComponent:
    """Navigation menu component for pre-login state"""

    def __init__(self, page: Page):
        self.page = page
        self.nav_container = page.locator("header, nav, [role='banner']").first
        self.header = page.locator("header").first
        self.logo_link = self.header.locator('a[href="/"]').first
        self.markets_nav_link = self.header.get_by_role("link", name="Markets", exact=True)
        self.login_nav_link = self.header.get_by_role("link", name="Log In", exact=True)
        self.signup_nav_link = self.header.get_by_role("link", name="Sign Up", exact=True)
        # Dropdown toggle items - these are buttons/toggles, not links
        self._about_us_toggle = self.header.locator("#about-header-option-open-button")
        self._features_toggle = self.header.locator("#features-header-option-open-button")
        self._trade_toggle = self.header.locator("#trade-header-option-open-button")
        self._support_toggle = self.header.locator("#support-header-option-open-button")

    def _find_toggle_item(self, text: str, timeout: int = 5000) -> Locator:
        """Find toggle/button navigation item by text using proper locators

        Args:
            text: Text of the toggle item to find
            timeout: Maximum time to wait in milliseconds

        Returns:
            Locator for the toggle item
        """
        return (
            self.header.get_by_role("button", name=text, exact=False)
            .or_(self.header.get_by_role("link", name=text, exact=False))
            .first
        )

    @property
    def about_us_nav(self) -> Locator:
        """Get About Us toggle (button that reveals dropdown)"""
        return self._about_us_toggle

    @property
    def features_nav(self) -> Locator:
        """Get Features toggle (button that reveals dropdown)"""
        return self._features_toggle

    @property
    def trade_nav(self) -> Locator:
        """Get Trade toggle (button that reveals dropdown)"""
        return self._trade_toggle

    @property
    def support_nav(self) -> Locator:
        """Get Support toggle (button that reveals dropdown)"""
        return self._support_toggle

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if navigation menu is visible using Playwright's auto-wait"""
        try:
            self.nav_container.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_all_nav_items(self, timeout: int = 2000) -> list[str]:
        """Get all navigation link texts using Playwright's visibility checks"""
        nav_items = []
        nav_links = [
            (self.markets_nav_link, "Markets"),
            (self.login_nav_link, "Log In"),
            (self.signup_nav_link, "Sign Up"),
        ]

        for link_locator, name in nav_links:
            try:
                link_locator.wait_for(state="visible", timeout=timeout)
                nav_items.append(name)
            except PlaywrightTimeoutError:
                continue

        return nav_items

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def click_markets(self, timeout: int = 10000) -> None:
        """Click Markets link with auto-wait"""
        self.markets_nav_link.wait_for(state="visible", timeout=timeout)
        self.markets_nav_link.click()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def click_login(self, timeout: int = 10000) -> None:
        """Click Log In link with auto-wait"""
        self.login_nav_link.wait_for(state="visible", timeout=timeout)
        self.login_nav_link.click()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def click_signup(self, timeout: int = 10000) -> None:
        """Click Sign Up link with auto-wait"""
        self.signup_nav_link.wait_for(state="visible", timeout=timeout)
        self.signup_nav_link.click()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def click_logo(self, timeout: int = 10000) -> None:
        """Click logo link with auto-wait"""
        self.logo_link.wait_for(state="visible", timeout=timeout)
        self.logo_link.click()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def hover_about_us(self, timeout: int = 5000) -> None:
        """Hover over About Us to open dropdown"""
        self.about_us_nav.wait_for(state="visible", timeout=timeout)
        self.about_us_nav.hover()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def hover_features(self, timeout: int = 5000) -> None:
        """Hover over Features to open dropdown"""
        self.features_nav.wait_for(state="visible", timeout=timeout)
        self.features_nav.hover()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def hover_trade(self, timeout: int = 5000) -> None:
        """Hover over Trade to open dropdown"""
        self.trade_nav.wait_for(state="visible", timeout=timeout)
        self.trade_nav.hover()

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def hover_support(self, timeout: int = 5000) -> None:
        """Hover over Support to open dropdown"""
        self.support_nav.wait_for(state="visible", timeout=timeout)
        self.support_nav.hover()

    @retry_on_failure(max_attempts=3, delay=0.5)
    def get_dropdown_items(self, parent_locator: Locator) -> list[str]:
        """Get all dropdown menu items from a parent locator"""
        parent_locator.hover()
        dropdown_panel = self.page.locator('[id^="headlessui-popover-panel-"]').first
        return [link.inner_text().strip() for link in dropdown_panel.locator("a").all()]

    @retry_element_interaction(max_attempts=3, delay=0.5)
    def click_dropdown_item(self, item_text: str) -> None:
        """Click a specific item in a dropdown menu

        Args:
            item_text: Text of the dropdown item to click
        """
        self.page.get_by_role("link", name=item_text, exact=False).first.click()

    def get_about_us_dropdown_items(self, timeout: int = 3000) -> list[str]:
        """Get About Us dropdown menu items"""
        self.hover_about_us(timeout=timeout)
        return self.get_dropdown_items(self.about_us_nav, timeout=timeout)

    def get_features_dropdown_items(self, timeout: int = 3000) -> list[str]:
        """Get Features dropdown menu items"""
        self.hover_features(timeout=timeout)
        return self.get_dropdown_items(self.features_nav, timeout=timeout)

    def get_trade_dropdown_items(self, timeout: int = 3000) -> list[str]:
        """Get Trade dropdown menu items"""
        self.hover_trade(timeout=timeout)
        return self.get_dropdown_items(self.trade_nav, timeout=timeout)

    def get_support_dropdown_items(self, timeout: int = 3000) -> list[str]:
        """Get Support dropdown menu items"""
        self.hover_support(timeout=timeout)
        return self.get_dropdown_items(self.support_nav, timeout=timeout)

    @retry_on_failure(max_attempts=3, delay=0.5)
    def click_about_us_item(self, item_text: str, timeout: int = 10000) -> None:
        """Click a specific About Us dropdown item"""
        self.hover_about_us(timeout=timeout)
        self.click_dropdown_item(item_text)

    @retry_on_failure(max_attempts=3, delay=0.5)
    def click_features_item(self, item_text: str, timeout: int = 10000) -> None:
        """Click a specific Features dropdown item"""
        self.hover_features(timeout=timeout)
        self.click_dropdown_item(item_text)

    @retry_on_failure(max_attempts=3, delay=0.5)
    def click_trade_item(self, item_text: str, timeout: int = 10000) -> None:
        """Click a specific Trade dropdown item"""
        self.hover_trade(timeout=timeout)
        self.click_dropdown_item(item_text)

    @retry_on_failure(max_attempts=3, delay=0.5)
    def click_support_item(self, item_text: str, timeout: int = 10000) -> None:
        """Click a specific Support dropdown item"""
        self.hover_support(timeout=timeout)
        self.click_dropdown_item(item_text)
