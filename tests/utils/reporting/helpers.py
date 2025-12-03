"""Allure reporting helpers for test framework"""

import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page


class AllureHelper:
    """Helper class for Allure reporting operations"""

    @staticmethod
    @allure.step("Take screenshot")
    def attach_screenshot(page: Page, name: str = "screenshot"):
        """Attach screenshot to Allure report"""
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=AttachmentType.PNG,
        )

    @staticmethod
    @allure.step("Attach page HTML")
    def attach_page_html(page: Page, name: str = "page_html"):
        """Attach page HTML to Allure report"""
        html = page.content()
        allure.attach(
            html,
            name=name,
            attachment_type=AttachmentType.HTML,
        )

    @staticmethod
    @allure.step("Attach page screenshot on failure")
    def attach_screenshot_on_failure(page: Page, name: str = "failure_screenshot"):
        """Attach screenshot when test fails"""
        try:
            AllureHelper.attach_screenshot(page, name)
        except Exception as e:
            allure.attach(
                f"Failed to capture screenshot: {str(e)}",
                name="screenshot_error",
                attachment_type=AttachmentType.TEXT,
            )

    @staticmethod
    def attach_text(text: str, name: str = "text_attachment"):
        """Attach text to Allure report"""
        allure.attach(
            text,
            name=name,
            attachment_type=AttachmentType.TEXT,
        )

    @staticmethod
    def attach_json(data: dict, name: str = "json_attachment"):
        """Attach JSON data to Allure report"""
        import json

        allure.attach(
            json.dumps(data, indent=2),
            name=name,
            attachment_type=AttachmentType.JSON,
        )

    @staticmethod
    @allure.step("{step_name}")
    def step(step_name: str):
        """Create an Allure step"""
        pass
