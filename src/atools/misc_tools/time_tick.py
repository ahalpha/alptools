import time

TIME_TICK_CACHE = {}


def time_tick(_name, _time=3, _reset=True):
    if time.time() <= TIME_TICK_CACHE.get(_name, 0):
        if _reset:
            TIME_TICK_CACHE[_name] = 0
        return True
    else:
        TIME_TICK_CACHE[_name] = time.time() + _time
        return False
