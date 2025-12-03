"""Trading section component for MultiBank.io"""

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from tests.utils.core.exceptions import ElementNotFoundError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


class TradingSectionComponent:
    """Spot Trading Section Component"""

    def __init__(self, page: Page):
        self.page = page
        self.spot_tab = page.get_by_role("button", name="Spot", exact=True)
        self.trading_pairs_table = page.locator("table").first
        self.favorites_button = page.get_by_text("Favorites", exact=False)
        self.all_button = page.get_by_text("All", exact=True)

    def is_spot_section_visible(self, timeout: int = 5000) -> bool:
        """Check if Spot trading section is visible using Playwright's auto-wait"""
        try:
            self.spot_tab.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def click_spot_tab(self, timeout: int = 10000) -> None:
        """Click Spot tab with auto-wait and wait for table to load

        Args:
            timeout: Maximum time to wait for elements

        Raises:
            ElementNotFoundError: If spot tab or trading table is not found
        """
        try:
            logger.debug("Clicking Spot tab")
            self.spot_tab.wait_for(state="visible", timeout=timeout)
            self.spot_tab.click()
            logger.debug("Waiting for trading pairs table to load")
            self.trading_pairs_table.wait_for(state="visible", timeout=timeout)
            logger.info("Spot tab clicked and trading table loaded successfully")
        except PlaywrightTimeoutError as e:
            error_msg = f"Failed to click spot tab or load trading table within {timeout}ms"
            logger.error(error_msg)
            raise ElementNotFoundError(error_msg) from e

    def get_trading_pairs_data(self, timeout: int = 10000) -> list[dict]:
        """Extract trading pairs data from table using Playwright's locator API

        Args:
            timeout: Maximum time to wait for table rows

        Returns:
            List of dictionaries containing trading pair data
        """
        pairs_data: list[dict[str, str]] = []
        rows_locator = self.trading_pairs_table.locator("tbody tr")

        # Wait for at least one row to be visible
        try:
            rows_locator.first.wait_for(state="visible", timeout=timeout)
            logger.debug("Trading pairs table rows found")
        except PlaywrightTimeoutError:
            logger.warning(f"No trading pairs found in table within {timeout}ms")
            return pairs_data

        row_count = rows_locator.count()

        for i in range(row_count):
            try:
                row = rows_locator.nth(i)
                row.wait_for(state="attached", timeout=2000)
                cells = row.locator("td")
                cell_count = cells.count()

                if cell_count >= 2:  # At least empty first cell + pair name
                    # Skip first empty cell, then: Pair, Price, 24h Change, High, Low, Last 7 days
                    pair_data = {
                        "pair": cells.nth(1).inner_text().strip() if cell_count > 1 else "",
                        "price": cells.nth(2).inner_text().strip() if cell_count > 2 else "",
                        "change_24h": cells.nth(3).inner_text().strip() if cell_count > 3 else "",
                        "high": cells.nth(4).inner_text().strip() if cell_count > 4 else "",
                        "low": cells.nth(5).inner_text().strip() if cell_count > 5 else "",
                        "last_7_days": cells.nth(6).inner_text().strip() if cell_count > 6 else "",
                    }
                    if pair_data["pair"]:  # Only add if pair name exists
                        pairs_data.append(pair_data)
            except PlaywrightTimeoutError as e:
                logger.warning(f"Failed to extract data from row {i}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error extracting data from row {i}: {str(e)}")
                continue

        logger.info(f"Extracted {len(pairs_data)} trading pairs from table")
        return pairs_data

    def get_expected_table_headers(self) -> list[str]:
        """Get expected table headers"""
        return ["Pair", "Price", "24h Change", "High", "Low", "Last 7 days"]

    def get_actual_table_headers(self, timeout: int = 5000) -> list[str]:
        """Get actual table headers from page using Playwright's locator API"""
        headers: list[str] = []
        header_locator = self.trading_pairs_table.locator("thead th")

        try:
            header_locator.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            return headers

        header_count = header_locator.count()

        for i in range(header_count):
            try:
                header = header_locator.nth(i)
                text = header.inner_text()
                if text and text.strip():  # Only add non-empty headers
                    headers.append(text.strip())
            except Exception:
                continue
        return headers

    def click_favorites_filter(self, timeout: int = 10000) -> None:
        """Click Favorites filter with auto-wait"""
        self.favorites_button.wait_for(state="visible", timeout=timeout)
        self.favorites_button.click()
        # Wait for table rows to update after filter is applied
        rows_locator = self.trading_pairs_table.locator("tbody tr")
        try:
            rows_locator.first.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            pass  # Table may be empty, that's okay

    def click_all_filter(self, timeout: int = 10000) -> None:
        """Click All filter with auto-wait"""
        self.all_button.wait_for(state="visible", timeout=timeout)
        self.all_button.click()
        # Wait for table rows to update after filter is applied
        rows_locator = self.trading_pairs_table.locator("tbody tr")
        try:
            rows_locator.first.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            pass  # Table may be empty, that's okay

    def get_trading_pairs_count(self, timeout: int = 5000) -> int:
        """Get count of visible trading pairs using Playwright's count API"""
        rows_locator = self.trading_pairs_table.locator("tbody tr")
        try:
            rows_locator.first.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            return 0
        return rows_locator.count()

    def favorite_trading_pair(self, row_index: int = 0, timeout: int = 10000) -> None:
        """Click star icon to favorite a trading pair in the specified row"""
        row = self.trading_pairs_table.locator("tbody tr").nth(row_index)
        row.locator("td").first.click(timeout=timeout)
