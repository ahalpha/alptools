import os
import shutil

from ..__logger import warn


def delete_file(file_path: str, show_warn: bool = True) -> int:
    """
    Deletes a file or directory.

    Parameters:
    - file_path (str): The path to the file or directory to delete.
    - show_warn (bool): If True, prints warnings when the operation fails. Defaults to True.

    Returns:
    - int: Status code indicating the result of the operation.
        0: Success.
        1: File or directory not found.
        2: Permission denied.
        3: Other errors occurred.
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            if show_warn:
                warn(f'FileNotFoundError: Item "{file_path}" not found.')
            return -1
        return 0
    except PermissionError:
        if show_warn:
            warn(f'PermissionError: Permission denied to delete "{file_path}".')
        return -2
    except Exception as e:
        if show_warn:
            warn(f'{e} File "{file_path}".')
        return -3
