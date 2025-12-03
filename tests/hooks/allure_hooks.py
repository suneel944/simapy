"""Allure reporting hooks to abstract reporting from test layer"""

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Page

from tests.utils.reporting.helpers import AllureHelper


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure Allure environment"""
    allure.dynamic.epic("MultiBank.io UI Tests")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Setup hook - add Allure metadata before test execution"""
    # Extract feature from test class
    if hasattr(item, "cls") and item.cls:
        class_name = item.cls.__name__
        if "Navigation" in class_name:
            allure.dynamic.feature("Navigation & Layout")
        elif "Trading" in class_name:
            allure.dynamic.feature("Trading Functionality")
        elif "Content" in class_name:
            allure.dynamic.feature("Content Validation")

    # Extract story from test name
    test_name = item.name
    if "navigation" in test_name.lower() or "nav" in test_name.lower():
        allure.dynamic.story("Navigation")
    elif "trading" in test_name.lower() or "trade" in test_name.lower():
        allure.dynamic.story("Trading")
    elif "content" in test_name.lower() or "marketing" in test_name.lower() or "download" in test_name.lower():
        allure.dynamic.story("Content")

    # Set severity based on test name
    if "core_001" in test_name or "core_002" in test_name:
        allure.dynamic.severity(allure.severity_level.CRITICAL)
    else:
        allure.dynamic.severity(allure.severity_level.NORMAL)

    # Set title from docstring or test name
    if item.function.__doc__:
        title = item.function.__doc__.strip().split("\n")[0]
        allure.dynamic.title(title)
    else:
        allure.dynamic.title(test_name.replace("_", " ").title())

    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to attach screenshots and HTML on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Get page from test item if available
        for fixture_name in item.fixturenames:
            if fixture_name == "page":
                page = item.funcargs.get("page")
                if page and isinstance(page, Page):
                    try:
                        AllureHelper.attach_screenshot_on_failure(page, "test_failure_screenshot")
                        AllureHelper.attach_page_html(page, "test_failure_page_html")
                    except Exception:
                        pass
                break


@pytest.fixture(scope="function", autouse=True)
def allure_attach_page_data(page: Page):
    """Fixture to attach page data to Allure report after test execution"""
    yield

    # Attach page URL and title after test
    try:
        page_url = page.url
        page_title = page.title()
        allure.attach(
            f"URL: {page_url}\nTitle: {page_title}",
            name="Page Information",
            attachment_type=AttachmentType.TEXT,
        )
    except Exception:
        pass
