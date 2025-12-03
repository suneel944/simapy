import re
from os import environ, path
from pathlib import Path

from dotenv import load_dotenv
from pytest import Config, fixture
from yaml import safe_load

from tests.utils.config.validation import ConfigValidationError, validate_full_config
from tests.utils.logging.logger import get_logger

logger = get_logger(__name__)


def _load_env_file():
    """Load .env file if it exists"""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        return True
    return False


def _substitute_env_vars(text: str) -> str:
    """Replace ${VAR_NAME} placeholders with environment variable values"""
    # Pattern matches ${VAR_NAME} or ${VAR_NAME:default} or ${VAR_NAME:-default}
    # Handles both :default and :-default formats
    pattern = r"\$\{([^}:]+)(?::([^}]*))?\}"

    def replace_match(match):
        var_name = match.group(1)
        default_value = match.group(2) if match.group(2) else None
        env_value = environ.get(var_name)
        if env_value is not None:
            return env_value
        elif default_value is not None:
            return default_value
        else:
            return match.group(0)

    return re.sub(pattern, replace_match, text)


def _replace_env_in_dict(data):
    """Recursively replace ${VAR_NAME} placeholders in dict/list/str"""
    if isinstance(data, dict):
        return {key: _replace_env_in_dict(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_replace_env_in_dict(item) for item in data]
    elif isinstance(data, str):
        return _substitute_env_vars(data)
    else:
        return data


@fixture(scope="session")
def config(pytestconfig: Config):
    """Load and validate configuration for test execution"""
    # Load .env file first
    _load_env_file()

    # Get environment: CLI arg > .env ENV variable > default "dev"
    env = pytestconfig.getoption("--env", default=None)
    if env is None:
        env = environ.get("ENV", "dev")

    logger.info(f"Loading configuration for environment: {env}")

    config_path = path.join(Path.cwd(), "configs", f"{env}.yaml")

    if not path.exists(config_path):
        error_msg = f"Config file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(config_path, encoding="utf-8") as config_file:
            config_content = config_file.read()

        # Replace environment variables in YAML content
        config_content = _substitute_env_vars(config_content)

        # Parse YAML
        config = safe_load(config_content)

        if config is None:
            error_msg = f"Config file is empty or invalid: {config_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Recursively replace env vars in parsed config (handles nested structures)
        config = _replace_env_in_dict(config)

        # Validate configuration
        try:
            validate_full_config(config)
            logger.info("Configuration validated successfully")
        except ConfigValidationError as e:
            error_msg = f"Configuration validation failed: {str(e)}"
            logger.error(error_msg)
            raise ConfigValidationError(error_msg) from e

        return config

    except FileNotFoundError:
        raise
    except Exception as e:
        error_msg = f"Failed to load configuration from {config_path}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e
