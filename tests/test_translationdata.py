"""The module defines pytest test functions for a TranslationData class.

TranslationData loads data from mock files and tests methods for
generating prompts.
"""

import pytest
from rdflib import Graph

from aidi.translationdata import TranslationData


@pytest.fixture
def mock_files(tmp_path):
    """Fixture to create mock data, schema, and ontology files."""
    # JSON Files
    json_content = '{"key": "value"}'
    sample1_content = '{"sample1": "data"}'
    schema_content = '{"schema": "definition"}'

    # RDF Turtle Ontology Files
    ontology_content = """
        @prefix ex: <http://example.org/> .
        ex:subject ex:predicate ex:object .
    """

    # Create files
    files = {
        "source_data.json": json_content,
        "target_data.json": json_content,
        "source_data_sample1.json": sample1_content,
        "target_data_sample1.json": sample1_content,
        "source_data_sample2.json": sample1_content,
        "target_data_sample2.json": sample1_content,
        "source_schema.json": schema_content,
        "target_schema.json": schema_content,
        "source_ontology.ttl": ontology_content,
        "target_ontology.ttl": ontology_content,
    }

    file_paths = {}
    for name, content in files.items():
        file_path = tmp_path / name
        file_path.write_text(content)
        file_paths[name] = str(file_path)

    return file_paths


def test_from_files(mock_files):
    """Test the from_files method of TranslationData."""
    # Load TranslationData using from_files
    data = TranslationData.from_files(
        source_data_path=mock_files["source_data.json"],
        target_data_path=mock_files["target_data.json"],
        source_data_sample1_path=mock_files["source_data_sample1.json"],
        target_data_sample1_path=mock_files["target_data_sample1.json"],
        source_data_sample2_path=mock_files["source_data_sample2.json"],
        target_data_sample2_path=mock_files["target_data_sample2.json"],
        source_schema_path=mock_files["source_schema.json"],
        target_schema_path=mock_files["target_schema.json"],
        source_ontology_path=mock_files["source_ontology.ttl"],
        target_ontology_path=mock_files["target_ontology.ttl"],
    )

    # Assertions to validate loaded data
    assert data.source_data == {"key": "value"}
    assert data.target_data == {"key": "value"}
    assert data.source_schema == {"schema": "definition"}
    assert isinstance(data.source_ontology_rdf, Graph)
    assert isinstance(data.target_ontology_rdf, Graph)
    assert "predicate" in data.source_ontology_str
    assert "predicate" in data.target_ontology_str


def test_generate_llm_prompt(mock_files):
    """Test the generate_llm_prompt method of TranslationData."""
    # Load data from mock files
    data = TranslationData.from_files(
        source_data_path=mock_files["source_data.json"],
        target_data_path=mock_files["target_data.json"],
        source_data_sample1_path=mock_files["source_data_sample1.json"],
        target_data_sample1_path=mock_files["target_data_sample1.json"],
        source_data_sample2_path=mock_files["source_data_sample2.json"],
        target_data_sample2_path=mock_files["target_data_sample2.json"],
        source_schema_path=mock_files["source_schema.json"],
        target_schema_path=mock_files["target_schema.json"],
        source_ontology_path=mock_files["source_ontology.ttl"],
        target_ontology_path=mock_files["target_ontology.ttl"],
    )

    # Define a template and components
    template = (
        "Source: {source_data}, Target: {target_data}, Schema: {source_schema}"
    )
    components = ("sd", "td", "ss")

    # Generate prompt
    prompt = data.generate_llm_prompt(template, components)

    # Assertions
    assert "Source: {'key': 'value'}" in prompt
    assert "Target: {'key': 'value'}" in prompt
    assert "Schema: {'schema': 'definition'}" in prompt
