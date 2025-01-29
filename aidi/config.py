"""Module for loading and managing configuration for an LLM-based tool.

This module defines the `LoadConfig` class, which is responsible for loading
configuration from a YAML file, extracting service-specific settings, setting
environment variables, and providing access to the full configuration for the
tool.

It supports the configuration of different LLM services, such as OpenAI, by
reading relevant keys from the YAML configuration and setting necessary
environment variables like API keys for authentication.

Functions provided by `LoadConfig` allow you to:
- Load YAML configuration files.
- Extract service-specific configuration.
- Set up environment variables based on the selected service.
- Retrieve full configuration details including logging settings, custom
configurations, and service settings.

The module can be executed as a standalone script for testing purposes,
which will display the loaded configuration and environment variables.

Example usage:
    - Initialize `LoadConfig` with the path to a YAML configuration file.
    - Retrieve service settings, logging configurations, and environment
      variables.
"""

import os
from typing import Any, Dict, List, Tuple

import yaml
from rich import print as print


class LoadConfig:
    """A class to load and manage configuration settings for the system.

    This class reads a YAML configuration file, extracts settings related
    to the active LLM service, and sets environment variables required for
    LLM API interactions (e.g., OpenAI API key).
    It also retrieves the service-specific configuration, logging settings,
    and other configurations necessary for the tool to function.

    Attributes:
        config_path (str): Path to the configuration YAML file.
        config (Dict[str, Any]): Loaded configuration dictionary.
        llm_service (str): The active LLM service specified in the conf.
        service_config (Dict[str, Any]): The configuration specific to
        the active LLM service.
        config_list (List[Dict[str, Any]]): Configuration list for the service.
        custom_config_list (List[Dict[str, str]]): Custom configuration list
        for the service.
        log_config (Dict[str, Any]): Logging settings from the configuration.
        full_config (Dict[str, Any]): Full configuration dictionary.

    Methods:
        load_yaml_config(file_path: str) -> Dict[str, Any]:
            Loads the YAML configuration file and returns its content as a
            dictionary.

        _get_service_config() -> Dict[str, Any]:
            Retrieves and returns the configuration specific to the active
            LLM service.

        _set_environment_variables():
            Sets the necessary environment variables (e.g., OpenAI API key)
            based on the configuration.

        get_configuration() -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]
        , Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
            Returns the configuration lists and additional settings for the
            active service, logging, and full configuration.
    """

    def __init__(self, config_path: str = "config_aidi.yaml"):
        """Load Configuration Init.

        Args:
            config_path (str, optional): _description_.
            Defaults to "config_aidi.yaml".
        """
        self.config_path = config_path
        self.config = self.load_yaml_config(self.config_path)
        self.llm_service = self.config["active_service"]
        self.service_config = self._get_service_config()
        self._set_environment_variables()
        self.config_list = self.service_config.get("config_list", [])
        self.custom_config_list = self.service_config.get(
            "custom_config_list", []
        )
        self.log_config = self.config["logging"]
        self.full_config = self.config
        self._create_code_folder()  # Ensure the `code_folder` exists

    @staticmethod
    def load_yaml_config(file_path: str) -> Dict[str, Any]:
        """Loads the configuration from a YAML file."""
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def _get_service_config(self) -> Dict[str, Any]:
        """Retrieves the specific service configuration."""
        service_config = self.config["services"].get(self.llm_service)
        if not service_config:
            raise Exception(f"Unsupported LLM service: {self.llm_service}")
        return service_config

    def _set_environment_variables(self):
        """Sets environment variables for LLM services if required."""
        if self.llm_service == "OpenAI":
            openai_api_key = self.service_config.get("api_key")
            if openai_api_key:
                os.environ["OPENAI_API_KEY"] = openai_api_key
            else:
                raise ValueError(
                    "API key for OpenAI service is missing in the conf."
                )

    def _create_code_folder(self):
        """Create code folder.

        Ensures the `code_folder` directory exists, creating
        it if necessary.
        """
        code_folder = self.config.get("code", {}).get("code_folder")
        try:
            if not os.path.exists(code_folder):
                os.makedirs(code_folder)
        except OSError as e:
            print(f"Failed to create code folder '{code_folder}': {e}")

    def get_configuration(
        self,
    ) -> Tuple[
        List[Dict[str, Any]],
        List[Dict[str, str]],
        Dict[str, Any],
        Dict[str, Any],
        Dict[str, Any],
    ]:
        """Returns the configuration lists and settings for the service."""
        return (
            self.config_list,
            self.custom_config_list,
            self.service_config,
            self.log_config,
            self.full_config,
        )


# Execute main if script is run directly for testing purposes
if __name__ == "__main__":
    # Example usage:
    # Set llm_service as "OpenAI" or "ollama"
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()
    print("LLM Service:", service_settings["service_name"])
    print("Config List:", config_list)
    print("Custom Config List:", custom_config_list)
    print("Service Settings:", service_settings)
    print("Log Settings:", log_config)
    print(
        "Environment API Key:", os.environ.get("OPENAI_API_KEY")
    )  # Verify the API key is set
