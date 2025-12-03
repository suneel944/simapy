from playwright.sync_api import Page, Playwright
from pytest import fixture

from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


@fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-qa-id")


@fixture(autouse=True)
def cleanup_browser_state(page: Page):
    """Cleanup browser state between tests to ensure test isolation

    This fixture runs automatically before each test to clear:
    - Cookies
    - Local storage
    - Session storage
    - Cache (if possible)

    This ensures no stale state affects tests, which is critical for parallel execution.
    """
    # Clear cookies
    try:
        page.context.clear_cookies()
        logger.debug("Cleared cookies for test isolation")
    except Exception as e:
        logger.warning(f"Failed to clear cookies: {str(e)}")

    # Clear storage
    try:
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        logger.debug("Cleared localStorage and sessionStorage for test isolation")
    except Exception as e:
        logger.warning(f"Failed to clear storage: {str(e)}")

    yield

    # Post-test cleanup
    try:
        # Clear any remaining state
        page.context.clear_cookies()
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        logger.debug("Post-test cleanup completed")
    except Exception as e:
        logger.warning(f"Post-test cleanup failed: {str(e)}")


@fixture(scope="session")
def browser_context_args(config: dict):
    playwright_config = config.get("Playwright", {})
    viewport_config = playwright_config.get("viewport", {})

    context_args = {
        # Stealth: Realistic user agent
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        # Stealth: Realistic locale and timezone
        "locale": "en-US",
        "timezone_id": "America/New_York",
        # Stealth: Realistic permissions
        "permissions": ["geolocation"],
        # Stealth: Realistic geolocation
        "geolocation": {"longitude": -74.006, "latitude": 40.7128},
        # Stealth: Realistic color scheme
        "color_scheme": "light",
        # Stealth: Reduce automation detection
        "ignore_https_errors": False,
        # Stealth: Realistic device scale factor
        "device_scale_factor": 1,
    }

    if viewport_config:
        context_args["viewport"] = {
            "width": viewport_config.get("width", 1280),
            "height": viewport_config.get("height", 720),
        }

    return context_args


@fixture(scope="session")
def browser_type_launch_args(config: dict):
    playwright_config = config.get("Playwright", {})

    launch_args = {}

    if "headed" in playwright_config:
        launch_args["headless"] = not playwright_config["headed"]

    return launch_args
