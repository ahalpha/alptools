from typing import Any, Optional, Callable


def append_unique(target_list: list, value: Any, filter_func: Optional[Callable[[Any], bool]] = None, mapper_func: Optional[Callable[[Any], Any]] = None) -> list:
    """
    Append an item to a list if it is unique, with optional filtering and mapping.

    Parameters:
    - target_list (list): The list to which the item will be appended.
    - value (Any): The item to append. Can be a single item or an iterable (list, tuple, set, or dict).
    - filter_func (Callable[[Any], bool], optional): A function to filter items. Only items passing the filter will be appended.
    - mapper_func (Callable[[Any], Any], optional): A function to transform the item before appending.

    Returns:
    - list: The updated list with the unique item(s) appended.
    """
    if isinstance(value, (list, tuple, set, dict)):
        for item in value:
            append_unique(target_list, item, filter_func, mapper_func)
    else:
        item = mapper_func(value) if mapper_func else value
        if item not in target_list:
            if not filter_func or filter_func(item):
                target_list.append(item)
    return target_list
