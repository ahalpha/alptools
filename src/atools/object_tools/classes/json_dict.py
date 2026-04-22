import os
from itertools import islice
from contextlib import contextmanager


from ...base_tools import read_file, write_file


class JsonDict:
    def __init__(self, on_update=None):
        self.data = {}
        self.index = self.data
        self.on_update = on_update
        self._ipos = []

    def __setitem__(self, pos: str | int | list | tuple, value: any):
        if isinstance(pos, str) or isinstance(pos, int):
            self.index[pos] = value
            return
        if pos == ():
            if isinstance(self.index, list):
                self.index.append(value)
            else:
                raise TypeError("() cannot be used for non-list index")
            return
        obj = self.index
        for key in islice(pos, 0, len(pos) - 1):
            if isinstance(obj, dict):
                if key == ():
                    raise TypeError("() cannot be used for non-list index")
                elif key in obj:
                    obj = obj[key]
                else:
                    obj[key] = {}
                    obj = obj[key]
            elif isinstance(obj, list):
                if key == ():
                    obj.append({})
                    obj = obj[-1]
                elif key < len(obj):
                    obj = obj[key]
                else:
                    raise IndexError("list index out of range")
            else:
                raise TypeError()
        obj[pos[-1]] = value
        return

    def __getitem__(self, pos):
        if isinstance(pos, str):
            return self.index[pos]
        value = self.index
        for key in pos:
            value = value[key]
        return value

    def get(self, pos, default=None):
        if isinstance(pos, str):
            return self.index[pos] if (isinstance(self.index, dict) and pos in self.index) or (isinstance(self.index, (list, tuple)) and pos < len(self.index)) else default
        value = self.index
        for key in pos:
            if (isinstance(value, dict) and key in value) or (isinstance(value, (list, tuple)) and key < len(value)):
                value = value[key]
            else:
                return default
        return value

    def __str__(self):
        return str(self.index)

    def __update__(self, data):
        self.index.update(data)
        if self.on_update:
            self.on_update(self.index)
        return

    def __delitem__(self, pos):
        if isinstance(pos, str) or isinstance(pos, int):
            if pos in self.index:
                del self.index[pos]
            return
        obj = self.index
        for key in islice(pos, 0, len(pos) - 1):
            if isinstance(obj, dict):
                if key in obj:
                    obj = obj[key]
                else:
                    return
            elif isinstance(obj, list):
                if key < len(obj):
                    obj = obj[key]
                else:
                    raise IndexError("list index out of range")
            else:
                raise TypeError()
        if (isinstance(self.index, dict) and pos in self.index) or (isinstance(self.index, (list, tuple)) and pos < len(self.index)):
            del obj[pos[-1]]
        return

    def pos(self, *pos):
        if not len(pos) or pos[0] not in [".", ".."]:
            self._ipos = []

        for _p_ in pos:
            if _p_ == ".":
                continue
            elif _p_ == "..":
                if len(self._ipos):
                    del self._ipos[-1]
            else:
                self._ipos.append(_p_)

        self.index = self.data
        for key in self._ipos:
            if isinstance(self.index, dict):
                if key == ():
                    raise TypeError("() cannot be used for non-list index")
                elif key in self.index:
                    self.index = self.index[key]
                else:
                    self.index[key] = {}
                    self.index = self.index[key]
            elif isinstance(self.index, list):
                if key == ():
                    self.index.append({})
                    self.index = self.index[-1]
                elif key < len(self.index):
                    self.index = self.index[key]
                else:
                    raise IndexError("list index out of range")
            else:
                raise TypeError()
        return

    @contextmanager
    def pos_to(self, *pos_):
        _prev_index, _prev_ipos = self.index, self._ipos[:]
        self.pos(".", *pos_)
        try:
            yield self
        finally:
            self.index, self._ipos = _prev_index, _prev_ipos


class FileDict(JsonDict):
    def __init__(self, file, init=None):
        super(FileDict, self).__init__(on_update=lambda data: write_file(self.file, data, as_json=True))
        self.file = file
        if os.path.exists(file):
            self.data = read_file(file, with_json=True)
        else:
            self.data = init if init else {}
            write_file(file, self.data, as_json=True)
