"""Module that provides utilities for executing and processing Python scripts.

This module includes functions for identifying and executing the last modified
Python file in a specified directory, processing its output, and managing the
resulting data.

Functions:
- execute_last_modified_python_file(directory: str): Identifies the last
modified Python file in a given directory, executes it, and returns the
inferred dictionary.
- rename_last_modified_python_file(directory: str): Renames the last modified
Python file in the specified directory to 'program_generated_by_AI.py'.
- get_generated_data(directory: str): Executes the last modified Python file,
saves its output as a JSON file.

Main Entry Point:
- When run as a standalone script, this module loads configuration settings,
executes the last modified Python file in the specified directory, saves the
inferred dictionary to a JSON file, and prints it with syntax highlighting.
"""

import ast
import json
import os
import subprocess
from typing import Any, Dict

from rich import print as print
from rich.syntax import Syntax

from aidi.config import LoadConfig


def execute_last_modified_python_file(directory: str):
    """Executes the last modifief Python File.

    Identify the last modified Python file in the given directory,
    execute it, and return the dictionary.
    """
    # Find the last modified Python file
    python_files = [
        f for f in os.listdir(directory) if not f.endswith(".json")
    ]
    # python_files = [f for f in os.listdir(directory)]
    if not python_files:
        raise FileNotFoundError("No Python files found in the directory.")

    # Get the full path and sort by modification time
    full_paths = [os.path.join(directory, f) for f in python_files]
    last_modified_file = max(full_paths, key=os.path.getmtime)
    print(f"Last modified file: {last_modified_file}")

    # Execute the Python file and capture output
    result = subprocess.run(
        ["python", last_modified_file], capture_output=True, text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Error executing {last_modified_file}: {result.stderr}"
        )

    # Assuming the output is a valid dictionary representation
    output = result.stdout.strip()

    # Convert the output string to a dictionary
    result_dict = ast.literal_eval(output)

    # print("Inferred Target Data:")
    # print(result_dict)
    return result_dict


def rename_last_modified_python_file(directory: str):
    """Rename the last modified Python file in the given directory.

    to 'program_generated_by_AI.py'.
    """
    # Find all Python files in the directory
    python_files = [
        f for f in os.listdir(directory) if not f.endswith(".json")
    ]
    if not python_files:
        raise FileNotFoundError("No Python files found in the directory.")

    # Get the full path of files and find the last modified file
    full_paths = [os.path.join(directory, f) for f in python_files]
    last_modified_file = max(full_paths, key=os.path.getmtime)

    # Define the new file path
    new_file_path = os.path.join(directory, "program_generated_by_AI.py")

    # Rename the file
    os.rename(last_modified_file, new_file_path)
    # print(f"Renamed '{last_modified_file}' to '{new_file_path}'")

    return new_file_path


def get_generated_data(directory: str):
    """Get generated data.

    Execute the data translation program and save the generated json data model
    to a file.
    """
    code_directory = directory

    # Call the function to execute the last modified Python file
    inferred_data: Dict[str, Any] = execute_last_modified_python_file(
        code_directory
    )
    # print(inferred_data)

    # Save the dictionary as a JSON file
    with open(code_directory + "generated_target_data.json", "w") as file:
        json.dump(inferred_data, file, indent=4)

    # Convert the dictionary to a JSON string
    infererd_data_json = json.dumps(inferred_data, indent=4)

    syntax = Syntax(
        infererd_data_json, "json", theme="monokai", line_numbers=False
    )
    print(syntax)


# Execute main if script is run directly
if __name__ == "__main__":
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
    # print(inferred_data)

    # Save the dictionary as a JSON file
    with open(code_directory + "generated_target_data.json", "w") as file:
        json.dump(inferred_data, file, indent=4)

    # Convert the dictionary to a JSON string
    infererd_data_json = json.dumps(inferred_data, indent=4)

    syntax = Syntax(
        infererd_data_json, "json", theme="monokai", line_numbers=False
    )
    print(syntax)
