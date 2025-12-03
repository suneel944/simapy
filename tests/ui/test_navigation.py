import pytest

from tests.pages.multibank.aboutuspage import AboutUsPage
from tests.pages.multibank.featurespage import FeaturesPage
from tests.pages.multibank.supportpage import SupportPage
from tests.pages.multibank.tradepage import TradePage
from tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestNavigation(BaseUITest):
    """Test cases for Navigation"""

    def _verify_navigation_to_sub_page(self, page, config, homepage, page_object, navigation_method, sub_page_name):
        """Helper method to verify navigation to a sub-page via dropdown"""
        base_url = self.get_base_url(config)

        homepage.goto(base_url)
        navigation_method(sub_page_name)
        load_state_timeout = self.get_timeout(config, "load_state_timeout", 30000)
        page.wait_for_load_state("load", timeout=load_state_timeout)

        # Wait for content sections to appear and verify count is greater than 0
        element_timeout = self.get_timeout(config, "element_timeout", 10000)
        try:
            page_object.content_sections.first.wait_for(state="attached", timeout=element_timeout)
        except Exception:
            pass  # Continue to check count even if wait times out
        count = page_object.get_content_sections_count()
        assert count > 0, f"Expected at least one content section, but found {count}"

    def test_tc_navigation_002_about_us_navigation(self, page, config, about_us_sub_page):
        """TC-NAVIGATION-002: About Us page navigation via dropdown links"""
        homepage = self.navigate_to_homepage(page, config)
        about_page = AboutUsPage(page)

        self._verify_navigation_to_sub_page(
            page,
            config,
            homepage,
            about_page,
            homepage.navigation.click_about_us_item,
            about_us_sub_page,
        )

    def test_tc_navigation_003_trade_navigation(self, page, config, trade_sub_page):
        """TC-NAVIGATION-003: Trade page navigation via dropdown links"""
        homepage = self.navigate_to_homepage(page, config)
        trade_page = TradePage(page)

        self._verify_navigation_to_sub_page(
            page,
            config,
            homepage,
            trade_page,
            homepage.navigation.click_trade_item,
            trade_sub_page,
        )

    def test_tc_navigation_004_features_navigation(self, page, config, features_sub_page):
        """TC-NAVIGATION-004: Features page navigation via dropdown links"""
        homepage = self.navigate_to_homepage(page, config)
        features_page = FeaturesPage(page)

        self._verify_navigation_to_sub_page(
            page,
            config,
            homepage,
            features_page,
            homepage.navigation.click_features_item,
            features_sub_page,
        )

    def test_tc_navigation_005_support_navigation(self, page, config, test_data, support_sub_page):
        """TC-NAVIGATION-005: Support page navigation via dropdown links"""
        homepage = self.navigate_to_homepage(page, config)
        support_page = SupportPage(page)

        self._verify_navigation_to_sub_page(
            page,
            config,
            homepage,
            support_page,
            homepage.navigation.click_support_item,
            support_sub_page,
        )
