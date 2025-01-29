"""Module for loading translation data and generating LLM prompts."""

import json
import logging
import os
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel
from rdflib import Graph
from rich import print as print

logger = logging.getLogger(__name__)


class TranslationData(BaseModel):
    """A data model for loadingtranslation data, schemas, and ontologies.

    The `TranslationData` class provides a structured representation of source
    and target data, schemas, and ontologies, along with utilities for loading,
    processing, and generating LLM prompts for translation tasks. It is built
    on Pydantic for robust data validation and type checking.

    Attributes:
    -----------
    source_data : Dict[str, Any]
        The source data to be translated.
    target_data : Dict[str, Any]
        The target data for comparison with the translated source.
    source_data_sample1 : Dict[str, Any]
        A sample of source data for reference in translation.
    target_data_sample1 : Dict[str, Any]
        A corresponding sample of target data for reference.
    source_data_sample2 : Dict[str, Any]
        An additional sample of source data for reference.
    target_data_sample2 : Dict[str, Any]
        An additional sample of target data for reference.
    source_schema : Dict[str, Any]
        The schema definition for the source data.
    target_schema : Dict[str, Any]
        The schema definition for the target data.
    source_ontology_str : str
        The raw RDF Turtle string representation of the source ontology.
    target_ontology_str : str
        The raw RDF Turtle string representation of the target ontology.
    source_ontology_rdf : Graph
        The RDF graph representation of the source ontology.
    target_ontology_rdf : Graph
        The RDF graph representation of the target ontology.

    """

    source_data: Dict[str, Any]
    target_data: Dict[str, Any]
    source_data_sample1: Dict[str, Any]
    target_data_sample1: Dict[str, Any]
    source_data_sample2: Dict[str, Any]
    target_data_sample2: Dict[str, Any]
    source_schema: Dict[str, Any]
    target_schema: Dict[str, Any]
    source_ontology_str: str
    target_ontology_str: str
    source_ontology_rdf: Graph
    target_ontology_rdf: Graph

    class Config:
        """Class for Config."""

        arbitrary_types_allowed = True

    @classmethod
    def from_files(
        cls,
        source_data_path: str,
        target_data_path: str,
        source_data_sample1_path: str,
        target_data_sample1_path: str,
        source_data_sample2_path: str,
        target_data_sample2_path: str,
        source_schema_path: str,
        target_schema_path: str,
        source_ontology_path: str,
        target_ontology_path: str,
    ):
        """Load translation data, schemas, and ontologies.

        from file paths to create a `TranslationData` instance.

        This method reads JSON data files, schema files, and ontology files
        in RDF Turtle format, parses them, and initializes a `TranslationData`
        object with the loaded information. If any file is missing or invalid,
        it logs a warning and uses a default
        empty value.
        """
        logger.info("Loading source and target data from files.")

        # Load data and schema
        source_data = cls.load_json_file(source_data_path)
        target_data = cls.load_json_file(target_data_path)
        source_data_sample1 = cls.load_json_file(source_data_sample1_path)
        target_data_sample1 = cls.load_json_file(target_data_sample1_path)
        source_data_sample2 = cls.load_json_file(source_data_sample2_path)
        target_data_sample2 = cls.load_json_file(target_data_sample2_path)
        source_schema = cls.load_json_file(source_schema_path)
        target_schema = cls.load_json_file(target_schema_path)

        # Load ontologies
        source_ontology_str, source_ontology_rdf = cls.load_ontology_file(
            source_ontology_path
        )
        target_ontology_str, target_ontology_rdf = cls.load_ontology_file(
            target_ontology_path
        )

        return cls(
            source_data=source_data,
            target_data=target_data,
            source_data_sample1=source_data_sample1,
            target_data_sample1=target_data_sample1,
            source_data_sample2=source_data_sample2,
            target_data_sample2=target_data_sample2,
            source_schema=source_schema,
            target_schema=target_schema,
            source_ontology_str=source_ontology_str,
            target_ontology_str=target_ontology_str,
            source_ontology_rdf=source_ontology_rdf,
            target_ontology_rdf=target_ontology_rdf,
        )

    @staticmethod
    def load_json_file(filepath: str) -> Dict[str, Any]:
        """Load JSON file."""
        logger.debug(f"Loading JSON file: {filepath}")
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            # raise FileNotFoundError(f"File not found: {filepath}")
            return {}
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            logger.info(f"Successfully loaded JSON data from {filepath}")
            return data
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in file {filepath}: {e}")
            # raise ValueError(f"Invalid JSON in file {filepath}: {e}")
            return {}

    @staticmethod
    def load_ontology_file(filepath: str) -> Tuple[str, Graph]:
        """Load rdf/ttl ontology file."""
        logger.debug(f"Loading ontology file: {filepath}")
        graph = Graph()
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            # raise FileNotFoundError(f"File not found: {filepath}")
            return "", graph

        try:
            with open(filepath, "r") as f:
                turtle_data = f.read()
            graph.parse(data=turtle_data, format="turtle")
            logger.info(f"Successfully loaded ontology from {filepath}")
            return graph.serialize(format="turtle"), graph
        except Exception as e:
            logger.warning(f"Error parsing RDF ontology file {filepath}: {e}")
            # raise ValueError(f"Error parsing RDF ontology file {filepath}: {e}")  # noqa: E501
            return "", graph

    def generate_llm_prompt(
        self,
        prompt_template: str,
        components: Optional[Tuple[str, ...]] = (
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
    ) -> str:
        """Generates a structured prompt based on specified components.

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
        # Default components to an empty tuple if None
        components = components or ()

        logger.info("Generating LLM prompt with specified inputs.")

        # Query ontology data for relevant mappings (basic query example)
        source_ontology_sample = self.source_ontology_str
        target_ontology_sample = self.target_ontology_str

        # Use Python's format to substitute values
        prompt = prompt_template.format(
            source_data_sample1=self.source_data_sample1
            if "sds1" in components
            else "",
            target_data_sample1=self.target_data_sample1
            if "tds1" in components
            else "",
            source_data_sample2=self.source_data_sample2
            if "sds2" in components
            else "",
            target_data_sample2=self.target_data_sample2
            if "tds2" in components
            else "",
            source_schema=self.source_schema if "ss" in components else "",
            target_schema=self.target_schema if "ts" in components else "",
            source_ontology_sample=source_ontology_sample
            if "so" in components
            else "",
            target_ontology_sample=target_ontology_sample
            if "to" in components
            else "",
            source_data=self.source_data if "sd" in components else "",
            target_data=self.target_data if "td" in components else "",
        )

        logger.debug("Generated LLM prompt successfully.")
        return prompt
