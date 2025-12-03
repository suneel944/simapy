"""Constants for test framework"""

from enum import Enum, unique


@unique
class ConfigKeys(Enum):
    """Configuration keys enum"""

    MULTIBANK = "MultiBank"
    BASE_URL = "base_url"
    ELEMENT_VISIBILITY_TIMEOUT = "element_visibility_timeout"
    PLAYWRIGHT = "Playwright"
    NAVIGATION_TIMEOUT = "navigation_timeout"
    LOAD_STATE_TIMEOUT = "load_state_timeout"


@unique
class TestDataFilePaths(Enum):
    CONTENT_DATA = "tests/data/content_test_data.yaml"
    NAVIGATION_DATA = "tests/data/navigation_test_data.yaml"
    TRADING_DATA = "tests/data/trading_test_data.yaml"
