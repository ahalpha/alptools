import os
import json
from typing import Any, Literal

from ..path.check_dir import check_dir


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return " ".join(f"{byte:02X}" for byte in obj)
        return super().default(obj)


def write_file(file_path: str, content: Any = "", encoding: str = "utf-8", as_json: bool | int | Literal["no-format"] = False, as_bytes: bool = False):
    """
    Writes content to a file with optional JSON formatting or binary mode.

    Parameters:
    - file_path (str): The path to the file to be written.
    - content (any): The content to write to the file. Can be a string, JSON-serializable object, or bytes.
    - encoding (str): The encoding to use when writing text content. Defaults to "utf-8".
    - as_json (bool): If True, serializes the content as JSON before writing.
    - as_bytes (bool): If True, writes the content in binary mode.

    Returns:
    - None
    """
    if os.path.dirname(file_path) != "":
        check_dir(os.path.dirname(file_path), logger_level=3)
    if as_bytes or isinstance(content, bytes) or isinstance(content, bytearray):
        with open(file_path, "wb") as f:
            f.write(content)
        return
    if as_json == 2 or as_json == "no-format":
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(content, f, ensure_ascii=False, cls=BytesEncoder)
        return
    if as_json or isinstance(content, dict) or isinstance(content, list):
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(content, f, ensure_ascii=False, indent=2, separators=(",", ": "), cls=BytesEncoder)
        return
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)
    return
