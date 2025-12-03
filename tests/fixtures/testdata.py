"""Fixtures for loading test data"""

from pathlib import Path

import pytest
from pytest import fixture, param

from tests.utils.data.validation import TestDataError, validate_full_test_data
from tests.utils.data.yaml_reader import YamlReader
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


def _load_test_data() -> dict:
    """Internal function to load test data (used by both fixture and parametrized fixtures)

    Returns:
        Dictionary containing validated test data

    Raises:
        TestDataError: If test data is invalid or missing
    """
    data_dir = Path(__file__).parent.parent / "data"
    test_data = {}

    yaml_files = {
        "navigation": "navigation_test_data.yaml",
        "trading": "trading_test_data.yaml",
        "content": "content_test_data.yaml",
    }

    for key, filename in yaml_files.items():
        file_path = data_dir / filename
        if file_path.exists():
            try:
                loaded_data = YamlReader.load(file_path)
                # YAML files have top-level key matching the filename, extract the actual data
                test_data[key] = loaded_data.get(key, loaded_data)
                logger.debug(f"Loaded test data from {filename}")
            except Exception as e:
                error_msg = f"Failed to load test data from {filename}: {str(e)}"
                logger.error(error_msg)
                raise TestDataError(error_msg) from e
        else:
            error_msg = f"Test data file not found: {file_path}"
            logger.error(error_msg)
            raise TestDataError(error_msg)

    # Validate test data structure
    try:
        validate_full_test_data(test_data)
    except TestDataError as e:
        logger.error(f"Test data validation failed: {str(e)}")
        raise

    return test_data


@fixture(scope="session")
def test_data() -> dict:
    """Load and validate all test data YAML files

    Returns:
        Dictionary containing validated test data

    Raises:
        TestDataError: If test data is invalid or missing
    """
    return _load_test_data()


@fixture(scope="session")
def about_us_sub_page(request):
    """Parametrized fixture for About Us sub-pages

    Yields each sub-page name from test data.
    If no sub-pages exist, the fixture will be skipped.
    """
    test_data = _load_test_data()
    content_data = test_data.get("content", {})
    about_data = content_data.get("about_us", {})
    sub_pages = about_data.get("sub_pages", [])

    if not sub_pages:
        pytest.skip("No sub pages defined for About Us in test data")

    return request.param


@fixture(scope="session")
def trade_sub_page(request):
    """Parametrized fixture for Trade sub-pages

    Yields each sub-page name from test data.
    If no sub-pages exist, the fixture will be skipped.
    """
    test_data = _load_test_data()
    content_data = test_data.get("content", {})
    trade_data = content_data.get("trade", {})
    sub_pages = trade_data.get("sub_pages", [])

    if not sub_pages:
        pytest.skip("No sub pages defined for Trade in test data")

    return request.param


@fixture(scope="session")
def features_sub_page(request):
    """Parametrized fixture for Features sub-pages

    Yields each sub-page name from test data.
    If no sub-pages exist, the fixture will be skipped.
    """
    test_data = _load_test_data()
    content_data = test_data.get("content", {})
    features_data = content_data.get("features", {})
    sub_pages = features_data.get("sub_pages", [])

    if not sub_pages:
        pytest.skip("No sub pages defined for Features in test data")

    return request.param


@fixture(scope="session")
def support_sub_page(request):
    """Parametrized fixture for Support sub-pages

    Yields each sub-page name from test data.
    If no sub-pages exist, the fixture will be skipped.
    """
    test_data = _load_test_data()
    content_data = test_data.get("content", {})
    support_data = content_data.get("support", {})
    sub_pages = support_data.get("sub_pages", [])

    if not sub_pages:
        pytest.skip("No sub pages defined for Support in test data")

    return request.param


def pytest_generate_tests(metafunc):
    """Dynamically parametrize fixtures based on test data

    This hook runs at collection time and sets up parametrized fixtures
    with values from test data, allowing fixtures to be used directly in tests.
    """
    test_data = _load_test_data()
    content_data = test_data.get("content", {})

    if "about_us_sub_page" in metafunc.fixturenames:
        sub_pages = content_data.get("about_us", {}).get("sub_pages", [])
        if sub_pages:
            metafunc.parametrize("about_us_sub_page", [param(name, id=name) for name in sub_pages])
        else:
            metafunc.parametrize("about_us_sub_page", [], indirect=True)

    if "trade_sub_page" in metafunc.fixturenames:
        sub_pages = content_data.get("trade", {}).get("sub_pages", [])
        if sub_pages:
            metafunc.parametrize("trade_sub_page", [param(name, id=name) for name in sub_pages])
        else:
            metafunc.parametrize("trade_sub_page", [], indirect=True)

    if "features_sub_page" in metafunc.fixturenames:
        sub_pages = content_data.get("features", {}).get("sub_pages", [])
        if sub_pages:
            metafunc.parametrize("features_sub_page", [param(name, id=name) for name in sub_pages])
        else:
            metafunc.parametrize("features_sub_page", [], indirect=True)

    if "support_sub_page" in metafunc.fixturenames:
        sub_pages = content_data.get("support", {}).get("sub_pages", [])
        if sub_pages:
            metafunc.parametrize("support_sub_page", [param(name, id=name) for name in sub_pages])
        else:
            metafunc.parametrize("support_sub_page", [], indirect=True)
