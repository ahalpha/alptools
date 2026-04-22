from typing import Any


def object_get(base_object: dict | list, pos: str | tuple | list, default: Any = None) -> Any:
    """
    Retrieve a value from a nested dictionary or list using a key or sequence of keys.

    Parameters:
    - base_object (dict | list): The dictionary or list to retrieve the value from.
    - pos (str | tuple | list): The key or sequence of keys to locate the value.
    - default (any, optional): The default value to return if the key is not found. Defaults to None.

    Returns:
    - any: The value found at the specified position, or the default value if not found.
    """
    if isinstance(pos, str):
        pos = (pos,)
    _value = base_object
    for _key in pos:
        if (isinstance(_value, dict) and _key in _value) or (isinstance(_value, (list, tuple)) and _key < len(_value)):
            _value = _value[_key]
        else:
            return default
    return _value
