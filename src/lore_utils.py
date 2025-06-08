# src/lore_utils.py

import yaml
from pathlib import Path
from typing import Any, Dict

def _load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """
    Loads and parses a YAML file, ensuring the content is a dictionary.

    Args:
        file_path: The path to the YAML file.

    Returns:
        A dictionary representing the YAML content.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If the file content is not valid YAML.
        TypeError: If the parsed YAML content is not a dictionary.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if not isinstance(data, dict):
            raise TypeError(f"YAML content in '{file_path}' is not a dictionary. Found type: {type(data)}")
        return data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML from {file_path}: {e}")

def get_lore_markdown(file_path: Path) -> str:
    """
    Extracts the 'converted_lore' (Markdown string) from the LLM's YAML response file.

    Args:
        file_path: The path to the YAML file containing the LLM's response
                   from the 'extract-lore' step.

    Returns:
        The Markdown string content of the 'converted_lore' section.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If the file content is not valid YAML.
        KeyError: If the 'converted_lore' key is not found in the YAML.
    """
    data = _load_yaml_file(file_path)
    try:
        return data['converted_lore']
    except KeyError:
        raise KeyError(f"Key 'converted_lore' not found in YAML from {file_path}. "
                       "Ensure the LLM response contains this section.")

def get_adversary_renaming_table_markdown(file_path: Path) -> str:
    """
    Extracts the 'renaming_table' data from the LLM's YAML response file
    and formats it into a Markdown table string suitable for Jinja.
    Each dictionary in the table is expected to contain 'original_name', 'sots_name', and 'level'.

    Args:
        file_path: The path to the YAML file containing the LLM's response
                   from the 'extract-lore' step.

    Returns:
        A Markdown table string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If the file content is not valid YAML.
        KeyError: If the 'renaming_table' key is not found in the YAML.
        TypeError: If 'renaming_table' is not a list.
    """
    data = _load_yaml_file(file_path)
    try:
        renaming_data = data['renaming_table']
        if not isinstance(renaming_data, list):
            raise TypeError(f"Expected 'renaming_table' to be a list, but found {type(renaming_data)} in {file_path}.")
    except KeyError:
        raise KeyError(f"Key 'renaming_table' not found in YAML from {file_path}. "
                       "Ensure the LLM response contains this section.")

    if not renaming_data:
        # Return empty table header if no data, matching the expected format
        return "| Original Name | Revised Name | Type |\n|---|---|---|\n"

    # Define headers explicitly
    headers = ["Original Name", "Revised Name", "Type"]
    header_line = "| " + " | ".join(headers) + " |\n"
    separator_line = "|---" * len(headers) + "|\n"

    rows = []
    for entry in renaming_data:
        # Using .get() with default empty string for robustness in case a key is missing
        original_name = entry.get('original_name', '')
        sots_name = entry.get('sots_name', '')
        # Map 'level' from LLM output to 'Type' for the Markdown table
        entity_type = entry.get('level', '')

        row_cells = [original_name, sots_name, entity_type]
        rows.append("| " + " | ".join(row_cells) + " |")

    return header_line + separator_line + "\n".join(rows)