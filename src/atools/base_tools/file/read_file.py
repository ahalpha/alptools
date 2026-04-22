import os
import json
from typing import Any

from ..__logger import warn


def read_file(file_path: str, encoding: str = "utf-8", with_json: bool = False, with_bytes: bool = False, default: Any = None, show_warn: bool = True):
    """
    Reads the content of a file with optional JSON parsing or byte reading.

    Parameters:
    - file_path (str): The path to the file to be read.
    - with_json (bool): If True, attempts to parse the file content as JSON.
    - with_bytes (bool): If True, reads the file in binary mode.
    - default (any): The default value to return if the file does not exist or an error occurs.
    - show_warn (bool): If True, prints a warning message when the file is not found or cannot be read.

    Returns:
    - any: The content of the file, parsed JSON object, or the default `default` value.
    """
    if not os.path.exists(file_path):
        if show_warn:
            warn(f'FileNotFoundError: File "{file_path}" not found.')
        return default
    if with_bytes:
        with open(file_path, "rb") as f:
            return f.read()
    with open(file_path, "r", encoding=encoding) as f:
        if with_json:
            try:
                return json.load(f)
            except Exception as e:
                if show_warn:
                    warn(f'JSONDecodeError: File "{file_path}" is not a valid JSON file ({e}).')
                return default
        return f.read()
