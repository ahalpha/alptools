import os

MAIN_PATH = os.getcwd().split("\\")



def path_join(*pos: str, auto_path: bool = True) -> str:

    """
    Joins multiple path components into a single path string.

    Parameters:
    - pos (str): One or more path components to join.
    - auto_path (bool): If True, prepends the MAIN_PATH to the resulting path.

    Returns:
    - str: The joined path as a string.
    """
    return_path = []
    for _i, _p in enumerate(pos):
        _p = _p.replace("\\", "/").split("/")
        if len(_p[0]) == 2 and _p[0][1] == ":":
            return_path.clear()
        elif _i == 0 and auto_path:
            return_path = list(MAIN_PATH)
        for _x_ in _p:
            if _x_ in ".":
                continue
            elif _x_ == "..":
                return_path.pop()
            elif _x_ != "":
                return_path.append(_x_)
    return "/".join(return_path)