def connect_str(str_first, str_join, str_append, *str_more, _ignore=[""]):
    connect_str_cache = ""
    if isinstance(str_append, list):
        connect_str_cache = str_first
        for append_str_cache in str_append:
            connect_str_cache = connect_str(connect_str_cache, str_join, append_str_cache, _ignore)
            del str_append[0]
    else:
        if str_first not in _ignore and str_append not in _ignore:
            connect_str_cache = f"{str_first}{str_join}{str_append}"
        elif str_first not in _ignore:
            connect_str_cache = f"{str_first}"
        elif str_append not in _ignore:
            connect_str_cache = f"{str_append}"
        else:
            connect_str_cache = f""
    if str_more:
        if len(str_more) >= 2:
            connect_str_cache = connect_str(connect_str_cache, *str_more, _ignore=_ignore)
        elif len(str_more) == 1:
            print(f" [WARN] connect_str: ({connect_str_cache}, {str_more[0]}, ...) append args not Double.")
    return connect_str_cache


def connect_str_main(*str_args, _ignore=[""], _igmode="None"):
    if _igmode in ["None", "n"]:
        return connect_str(*str_args, _ignore=_ignore)
    elif _igmode in ["Head", "h"]:
        return connect_str(" ", *str_args, _ignore=_ignore)[1:]
    elif _igmode in ["Tail", "t"]:
        return connect_str(*str_args, " ", _ignore=_ignore)[:-1]
    elif _igmode in ["Head_and_Tail", "ht", "th"]:
        connect_str_main_cache = connect_str_main(*str_args[:-1], _ignore=_ignore, _igmode="Head")
        connect_str_main_cache = connect_str_main(connect_str_main_cache, str_args[-1], _ignore=_ignore, _igmode="Tail")
        return connect_str_main_cache