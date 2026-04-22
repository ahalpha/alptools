import unicodedata


def is_number(str_: str) -> bool:
    """
    Check if a string represents a number.

    Args:
    - str_ (str): The input string to check.

    Returns:
    - bool: True if the string represents a number, False otherwise.
    """
    try:
        float(str_) or unicodedata.numeric(str_)
        return True
    except (ValueError, TypeError):
        return False
