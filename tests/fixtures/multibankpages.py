"""Fixtures for MultiBank.io page objects"""

from playwright.sync_api import Page
from pytest import fixture

from tests.pages.multibank.aboutuspage import AboutUsPage
from tests.pages.multibank.featurespage import FeaturesPage
from tests.pages.multibank.homepage import HomePage
from tests.pages.multibank.supportpage import SupportPage
from tests.pages.multibank.tradepage import TradePage


@fixture
def homepage(page: Page, config) -> HomePage:
    """Fixture that returns a HomePage instance"""
    return HomePage(page)


@fixture
def aboutuspage(page: Page, config) -> AboutUsPage:
    """Fixture that returns an AboutUsPage instance"""
    return AboutUsPage(page)


@fixture
def featurespage(page: Page, config) -> FeaturesPage:
    """Fixture that returns a FeaturesPage instance"""
    return FeaturesPage(page)


@fixture
def tradepage(page: Page, config) -> TradePage:
    """Fixture that returns a TradePage instance"""
    return TradePage(page)


@fixture
def supportpage(page: Page, config) -> SupportPage:
    """Fixture that returns a SupportPage instance"""
    return SupportPage(page)
