from typing import Any, List, Callable, TypeVar, Optional


Object = TypeVar("Object")


def object_filter(lst: List[Object], filter_func: Callable[[Object], bool]) -> List[Object]:
    return list(filter(filter_func, lst))


def object_find(lst: List[Object], filter_func: Callable[[Object], bool]) -> Optional[Object]:
    return next(filter(filter_func, lst), None)
