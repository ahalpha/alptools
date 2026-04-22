import os

from ..__logger import info, warn


def check_dir(dir_path: str, is_filename: bool = False, show_info: bool = True, show_warn: bool = True, logger_level: int = 2) -> int:
    """
    Ensures the existence of a directory, creating it if necessary.

    Parameters:
    - dir_path (str): The directory path to check or create.
    - is_filename (bool): If True, treats `dir_` as a file path and checks its parent directory.

    Returns:
    - int:
        0 if the directory already exists,
        1 if the directory was successfully created,
        2 if the input directory path is empty,
        3 if the directory creation failed.
    """
    if is_filename:
        dir_path = os.path.dirname(dir_path)
    if dir_path == "":
        return -1
    if os.path.isdir(dir_path):
        return 0
    os.makedirs(dir_path, exist_ok=True)
    if os.path.isdir(dir_path):
        if show_info:
            info(f'Auto created the "{dir_path}" folder.', level=logger_level)
        return 1
    else:
        if show_warn:
            warn(f'OSError: Fail to created the "{dir_path}" folder.', level=logger_level)
        return -2
