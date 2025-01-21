"""Module for comparing target data against inferred data and schemas.

This module provides functions for validating and comparing target data using
several methods, including direct dictionary comparisons, deepdiff, and JSON
schema validation. It also handles the loading and execution of Python scripts
from a specified directory to infer target data. The module supports
configuration loading, data ingestion, and logging to facilitate
the validation workflow.

Functions:
- compare_dicts: Recursively compares two dictionaries and reports differences
or 'VALID' if they match.
- compare_dicts_deepdiff: Compares two dictionaries using the deepdiff library
and reports differences or 'VALID' if they match.
- execute_last_modified_python_file: Executes the last modified Python file in
a specified directory and returns the resulting dictionary.
- validate_target_data: Validates the inferred target data against
actual target data from the translation data ingestion process.
- validate_target_data_deepdiff: Validates the inferred target data using
deepdiff comparison against actual target data.
- validate_data_against_schema: Validates inferred target data against a
specified JSON schema.

Main entry point:
- When run as a module, the module performs a schema validation of
the inferred target data.
"""

from typing import Annotated, Any, Dict, List

from deepdiff import DeepDiff
from jsonschema import ValidationError, validate
from rich import print as print

from aidi.config import LoadConfig
from aidi.translation_data_ingest import TranslationDataIngest
from aidi.utils import execute_last_modified_python_file


def compare_dicts(
    dict1: Annotated[Dict[str, Any], "First dictionary to compare"],
    dict2: Annotated[Dict[str, Any], "Second dictionary to compare"],
    path: Annotated[str, "Current path in dictionary traversal"] = "",
) -> Annotated[List[str], "List of messages indicating comparison results"]:
    """Recursively compare two dictionaries and return a list of differences.

    returns 'VALID' if they match.
    """
    messages = []  # List to collect all messages
    is_valid = True  # Flag to track if any difference is found

    for key in dict1.keys() | dict2.keys():  # Union of keys in both dicts
        new_path = f"{path}.{key}" if path else key

        if key not in dict1:
            messages.append(f"Key '{new_path}' must not be in target data.")
            is_valid = False
        elif key not in dict2:
            messages.append(f"Key '{new_path}' is missing in target data.")
            is_valid = False
        else:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                # Recurse into nested dictionaries and collect results
                nested_messages = compare_dicts(
                    dict1[key], dict2[key], new_path
                )
                messages.extend(nested_messages)
                if nested_messages:
                    is_valid = False
            elif dict1[key] != dict2[key]:
                messages.append(
                    f"Value mismatch at '{new_path}': {dict1[key]} != {dict2[key]}"  # noqa: E501
                )
                is_valid = False

    # Only add a final status message if this is the top-level call
    if path == "":
        if is_valid:
            messages.append("VALID")
        else:
            messages.append("INVALID")

    return messages


def compare_dicts_deepdiff(
    dict1: Annotated[Dict[str, Any], "First dictionary to compare"],
    dict2: Annotated[Dict[str, Any], "Second dictionary to compare"],
    path: Annotated[str, "Current path in dictionary traversal"] = "",
) -> Annotated[List[str], "List of messages indicating comparison results"]:
    """Compare two dictionaries using deepdiff Python library.

    Returns a list of differences, or 'VALID' if they match.
    """
    messages = []  # List to collect all messages
    is_valid = True  # Flag to track if any difference is found

    res = DeepDiff(dict1, dict2, get_deep_distance=False)
    if res == {}:
        pass
    else:
        messages.append(str(res))
        is_valid = False

    # Only add a final status message if this is the top-level call
    if path == "":
        if is_valid:
            messages.append("VALID")
        else:
            messages.append("INVALID")

    return messages


def validate_target_data() -> List[str]:
    """Validate the target data against inferred data from Python file."""
    # load configuration
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()

    # Specify the directory where your Python files are located
    code_directory: str = full_config["code"].get("code_folder")

    # Call the function to execute the last modified Python file
    inferred_dict: Dict[str, Any] = execute_last_modified_python_file(
        code_directory
    )

    print("Actual target dictionary:")

    data_ingest = TranslationDataIngest(
        data_folder=full_config["data"]["data_folder"],
        prompt_components=full_config["prompt"]["prompt_components"],
        prompt_template=full_config["prompt"]["prompt_template"],
    )
    task_prompt, translation_data = data_ingest.load_translation_data()

    actual_target_data_dict: Dict[str, Any] = translation_data.target_data
    print(actual_target_data_dict)

    validation_output = compare_dicts(
        actual_target_data_dict, inferred_dict, path=""
    )
    print(validation_output)

    return validation_output


def validate_target_data_deepdiff() -> List[str]:
    """Validate the target data against inferred data from Python file."""
    # load configuration
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()

    # Specify the directory where your Python files are located
    code_directory: str = full_config["code"].get("code_folder")

    # Call the function to execute the last modified Python file
    inferred_dict: Dict[str, Any] = execute_last_modified_python_file(
        code_directory
    )

    # print("Actual target dictionary:")

    data_ingest = TranslationDataIngest(
        data_folder=full_config["data"]["data_folder"],
        prompt_components=full_config["prompt"]["prompt_components"],
        prompt_template=full_config["prompt"]["prompt_template"],
    )
    task_prompt, translation_data = data_ingest.load_translation_data()

    actual_target_data_dict: Dict[str, Any] = translation_data.target_data
    # print(actual_target_data_dict)

    validation_output = compare_dicts_deepdiff(
        actual_target_data_dict, inferred_dict, path=""
    )

    print(validation_output)

    return validation_output


def validate_data_against_schema() -> List[str]:
    """Validate the inferred target data against target json schema."""
    # load configuration
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()
    # Specify the directory where your Python files are located
    code_directory: str = full_config["code"].get("code_folder")

    # Call the function to execute the last modified Python file
    inferred_data: Dict[str, Any] = execute_last_modified_python_file(
        code_directory
    )

    data_ingest = TranslationDataIngest(
        data_folder=full_config["data"]["data_folder"],
        prompt_components=full_config["prompt"]["prompt_components"],
        prompt_template=full_config["prompt"]["prompt_template"],
    )
    task_prompt, translation_data = data_ingest.load_translation_data()
    print("Actual target schema:")
    target_schema: Dict[str, Any] = translation_data.target_schema
    print(target_schema)

    validation_output = []
    try:
        # Validate the data against the schema
        validate(instance=inferred_data, schema=target_schema)
        validation_output.append(
            "VALID"
        )  # If no error is raised, the data is valid
        print(validation_output)
    except ValidationError as e:
        validation_output.append(
            f"Validation error: {e.message} at {list(e.path)}"
        )
        validation_output.append("INVALID")
        print(validation_output)

    return validation_output


# Execute main if script is run directly (for testing purposes)
if __name__ == "__main__":
    validate_data_against_schema()
