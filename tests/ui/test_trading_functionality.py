"""Test Trading Functionality for MultiBank.io"""

import pytest
from playwright.sync_api import expect

from tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestTradingFunctionality(BaseUITest):
    """Test cases for Trading Functionality"""

    def test_tc_trade_core_001_spot_trading_section_display(self, page, config):
        """TC-TRADE-CORE-001: Spot trading section displays trading pairs across different categories"""
        homepage = self.navigate_to_homepage(page, config)

        expect(homepage.trading_section.spot_tab).to_be_visible()
        homepage.trading_section.click_spot_tab()

        element_timeout = self.get_timeout(config, "element_timeout", 10000)
        expect(homepage.trading_section.trading_pairs_table).to_be_visible(timeout=element_timeout)
        expect(homepage.trading_section.favorites_button).to_be_visible()
        expect(homepage.trading_section.all_button).to_be_visible()

    def test_tc_trade_core_002_trading_pair_data_structure(self, page, config, test_data):
        """TC-TRADE-CORE-002: Trading pair data structure and presentation is correct"""
        from tests.utils.reporting.decorators import attach_data

        homepage = self.navigate_to_homepage(page, config)
        trading_data = test_data["trading"]

        homepage.trading_section.click_spot_tab()
        # click_spot_tab already waits for table to be visible, no additional wait needed

        actual_headers = homepage.trading_section.get_actual_table_headers()
        header_text = " ".join(actual_headers).lower()
        attach_data(
            f"Table Headers: {actual_headers}",
            name="Trading Table Headers",
        )
        assert "pair" in header_text and len(actual_headers) > 0, (
            f"Expected 'pair' in headers and headers count > 0, got headers: {actual_headers}"
        )

        pairs_data = homepage.trading_section.get_trading_pairs_data()
        assert len(pairs_data) > 0, f"Expected trading pairs data, but got {len(pairs_data)} pairs"

        min_pairs = trading_data["table"]["min_pairs_to_check"]
        required_field = trading_data["table"]["required_field"]
        attach_data(
            pairs_data[:min_pairs],
            name="Trading Pairs Data",
            attachment_type="json",
        )
        for pair in pairs_data[:min_pairs]:
            assert pair.get(required_field) and pair[required_field], (
                f"Expected '{required_field}' field in pair data, got: {pair}"
            )

    def test_tc_trade_core_003_trading_pair_filtering(self, page, config):
        """TC-TRADE-CORE-003: Trading pair filtering and sorting"""
        from tests.utils.reporting.decorators import attach_data

        homepage = self.navigate_to_homepage(page, config)

        homepage.trading_section.click_spot_tab()

        short_timeout = self.get_timeout(config, "short_timeout", 2000)
        if homepage.trading_section.favorites_button.is_visible(timeout=short_timeout):
            # Click All filter to see all pairs
            homepage.trading_section.click_all_filter()
            all_count = homepage.trading_section.get_trading_pairs_count()

            # Favorite at least one pair by clicking its star icon
            # This is required for the Favorites filter to show any results
            assert all_count > 0, f"Expected trading pairs to be available, got {all_count}"
            homepage.trading_section.favorite_trading_pair(row_index=0)

            # Now click Favorites filter to see favorited pairs
            homepage.trading_section.click_favorites_filter()
            favorites_count = homepage.trading_section.get_trading_pairs_count()

            attach_data(
                f"All count: {all_count}\nFavorites count: {favorites_count}",
                name="Filter Counts",
            )

            # Verify favorites count is greater than 0 (since we favorited at least one)
            # and less than or equal to all count
            assert favorites_count > 0, f"Expected favorites count > 0 after favoriting a pair, got {favorites_count}"
            assert favorites_count <= all_count, (
                f"Expected favorites count ({favorites_count}) <= all count ({all_count})"
            )
        else:
            # Filters not available, just verify table has data
            count = homepage.trading_section.get_trading_pairs_count()
            attach_data(f"Trading pairs count: {count}", name="Trading Pairs Count")
            assert count > 0, f"Expected trading pairs count > 0, got {count}"

    def test_tc_trade_core_004_trading_pair_interaction(self, page, config, test_data):
        """TC-TRADE-CORE-004: Trading pair interaction - Market data buttons display and interaction"""
        homepage = self.navigate_to_homepage(page, config)

        homepage.trading_section.click_spot_tab()
        # click_spot_tab already waits for table to be visible, no additional wait needed

        expect(homepage.market_data.top_gainer_button).to_be_visible()
        expect(homepage.market_data.top_loser_button).to_be_visible()

        homepage.market_data.click_top_gainer()
        homepage.market_data.click_top_loser()
