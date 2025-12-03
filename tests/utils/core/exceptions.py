"""Custom exceptions for test framework"""


class FrameworkError(Exception):
    """Base exception for framework errors"""

    pass


class ElementNotFoundError(FrameworkError):
    """Raised when an expected element is not found"""

    pass


class PageLoadError(FrameworkError):
    """Raised when page fails to load"""

    pass


class ConfigurationError(FrameworkError):
    """Raised when configuration is invalid"""

    pass


class TestDataError(FrameworkError):
    """Raised when test data is invalid or missing"""

    pass


class TimeoutError(FrameworkError):
    """Raised when an operation times out"""

    pass
