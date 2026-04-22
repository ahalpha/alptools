from ..base_tools import append_unique


def dict_diff(d1_: dict, d2_: dict, log_missing: bool = False) -> tuple[dict, dict]:
    """
    Compare two dictionaries and return their differences.

    Parameters:
    - d1_ (dict): The first dictionary to compare.
    - d2_ (dict): The second dictionary to compare.
    - log_missing (bool, optional): Whether to log missing keys with a placeholder. Defaults to False.

    Returns:
    - tuple[dict, dict]: A tuple containing two dictionaries:
        - The first dictionary contains keys and values from d1_ that differ or are missing in d2_.
        - The second dictionary contains keys and values from d2_ that differ or are missing in d1_.
    """
    diff1 = {}
    diff2 = {}
    for key in append_unique(list(d1_), list(d2_)):
        if key in d1_ and key in d2_:
            if isinstance(d1_[key], dict) and isinstance(d2_[key], dict):
                sub_diff1, sub_diff2 = dict_diff(d1_[key], d2_[key], log_missing)
                if sub_diff1 or sub_diff2:
                    diff1[key] = sub_diff1
                    diff2[key] = sub_diff2

            elif d1_[key] != d2_[key]:
                diff1[key] = d1_[key]
                diff2[key] = d2_[key]

        elif key in d1_:
            diff1[key] = d1_[key]
            if log_missing:
                diff2[key] = "$__missing__"

        elif key in d2_:
            diff2[key] = d2_[key]
            if log_missing:
                diff1[key] = "$__missing__"

    return diff1, diff2


def dict_diff_compact(dict_):
    start_ver = list(dict_.keys())[0]
    diff_compact = {}
    last_ver = None
    for _ver, _data in dict_.items():
        if last_ver == None:
            last_ver = _ver
            diff_compact[_ver] = _data
            continue
        _diff_data, _ = dict_diff(dict_[last_ver], _data)
        last_ver = _ver
        if _diff_data != {}:
            diff_compact[_ver] = _diff_data
    return diff_compact
