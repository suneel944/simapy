"""Base test class for UI tests"""

from playwright.sync_api import Page

from tests.pages.multibank.homepage import HomePage
from tests.utils.helpers.test_helpers import TestHelper


class BaseUITest:
    """Base test class providing common setup and utilities for UI tests

    Test classes should inherit from this class and use pytest fixtures
    (page, config, test_data) in their test methods.
    """

    @staticmethod
    def get_base_url(config: dict) -> str:
        """Get base URL from config"""
        return TestHelper.get_base_url(config)

    @staticmethod
    def get_timeout(config: dict, timeout_key: str, default: int = 30000) -> int:
        """Get timeout value from config

        Args:
            config: Configuration dictionary
            timeout_key: Timeout key to look up (e.g., 'load_state_timeout', 'element_timeout')
            default: Default timeout value if not found in config

        Returns:
            Timeout value in milliseconds
        """
        return TestHelper.get_timeout(config, timeout_key, default)

    @staticmethod
    def navigate_to_homepage(page: Page, config: dict) -> HomePage:
        """Navigate to homepage and return HomePage instance

        Args:
            page: Playwright page instance
            config: Configuration dictionary

        Returns:
            HomePage instance
        """
        return TestHelper.navigate_to_homepage(page, config)
