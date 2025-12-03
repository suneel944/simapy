"""YAML file reader utility with optional environment variable substitution"""

import re
from os import environ
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from yaml import safe_load


class YamlReader:
    """Utility class for reading and parsing YAML files"""

    @staticmethod
    def _load_env_file() -> bool:
        """Load .env file if it exists"""
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return True
        return False

    @staticmethod
    def _substitute_env_vars(text: str) -> str:
        """Replace ${VAR_NAME} placeholders with environment variable values

        Supports formats:
        - ${VAR_NAME} - uses environment variable or leaves placeholder if not found
        - ${VAR_NAME:default} - uses environment variable or default value
        - ${VAR_NAME:-default} - uses environment variable or default value

        Args:
            text: String containing environment variable placeholders

        Returns:
            String with environment variables substituted
        """
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

    @staticmethod
    def _replace_env_in_dict(data: Any) -> Any:
        """Recursively replace ${VAR_NAME} placeholders in dict/list/str

        Args:
            data: Data structure (dict, list, str, or other) to process

        Returns:
            Data structure with environment variables substituted
        """
        if isinstance(data, dict):
            return {key: YamlReader._replace_env_in_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [YamlReader._replace_env_in_dict(item) for item in data]
        elif isinstance(data, str):
            return YamlReader._substitute_env_vars(data)
        else:
            return data

    @staticmethod
    def load(
        file_path: str | Path,
        substitute_env_vars: bool = False,
        auto_load_env: bool = False,
    ) -> dict[str, Any]:
        """Load and parse a YAML file

        Args:
            file_path: Path to the YAML file (string or Path object)
            substitute_env_vars: If True, replace ${VAR_NAME} placeholders with environment variables
            auto_load_env: If True, automatically load .env file if it exists (only used if substitute_env_vars is True)

        Returns:
            Parsed YAML data as a dictionary

        Raises:
            FileNotFoundError: If the YAML file does not exist
            yaml.YAMLError: If the YAML file is invalid
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path

        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with open(file_path, encoding="utf-8") as yaml_file:
            yaml_content = yaml_file.read()

        if substitute_env_vars:
            if auto_load_env:
                YamlReader._load_env_file()

            # Replace environment variables in YAML content
            yaml_content = YamlReader._substitute_env_vars(yaml_content)

            # Parse YAML
            data = safe_load(yaml_content)

            # Recursively replace env vars in parsed config (handles nested structures)
            data = YamlReader._replace_env_in_dict(data)
        else:
            # Parse YAML without environment variable substitution
            data = safe_load(yaml_content)

        return data or {}

    @staticmethod
    def load_multiple(
        file_paths: list[str] | list[Path],
        substitute_env_vars: bool = False,
        auto_load_env: bool = False,
    ) -> dict[str, Any]:
        """Load and merge multiple YAML files into a single dictionary

        Args:
            file_paths: List of paths to YAML files
            substitute_env_vars: If True, replace ${VAR_NAME} placeholders with environment variables
            auto_load_env: If True, automatically load .env file if it exists (only used if substitute_env_vars is True)

        Returns:
            Merged dictionary containing data from all YAML files

        Note:
            If multiple files contain the same keys, later files will overwrite earlier ones
        """
        merged_data = {}

        for file_path in file_paths:
            data = YamlReader.load(file_path, substitute_env_vars, auto_load_env)
            merged_data.update(data)

        return merged_data

    @staticmethod
    def load_from_directory(
        directory: str | Path,
        pattern: str = "*.yaml",
        substitute_env_vars: bool = False,
        auto_load_env: bool = False,
    ) -> dict[str, Any]:
        """Load all YAML files from a directory

        Args:
            directory: Path to the directory containing YAML files
            pattern: Glob pattern to match YAML files (default: "*.yaml")
            substitute_env_vars: If True, replace ${VAR_NAME} placeholders with environment variables
            auto_load_env: If True, automatically load .env file if it exists (only used if substitute_env_vars is True)

        Returns:
            Merged dictionary containing data from all YAML files in the directory

        Note:
            Files are processed in alphabetical order. If multiple files contain the same keys,
            later files will overwrite earlier ones
        """
        directory = Path(directory) if isinstance(directory, str) else directory

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        yaml_files = sorted(directory.glob(pattern))
        return YamlReader.load_multiple(yaml_files, substitute_env_vars, auto_load_env)
