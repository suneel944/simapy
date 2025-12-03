"""Configuration validation utilities"""

from typing import Any


class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""

    pass


def validate_config(config: dict[str, Any], required_keys: list[str] | None = None) -> None:
    """
    Validate configuration dictionary has required keys

    Args:
        config: Configuration dictionary to validate
        required_keys: List of required top-level keys. If None, uses default required keys

    Raises:
        ConfigValidationError: If required keys are missing
    """
    if not isinstance(config, dict):
        raise ConfigValidationError(f"Config must be a dictionary, got {type(config)}")

    if required_keys is None:
        required_keys = ["MultiBank", "Playwright"]

    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ConfigValidationError(f"Missing required configuration keys: {', '.join(missing_keys)}")


def validate_multibank_config(multibank_config: dict[str, Any]) -> None:
    """
    Validate MultiBank configuration section

    Args:
        multibank_config: MultiBank configuration dictionary

    Raises:
        ConfigValidationError: If required fields are missing or invalid
    """
    if not isinstance(multibank_config, dict):
        raise ConfigValidationError("MultiBank config must be a dictionary")

    required_fields = ["base_url"]
    missing_fields = [field for field in required_fields if field not in multibank_config]

    if missing_fields:
        raise ConfigValidationError(f"MultiBank config missing required fields: {', '.join(missing_fields)}")

    base_url = multibank_config.get("base_url", "")
    if not base_url or not isinstance(base_url, str):
        raise ConfigValidationError("MultiBank base_url must be a non-empty string")

    if not base_url.startswith(("http://", "https://")):
        raise ConfigValidationError(f"MultiBank base_url must start with http:// or https://, got: {base_url}")


def validate_playwright_config(playwright_config: dict[str, Any]) -> None:
    """
    Validate Playwright configuration section

    Args:
        playwright_config: Playwright configuration dictionary

    Raises:
        ConfigValidationError: If required fields are missing or invalid
    """
    if not isinstance(playwright_config, dict):
        raise ConfigValidationError("Playwright config must be a dictionary")

    # Validate viewport
    viewport = playwright_config.get("viewport", {})
    if not isinstance(viewport, dict):
        raise ConfigValidationError("Playwright viewport must be a dictionary")

    required_viewport_fields = ["width", "height"]
    missing_viewport_fields = [field for field in required_viewport_fields if field not in viewport]

    if missing_viewport_fields:
        raise ConfigValidationError(
            f"Playwright viewport missing required fields: {', '.join(missing_viewport_fields)}"
        )

    # Validate viewport dimensions
    width = viewport.get("width")
    height = viewport.get("height")

    if not isinstance(width, int) or width <= 0:
        raise ConfigValidationError(f"Playwright viewport width must be a positive integer, got: {width}")

    if not isinstance(height, int) or height <= 0:
        raise ConfigValidationError(f"Playwright viewport height must be a positive integer, got: {height}")

    # Validate timeouts
    timeout_keys = [
        "navigation_timeout",
        "load_state_timeout",
        "element_timeout",
        "short_timeout",
    ]

    for timeout_key in timeout_keys:
        timeout_value = playwright_config.get(timeout_key)
        if timeout_value is not None:
            if not isinstance(timeout_value, int) or timeout_value <= 0:
                raise ConfigValidationError(
                    f"Playwright {timeout_key} must be a positive integer, got: {timeout_value}"
                )

    # Validate headed flag
    headed = playwright_config.get("headed")
    if headed is not None and not isinstance(headed, bool):
        raise ConfigValidationError(f"Playwright headed must be a boolean, got: {type(headed)}")


def validate_full_config(config: dict[str, Any]) -> None:
    """
    Validate complete configuration dictionary

    Args:
        config: Complete configuration dictionary

    Raises:
        ConfigValidationError: If validation fails
    """
    # Validate top-level structure
    validate_config(config)

    # Validate MultiBank section
    if "MultiBank" in config:
        validate_multibank_config(config["MultiBank"])

    # Validate Playwright section
    if "Playwright" in config:
        validate_playwright_config(config["Playwright"])
