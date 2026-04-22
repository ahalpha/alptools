import re


def str_add_num(str_: str, sep_: str = "_", fill_: int = 0, start_: int = 1) -> str:
    """
    Increment the numeric suffix of a string, or add one if it doesn't exist.

    Args:
    - base_string (str): The input string to modify.
    - sep_ (str): The separator between the string and the number. Default is "_".
    - fill_ (int): The zero-padding width for the number. Default is 0 (no padding).
    - start_ (int): The starting number to append if no numeric suffix exists. Default is 1.

    Returns:
    - str: The modified string with an incremented or newly added numeric suffix.
    """
    match = re.search(rf"{sep_}(\d+)$", str_)
    if match:
        str_ = re.sub(rf"{sep_}\d+$", f"{sep_}{(int(match.group(1)) + 1):0{fill_}}", str_)
    else:
        str_ = f"{str_}{sep_}{start_}"
    return str_
