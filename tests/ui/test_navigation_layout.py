"""Test Navigation & Layout for MultiBank.io"""

import re

import pytest
from playwright.sync_api import expect

from tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestNavigationLayout(BaseUITest):
    """Test cases for Navigation & Layout"""

    def test_tc_nav_core_001_navigation_menu_display(self, page, config, test_data):
        """TC-NAV-CORE-001: Top navigation menu displays correctly with all expected options"""
        from tests.utils.reporting.decorators import attach_data

        homepage = self.navigate_to_homepage(page, config)
        nav_data = test_data["navigation"]

        expect(homepage.navigation.nav_container).to_be_visible()

        nav_items = homepage.navigation.get_all_nav_items()
        expected_items = nav_data["expected_items"]
        attach_data(
            f"Expected: {expected_items}\nFound: {nav_items}",
            name="Navigation Items",
        )
        for item in expected_items:
            assert item in nav_items, f"Navigation item '{item}' not found. Found items: {nav_items}"

        expect(homepage.navigation.logo_link).to_be_visible()

    def test_tc_nav_core_002_navigation_functionality(self, page, config, test_data):
        """TC-NAV-CORE-002: Navigation items are functional and link to appropriate destinations"""
        homepage = self.navigate_to_homepage(page, config)
        base_url = self.get_base_url(config)
        nav_data = test_data["navigation"]
        url_patterns = nav_data["url_patterns"]

        navigation_timeout = self.get_timeout(config, "navigation_timeout", 30000)
        homepage.navigation.click_markets()
        page.wait_for_url(re.compile(url_patterns["markets"], re.IGNORECASE), timeout=navigation_timeout)

        homepage.goto(base_url)
        homepage.navigation.click_login()
        # Wait for login page to load - check for login form or URL change
        page.wait_for_url(re.compile(".*login.*", re.IGNORECASE), timeout=navigation_timeout)

        homepage.goto(base_url)
        homepage.navigation.click_signup()
        # Wait for signup page to load - check for signup form or URL change
        page.wait_for_url(re.compile(".*register.*", re.IGNORECASE), timeout=navigation_timeout)

        homepage.goto(base_url)
        homepage.navigation.click_logo()
        page.wait_for_url(re.compile(url_patterns["multibank"], re.IGNORECASE), timeout=navigation_timeout)

    def test_tc_nav_core_003_navigation_responsiveness(self, page, config, test_data):
        """TC-NAV-CORE-003: Navigation menu responsiveness"""
        nav_data = test_data["navigation"]
        viewports = nav_data["viewports"]

        for viewport_name, viewport_size in viewports.items():
            page.set_viewport_size(viewport_size)
            homepage = self.navigate_to_homepage(page, config)
            expect(homepage.navigation.nav_container).to_be_visible()
