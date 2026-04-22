import os
import shutil

from ..__logger import warn
from ..path.check_dir import check_dir


def copy_file(bfile: str, afile: str, show_warn: bool = True) -> int:
    """
    Copies a file or directory from one location to another.

    Parameters:
    - bfile (str): The source file or directory path to copy.
    - afile (str): The destination file or directory path.
    - show_warn (bool): If True, prints warnings when the operation fails. Defaults to True.

    Returns:
    - int: Status code indicating the result of the operation.
        0: Success.
        1: Source file or directory not found.
        2: Permission denied.
        3: Other errors occurred.
    """
    try:
        if os.path.isfile(bfile):
            check_dir(afile, is_filename=True, logger_level=3)
            shutil.copy(bfile, afile)
        elif os.path.isdir(bfile):
            check_dir(afile, logger_level=3)
            shutil.copytree(bfile, afile, dirs_exist_ok=True)
        else:
            if show_warn:
                warn(f'FileNotFoundError: Item "{bfile}" not found.')
            return -1
        return 0
    except PermissionError:
        if show_warn:
            warn(f'PermissionError: Permission denied to copy "{bfile}".')
        return -2
    except Exception as e:
        if show_warn:
            warn(f'{e} "{bfile}".')
        return -3
