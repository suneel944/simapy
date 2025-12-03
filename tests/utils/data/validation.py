"""Test data validation utilities"""

from typing import Any

from tests.utils.core.exceptions import TestDataError
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


def validate_test_data_structure(test_data: dict[str, Any], required_keys: list[str]) -> None:
    """
    Validate test data has required top-level keys

    Args:
        test_data: Test data dictionary to validate
        required_keys: List of required top-level keys

    Raises:
        TestDataError: If required keys are missing
    """
    if not isinstance(test_data, dict):
        raise TestDataError(f"Test data must be a dictionary, got {type(test_data)}")

    missing_keys = [key for key in required_keys if key not in test_data]
    if missing_keys:
        error_msg = f"Test data missing required keys: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise TestDataError(error_msg)


def validate_navigation_data(navigation_data: dict[str, Any]) -> None:
    """
    Validate navigation test data structure

    Args:
        navigation_data: Navigation test data dictionary

    Raises:
        TestDataError: If navigation data is invalid
    """
    if not isinstance(navigation_data, dict):
        raise TestDataError("Navigation data must be a dictionary")

    required_fields = ["expected_items", "url_patterns"]
    missing_fields = [field for field in required_fields if field not in navigation_data]

    if missing_fields:
        error_msg = f"Navigation data missing required fields: {', '.join(missing_fields)}"
        logger.error(error_msg)
        raise TestDataError(error_msg)

    # Validate expected_items is a list
    expected_items = navigation_data.get("expected_items", [])
    if not isinstance(expected_items, list):
        raise TestDataError("Navigation expected_items must be a list")

    # Validate url_patterns is a dict
    url_patterns = navigation_data.get("url_patterns", {})
    if not isinstance(url_patterns, dict):
        raise TestDataError("Navigation url_patterns must be a dictionary")


def validate_trading_data(trading_data: dict[str, Any]) -> None:
    """
    Validate trading test data structure

    Args:
        trading_data: Trading test data dictionary

    Raises:
        TestDataError: If trading data is invalid
    """
    if not isinstance(trading_data, dict):
        raise TestDataError("Trading data must be a dictionary")

    # Check for table data
    if "table" in trading_data:
        table_data = trading_data["table"]
        if not isinstance(table_data, dict):
            raise TestDataError("Trading table data must be a dictionary")

        required_table_fields = ["min_pairs_to_check", "required_field"]
        missing_fields = [field for field in required_table_fields if field not in table_data]

        if missing_fields:
            error_msg = f"Trading table data missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise TestDataError(error_msg)


def validate_content_data(content_data: dict[str, Any]) -> None:
    """
    Validate content test data structure

    Args:
        content_data: Content test data dictionary

    Raises:
        TestDataError: If content data is invalid
    """
    if not isinstance(content_data, dict):
        raise TestDataError("Content data must be a dictionary")

    # Validate marketing_banners if present
    if "marketing_banners" in content_data:
        banners_data = content_data["marketing_banners"]
        if not isinstance(banners_data, dict):
            raise TestDataError("Marketing banners data must be a dictionary")

        if "min_count" not in banners_data:
            raise TestDataError("Marketing banners data missing 'min_count' field")

        min_count = banners_data.get("min_count")
        if not isinstance(min_count, int) or min_count < 0:
            raise TestDataError("Marketing banners min_count must be a non-negative integer")

    # Validate download_section if present
    if "download_section" in content_data:
        download_data = content_data["download_section"]
        if not isinstance(download_data, dict):
            raise TestDataError("Download section data must be a dictionary")

        required_fields = ["heading_keywords", "descriptive_text_pattern"]
        missing_fields = [field for field in required_fields if field not in download_data]

        if missing_fields:
            error_msg = f"Download section data missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise TestDataError(error_msg)


def validate_full_test_data(test_data: dict[str, Any]) -> None:
    """
    Validate complete test data structure

    Args:
        test_data: Complete test data dictionary

    Raises:
        TestDataError: If validation fails
    """
    # Validate top-level structure
    required_keys = ["navigation", "trading", "content"]
    validate_test_data_structure(test_data, required_keys)

    # Validate each section
    if "navigation" in test_data:
        validate_navigation_data(test_data["navigation"])

    if "trading" in test_data:
        validate_trading_data(test_data["trading"])

    if "content" in test_data:
        validate_content_data(test_data["content"])

    logger.info("Test data validation passed")
