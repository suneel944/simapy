"""HomePage page object for MultiBank.io"""

from typing import Literal

from playwright.sync_api import Page

from tests.pages.basepage import BasePage
from tests.pages.multibank.components.downloadsection import DownloadSectionComponent
from tests.pages.multibank.components.herobanner import HeroBannerComponent
from tests.pages.multibank.components.marketdata import MarketDataComponent
from tests.pages.multibank.components.marketingbanners import MarketingBannersComponent
from tests.pages.multibank.components.navigation import NavigationComponent
from tests.pages.multibank.components.tradingsection import TradingSectionComponent


class HomePage(BasePage):
    """HomePage for MultiBank.io trading platform"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.navigation = NavigationComponent(page)
        self.hero_banner = HeroBannerComponent(page)
        self.trading_section = TradingSectionComponent(page)
        self.market_data = MarketDataComponent(page)
        self.download_section = DownloadSectionComponent(page)
        self.marketing_banners = MarketingBannersComponent(page)

    def goto(
        self,
        url: str | None = None,
        wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] = "load",
        timeout: int = 30000,
    ) -> None:
        """Navigate to homepage with Playwright's built-in waiting"""
        if not url:
            raise ValueError("url parameter is required")
        super().goto(url, wait_until=wait_until, timeout=timeout)
        # Wait for navigation to be visible to ensure page is ready
        self.navigation.nav_container.wait_for(state="visible", timeout=timeout)
