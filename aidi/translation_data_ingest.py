"""Module for managing translation data ingestion and LLM prompt generation."""

import logging
from typing import Optional, Tuple

from rich import print as print

from aidi.config import LoadConfig
from aidi.translationdata import TranslationData

logger = logging.getLogger(__name__)


class TranslationDataIngest:
    """Class for data Ingestion.

    Class to manage the loading and validation of translation data, schema,
    and ontology from specified files.

    Also generates LLM prompt based on
    prompt components with the following acronyms:
    "sd": source data
    "td": target data
    "sds1": source data sample 1
    "tds1": target data sample 1
    "sds2": source data sample 2
    "tds2": target data sample 2
    "ss": source schema
    "ts": target schema
    "so": source ontology
    "to": target ontology
    """

    def __init__(  # noqa: D417
        self,
        data_folder: str,
        prompt_template: str,
        prompt_components: Optional[Tuple[str, ...]] = (
            "sd",
            "td",
            "sds1",
            "tds1",
            "sds2",
            "tds2",
            "ss",
            "ts",
            "so",
            "to",
        ),
    ):
        """TranslationDataIngest Init.

        Args:
            data_folder (str): _description_
            prompt_template (str): _description_
            prompt_components (Optional[Tuple[str, ...]], optional):
            _description_.
            Defaults to ( "sd", "td", "sds1", "tds1", "sds2", "tds2",
            "ss", "ts", "so", "to", ).
        """
        self.data_folder = data_folder
        self.prompt_components = prompt_components
        self.prompt_template = prompt_template

    def load_translation_data(self) -> Tuple[str, TranslationData]:
        """Loads data, schema, and ontology from source files after validation.

        Generates an LLM prompt afterwards.

        Returns:
            Optional[Tuple[str, TranslationData]]: A tuple with the generated
            prompt and TranslationData instance if successful,else None.
        """
        # Define file paths for source and target data, schemas, and ontologies
        source_data_path = self.data_folder + "source_data.json"
        target_data_path = self.data_folder + "target_data.json"
        source_data_sample1_path = (
            self.data_folder + "source_data_sample1.json"
        )
        target_data_sample1_path = (
            self.data_folder + "target_data_sample1.json"
        )
        source_data_sample2_path = (
            self.data_folder + "source_data_sample2.json"
        )
        target_data_sample2_path = (
            self.data_folder + "target_data_sample2.json"
        )
        source_schema_path = self.data_folder + "source_schema.json"
        target_schema_path = self.data_folder + "target_schema.json"
        source_ontology_path = self.data_folder + "source_ontology.ttl"
        target_ontology_path = self.data_folder + "target_ontology.ttl"

        logger.info(
            "Creating and validating translation data from source files."
        )

        # Initialize TranslationData using the from_files factory method
        translation_data = TranslationData.from_files(
            source_data_path,
            target_data_path,
            source_data_sample1_path,
            target_data_sample1_path,
            source_data_sample2_path,
            target_data_sample2_path,
            source_schema_path,
            target_schema_path,
            source_ontology_path,
            target_ontology_path,
        )

        # Generate and return the prompt,
        # specifying which components to include
        logger.info("Generating prompt from translation data.")
        prompt = translation_data.generate_llm_prompt(
            prompt_template=self.prompt_template,
            components=self.prompt_components,
        )
        logger.info("Prompt generated successfully.")
        return prompt, translation_data


# Execute main if script is run directly for testing purposes
if __name__ == "__main__":
    # load configuration
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()

    data_ingest = TranslationDataIngest(
        data_folder=full_config["data"].get("data_folder"),
        prompt_components=full_config["prompt"].get("prompt_components"),
        prompt_template=full_config["prompt"].get("prompt_template"),
    )
    task_prompt, translation_data = data_ingest.load_translation_data()

    print(task_prompt)
