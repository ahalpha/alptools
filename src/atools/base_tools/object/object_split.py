import math


def object_split(object: dict | list, num: int) -> list:
    """
    Split a dictionary or list into smaller chunks.

    Parameters:
    - object (dict | list): The dictionary or list to be split.
    - num (int): The number of items per chunk for a dictionary, or the number of chunks for a list.

    Returns:
    - list: A list of smaller dictionaries or lists, depending on the input type.
    """
    if isinstance(object, dict):
        keys = list(object.keys())
        return [{k: object[k] for k in keys[i : i + num]} for i in range(0, len(keys), num)]
    if isinstance(object, list):
        n = math.ceil(len(object) / num)
        return [object[i : i + n] for i in range(0, len(object), n)]
    return []
