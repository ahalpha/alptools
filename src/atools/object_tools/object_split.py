import math
from typing import TypeVar, overload

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


@overload
def object_split(obj: dict[K, V], size: int | None = None, num: int | None = None) -> list[dict[K, V]]: ...


@overload
def object_split(obj: list[T], size: int | None = None, num: int | None = None) -> list[list[T]]: ...


def object_split(object: dict[K, V] | list[T], size: int = None, num: int = None) -> list[dict[K, V]] | list[list[T]]:
    """
    Split a dictionary or list into smaller chunks while preserving order.

    Parameters:
    - obj (dict | list): The dictionary or list to be split.
    - size (int | None): The maximum number of items per chunk. Must be a positive
      integer. Required if num is not provided.
    - num (int | None): The target number of chunks. Must be a positive integer.
      If provided, overrides size with ceil(len(obj) / num). The actual number
      of chunks may be smaller than num. No empty chunks are added.

    Returns:
    - list[dict[K, V]] | list[list[T]]: A list of dictionaries if the input is a
      dictionary, or a list of lists if the input is a list. Key, value, and
      element types are preserved. Returns an empty list for empty input
      when the arguments are valid. Chunks are shallow copies.

    """
    if num is not None:
        size = math.ceil(len(object) / num)
    if isinstance(object, dict):
        keys = list(object.keys())
        return [{k: object[k] for k in keys[i : i + size]} for i in range(0, len(keys), size)]
    if isinstance(object, list):
        return [object[i : i + size] for i in range(0, len(object), size)]
    return []
