"""Test helper utilities to reduce code duplication"""

from playwright.sync_api import Page

from tests.pages.multibank.homepage import HomePage
from tests.utils.config.constants import ConfigKeys


class TestHelper:
    """Helper class for common test operations"""

    @staticmethod
    def get_base_url(config: dict) -> str:
        """Get base URL from config"""
        multibank_config = config.get(ConfigKeys.MULTIBANK.value, {})
        base_url = multibank_config.get(ConfigKeys.BASE_URL.value)
        if not base_url or not isinstance(base_url, str):
            raise ValueError(f"base_url not found in config under {ConfigKeys.MULTIBANK.value}")
        # Type narrowing: isinstance check ensures base_url is str
        return str(base_url)

    @staticmethod
    def get_timeout(config: dict, timeout_key: str, default: int = 30000) -> int:
        """Get timeout value from config

        Args:
            config: Configuration dictionary
            timeout_key: Timeout key to look up (e.g., 'load_state_timeout', 'navigation_timeout')
            default: Default timeout value if not found in config

        Returns:
            Timeout value in milliseconds
        """
        playwright_config = config.get(ConfigKeys.PLAYWRIGHT.value, {})
        timeout = playwright_config.get(timeout_key, default)
        return int(timeout)

    @staticmethod
    def navigate_to_homepage(page: Page, config: dict) -> HomePage:
        """Navigate to homepage and return HomePage instance"""
        homepage = HomePage(page)
        base_url = TestHelper.get_base_url(config)
        homepage.goto(base_url)
        return homepage
