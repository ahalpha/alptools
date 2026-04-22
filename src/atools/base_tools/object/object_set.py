from typing import List, Tuple, Any, Union, Literal

from ..__logger import warn


def object_set(
    base_object: dict,
    pos: Union[str, List[str], Tuple[str, ...]],
    value: Any = None,
    target_type: Literal["default", "str", "number", "list", "dict"] = "default",
    unique: bool = False,
) -> dict:
    """
    A function to set or update a value in a dictionary, supporting nested keys and various data types.

    Parameters:
    - object (dict): The dictionary to modify.
    - pos (str | list | tuple): The key or nested keys where the value should be set.
    - value (Any, optional): The value to set or update. Defaults to None.
    - target_type (str, optional): The type of operation to perform. Options include:
        - "default" or None: Directly set the value.
        - "str" or "": Concatenate the value to an existing string.
        - "number" or 0: Add the value to an existing number.
        - "list" or []: Append the value to a list, optionally ensuring uniqueness.
        - "dict" or {}: Update the value as a dictionary.
    - unique (bool, optional): If True, ensures the value is unique when appending to a list. Defaults to False.

    Returns:
    - dict: The updated dictionary.
    """
    # Handle nested keys if `pos` is a tuple or list
    if isinstance(pos, (list, tuple)):
        if len(pos) == 0:
            warn(f"Empty dict name received: {pos}.")
            return base_object
        elif len(pos) == 1:
            pos = pos[0]
        else:
            curr_key, pos = pos[0], pos[1:]
            if curr_key not in base_object or not isinstance(base_object[curr_key], dict):
                base_object[curr_key] = {}
            object_set(base_object[curr_key], pos, value, target_type, unique)
            return base_object

    # Create or update the value based on the `target_type` parameter
    if target_type in ("default", None):
        base_object[pos] = value
    elif target_type in ("str", ""):
        if pos not in base_object:  # Init
            base_object[pos] = ""
        if value is not None:
            base_object[pos] += value
    elif target_type in ("number", 0):
        if pos not in base_object:  # Init
            base_object[pos] = 0
        if value is not None:
            base_object[pos] += value
    elif target_type in ("list", []):
        if pos not in base_object:  # Init
            base_object[pos] = []
        if value is not None and (not unique or value not in base_object[pos]):
            base_object[pos].append(value)
    elif target_type in ("dict", {}):
        if pos not in base_object:  # Init
            base_object[pos] = {}
        if value is not None:
            base_object[pos].update(value)
    else:
        warn(f"Unknown type provided: {target_type}.")
    return base_object
