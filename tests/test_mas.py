"""The test functions are unit tests for a MultiAgentSystem class.

These are test for its initialization, task processing, error handling,
and output structure.

"""

from unittest.mock import patch

import pytest

from aidi.config import LoadConfig
from aidi.mas import MultiAgentSystem


@pytest.fixture
def setup_config():
    """Fixture to set up necessary configurations."""
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()
    return {
        "config_list": config_list,
        "custom_config_list": custom_config_list,
        "service_settings": service_settings,
        "full_config": full_config,
    }


def test_mas_initialization(setup_config):
    """Test the initialization of the MultiAgentSystem."""
    mas = MultiAgentSystem(
        setup_config["service_settings"], setup_config["full_config"]
    )
    assert mas.service_settings is not None
    assert mas.full_config is not None


def test_mas_create_and_run_valid_task(setup_config):
    """Test that create_and_run successfully processes a valid task."""
    task_input = """
    Translate the following source model:
        {"Category": "CV-CV-Abutment-G-P", "ss_epd_id": "9cf0bb8930ab4d3a"}
    to target schema:
        {"Name_notes": "CV-CV-Abutment-G-P", "Asset_Code": "9cf0bb8930ab4d3a"}
    """
    mas = MultiAgentSystem(
        setup_config["service_settings"], setup_config["full_config"]
    )

    # Mock the actual chat interaction and return a fake result
    with patch("aidi.mas.UserProxyAgent.initiate_chat") as mock_chat:
        mock_chat.return_value = {"response": "success", "task": "completed"}

        result = mas.create_and_run(task_input)
        assert result is not None
        assert "response" in result
        assert result["response"] == "success"


def test_mas_invalid_task_handling(setup_config):
    """Test MAS behavior when provided with invalid input."""
    invalid_task = None  # Simulating an invalid input

    mas = MultiAgentSystem(
        setup_config["service_settings"], setup_config["full_config"]
    )

    with patch("aidi.mas.UserProxyAgent.initiate_chat") as mock_chat:
        mock_chat.side_effect = Exception("Invalid task input")

        with pytest.raises(Exception, match="Invalid task input"):
            mas.create_and_run(invalid_task)


def test_mas_output_structure(setup_config):
    """Test create_and_run for the expected nested output structure."""
    task_input = """
    Translate the following source model:
        {"Category": "CV-CV-Barrier-G-P", "ss_epd_id": "5e99ea4bf1124b66a0899"}
    """

    expected_output = {
        "response": "success",
        "data": {
            "Name_notes": "CV-CV-Barrier-G-P",
            "Asset_Code": "5e99ea4bf1124b66a0899",
        },
    }

    mas = MultiAgentSystem(
        setup_config["service_settings"], setup_config["full_config"]
    )

    with patch("aidi.mas.UserProxyAgent.initiate_chat") as mock_chat:
        mock_chat.return_value = expected_output

        result = mas.create_and_run(task_input)
        assert isinstance(result, dict)
        assert "response" in result
        assert result["response"] == "success"
        assert "data" in result
        assert result["data"]["Name_notes"] == "CV-CV-Barrier-G-P"
