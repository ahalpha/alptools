import inspect


def info(*message, level=2) -> None:
    """
    Print the current stack trace as a formatted string.

    Returns:
    - None
    """
    frame = inspect.stack()[level]
    print(f" \033[32m[INF]\033[0m", f"\033[35m{frame.code_context[0].split("(")[0].strip()}()\033[0m:", *message)



def warn(*message, level=2) -> None:
    """
    Print the current stack trace as a formatted string.

    Returns:
    - None
    """
    frame = inspect.stack()[level]
    print(f" \033[33m[WRN]\033[0m", f"\033[35m{frame.code_context[0].split("(")[0].strip()}()\033[0m:", *message, f'File \033[35m"{frame.filename}"\033[0m, line \033[35m{frame.lineno}\033[0m')
