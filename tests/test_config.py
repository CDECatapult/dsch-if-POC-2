"""The module defines pytest test functions for congig.py.

Used to validate loading, retrieving, setting environment variables, and
testing the main functionality of a configuration loader module.

"""

import os

import pytest
import yaml

from aidi.config import LoadConfig  # Replace with the actual module name

# Fixture for a temporary YAML configuration file


@pytest.fixture
def temp_config_file(tmp_path):
    """This function creates a temporary YAML configuration file.

    with specific data for testing purposes.

    Args:
        tmp_path: `tmp_path` is a fixture provided by pytest that represents
        a temporary directory path.
        This fixture is used to create temporary files or directories during
        testing to isolate the test environment and ensure reproducibility.

    Returns:
        The fixture `temp_config_file` is returning the path to a temporary
        YAML configuration file that has been created with the specified
        configuration data.
    """
    config_data = {
        "logging": {
            "level": "INFO",
            "log_file_name": "./translation_log.log",
        },
        "data": {
            "data_folder": "./data/data1/",
        },
        "code": {
            "code_folder": str(tmp_path / "translation_folder"),
        },
        "active_service": "OpenAI",
        "services": {
            "OpenAI": {
                "service_name": "OpenAI",
                "model": "gpt-4o-2024-08-06",
                "embedding": "text-embedding-3-small",
                "api_key": "test_api_key",
                "selected_model": "gpt-4o-2024-08-06",
                "config_list": [
                    {
                        "model": "gpt-4o-2024-08-06",
                        "api_key": "test_api_key",
                    }
                ],
                "custom_config_list": [
                    {
                        "model": "custom_llm_json",
                        "model_client_cls": "CustomLLMClient",
                    }
                ],
            },
            "ollama": {
                "service_name": "ollama",
                "base_url": "http://52.56.167.144:11434/",
                "model": "mistral-nemo",
                "selected_model": "mistral-nemo",
                "embedding": "all-minilm",
                "config_list": [
                    {
                        "model": "mistral-nemo",
                        "base_url": "http://52.56.167.144:11434/v1/",
                        "api_type": "open_ai",
                        "api_key": "ollama",
                        "price": [0, 0],
                    }
                ],
                "custom_config_list": [
                    {
                        "model": "custom_llm_json",
                        "model_client_cls": "CustomLLMClient",
                    }
                ],
            },
        },
        "prompt": {
            "prompt_components": ["sd", "ts"],
            "prompt_template": "Translate source data to target data...",
        },
        "group_chat": {
            "messages": [],
            "max_round": 50,
            "send_introductions": False,
            "cache_chat": False,
            "structured_output": True,
            "validation_by_tool": True,
        },
    }
    config_file = tmp_path / "config_aidi.yaml"
    with open(config_file, "w") as file:
        yaml.dump(config_data, file)
    return config_file


def test_load_yaml_config(temp_config_file):
    """Test if the YAML configuration is loaded correctly."""
    config = LoadConfig.load_yaml_config(str(temp_config_file))
    assert config["active_service"] == "OpenAI"
    assert config["logging"]["level"] == "INFO"
    assert config["services"]["OpenAI"]["model"] == "gpt-4o-2024-08-06"


def test_get_service_config(temp_config_file):
    """Test if the correct service configuration is retrieved."""
    loader = LoadConfig(str(temp_config_file))
    service_config = loader._get_service_config()
    assert service_config["service_name"] == "OpenAI"
    assert service_config["api_key"] == "test_api_key"


def test_set_environment_variables(temp_config_file):
    """Test if environment variables are set correctly."""
    LoadConfig(str(temp_config_file))
    assert os.environ.get("OPENAI_API_KEY") == "test_api_key"


def test_main_functionality(temp_config_file, capsys):
    """Test the functionality of the __main__ section."""
    loader = LoadConfig(str(temp_config_file))
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = loader.get_configuration()

    assert service_settings["service_name"] == "OpenAI"
    assert len(config_list) == 1
    assert config_list[0]["model"] == "gpt-4o-2024-08-06"
    assert len(custom_config_list) == 1
    assert custom_config_list[0]["model"] == "custom_llm_json"
    assert log_config["level"] == "INFO"

    # Verify the code folder creation
    code_folder = full_config["code"]["code_folder"]
    assert os.path.exists(code_folder)
