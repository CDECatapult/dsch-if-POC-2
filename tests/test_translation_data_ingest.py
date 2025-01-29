"""The test functions for  `load_translation_data` class."""

from unittest.mock import MagicMock, patch

import pytest

from aidi.translation_data_ingest import TranslationDataIngest


@pytest.fixture
def mock_translation_data():
    """Fixture to mock the TranslationData class and its methods."""
    with patch(
        "aidi.translation_data_ingest.TranslationData"
    ) as MockTranslationData:  # noqa: N806
        mock_instance = MagicMock()
        mock_instance.generate_llm_prompt.return_value = "Generated Prompt"
        MockTranslationData.from_files.return_value = mock_instance
        yield MockTranslationData


@pytest.fixture
def mock_load_config():
    """Fixture to mock LoadConfig and its configuration."""
    with patch("aidi.translation_data_ingest.LoadConfig") as MockLoadConfig:  # noqa: N806
        mock_config = MagicMock()
        mock_config.get_configuration.return_value = (
            None,  # config_list
            None,  # custom_config_list
            None,  # service_settings
            None,  # log_config
            {
                "data": {"data_folder": "/path/to/data/"},
                "prompt": {
                    "prompt_template": "Template for {sd}, {td}",
                    "prompt_components": ("sd", "td"),
                },
            },
        )
        MockLoadConfig.return_value = mock_config
        yield MockLoadConfig


def test_load_translation_data(mock_translation_data):
    """Test the `load_translation_data` method."""
    data_ingest = TranslationDataIngest(
        data_folder="/path/to/data/",
        prompt_template="Template for {sd}, {td}",
        prompt_components=("sd", "td"),
    )

    prompt, translation_data = data_ingest.load_translation_data()

    # Verify that the prompt was generated
    assert prompt == "Generated Prompt"
