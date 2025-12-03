"""Test Content Validation for MultiBank.io"""

import re

import pytest
from playwright.sync_api import expect

from tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestContentValidation(BaseUITest):
    """Test cases for Content Validation"""

    def test_tc_content_core_001_hero_banner_top_section(self, page, config, test_data):
        """TC-CONTENT-CORE-001: Hero banner appears in the top section of the page"""
        homepage = self.navigate_to_homepage(page, config)
        content_data = test_data["content"]
        hero_banner_data = content_data.get("hero_banner", {})

        expect(homepage.hero_banner.banner_section).to_be_visible()

        assert homepage.hero_banner.is_in_top_section(), "Hero banner is not in the top section of the page"

        expect(homepage.hero_banner.text_container).to_be_visible()
        min_length = hero_banner_data.get("min_heading_length", 10)
        expect(homepage.hero_banner.text_container).not_to_have_text("", timeout=10000)
        heading_text = homepage.hero_banner.get_heading_text()
        assert len(heading_text) >= min_length, f"Heading text length {len(heading_text)} is less than {min_length}"

        expected_keywords = hero_banner_data.get("expected_keywords", [])
        heading_lower = heading_text.lower()

        keyword_found = any(keyword.lower() in heading_lower for keyword in expected_keywords)
        assert keyword_found, f"None of the keywords {expected_keywords} found in '{heading_text}'"

    def test_tc_content_core_002_marketing_banners_display(self, page, config, test_data):
        """TC-CONTENT-CORE-002: Marketing banners appear at the page bottom"""
        from tests.utils.reporting.decorators import attach_data

        homepage = self.navigate_to_homepage(page, config)
        content_data = test_data["content"]

        homepage.marketing_banners.scroll_to_bottom()

        banner_count = homepage.marketing_banners.get_count()
        min_count = content_data["marketing_banners"]["min_count"]

        attach_data(
            f"Banner count: {banner_count}\nMinimum required: {min_count}",
            name="Banner Count",
        )

        assert banner_count >= min_count, f"Expected at least {min_count} banners, found {banner_count}"

        expect(homepage.marketing_banners.banners.first).to_be_visible()

    def test_tc_content_core_003_download_section_links(self, page, config, test_data):
        """TC-CONTENT-CORE-003: Download section links correctly to App Store and Google Play"""
        from tests.utils.reporting.decorators import attach_data

        homepage = self.navigate_to_homepage(page, config)
        content_data = test_data["content"]
        download_data = content_data["download_section"]

        homepage.download_section.scroll_into_view()

        expect(homepage.download_section.section_heading).to_be_visible()
        expect(homepage.download_section.app_store_link).to_be_visible()
        expect(homepage.download_section.google_play_link).to_be_visible()

        app_store_url = homepage.download_section.get_app_store_url()
        assert app_store_url, "App Store URL is empty"

        app_store_patterns = download_data["app_store"]["url_patterns"]
        attach_data(
            f"App Store URL: {app_store_url}\nExpected patterns: {app_store_patterns}",
            name="App Store Link",
        )
        assert any(pattern in app_store_url.lower() for pattern in app_store_patterns), (
            f"App Store URL {app_store_url} does not contain any expected patterns"
        )

        google_play_url = homepage.download_section.get_google_play_url()
        assert google_play_url, "Google Play URL is empty"

        google_play_patterns = download_data["google_play"]["url_patterns"]
        attach_data(
            f"Google Play URL: {google_play_url}\nExpected patterns: {google_play_patterns}",
            name="Google Play Link",
        )
        assert any(pattern in google_play_url.lower() for pattern in google_play_patterns), (
            f"Google Play URL {google_play_url} does not contain any expected patterns"
        )

        with page.context.expect_page() as new_page_info:
            homepage.download_section.app_store_link.click(modifiers=["Control"])

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")

        pattern = "|".join(app_store_patterns)
        expect(new_page).to_have_url(re.compile(f".*({pattern}).*", re.IGNORECASE))
        new_page.close()

    def test_tc_content_core_004_download_section_content(self, page, config, test_data):
        """TC-CONTENT-CORE-004: Download section content"""

        homepage = self.navigate_to_homepage(page, config)
        content_data = test_data["content"]
        download_data = content_data["download_section"]

        homepage.download_section.scroll_into_view()

        expect(homepage.download_section.section_heading).to_be_visible()

        keywords = download_data["heading_keywords"]
        assert homepage.download_section.verify_heading_contains_keywords(keywords), (
            f"Heading did not contain expected keywords: {keywords}"
        )

        pattern = download_data["descriptive_text_pattern"]
        assert homepage.download_section.verify_descriptive_text_visible(pattern), (
            f"Descriptive text matching '{pattern}' was not visible"
        )

        if homepage.download_section.has_qr_code():
            expect(homepage.download_section.qr_code.first).to_be_visible()

    def test_tc_content_core_005_about_us_why_multibank_content(self, page, config, test_data):
        """TC-CONTENT-CORE-005: About Us → Why Multibank page renders all expected components with correct text"""
        from tests.pages.multibank.aboutuspage import AboutUsPage

        homepage = self.navigate_to_homepage(page, config)
        content_data = test_data["content"]
        about_data = content_data.get("about_us", {})

        homepage.navigation.click_about_us_item("Why Multibank?")

        page.wait_for_load_state("load")

        about_page = AboutUsPage(page)

        count = about_page.get_content_sections_count()
        assert count > 0, "No content sections found on Why Multibank page"

        placeholder_keywords = about_data.get("placeholder_keywords", [])
        assert about_page.verify_no_placeholder_text(placeholder_keywords), "Placeholder text was found on the page!"
