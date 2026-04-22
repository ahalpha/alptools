import os
from ..base_tools import path_join


def clear_empty_dir(base_path, check_self=True):
    del_count = 0
    for root, dirs, files in os.walk(base_path, topdown=False):
        for _dir in dirs:
            _dir = path_join(root, _dir)
            if not os.listdir(_dir):
                os.rmdir(_dir)
                del_count += 1
    if check_self and os.path.isdir(base_path):
        if not os.listdir(base_path):
            os.rmdir(base_path)
            del_count += 1
    return del_count
