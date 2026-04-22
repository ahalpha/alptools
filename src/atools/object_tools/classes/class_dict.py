class ClassDict(dict):
    def __init__(self, *args, **kwargs):

        super(ClassDict, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = ClassDict(value)

    def __getattr__(self, attr):
        if attr not in self:
            self[attr] = ClassDict()
        return self[attr]

    def __setattr__(self, attr, value):
        if isinstance(value, dict) and not isinstance(value, ClassDict):
            value = ClassDict(value)
        self[attr] = value

    def __delattr__(self, attr):
        if attr in self:
            del self[attr]

    def __getitem__(self, key):
        if key not in self:
            self[key] = ClassDict()
        return super(ClassDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, ClassDict):
            value = ClassDict(value)
        super(ClassDict, self).__setitem__(key, value)

    def update(self, _dict=None, **kwargs):
        if _dict is None:
            _dict = {}
        elif isinstance(_dict, dict):
            _dict = _dict.items()
        for key, value in _dict:
            if isinstance(value, dict):
                if key in self and isinstance(self[key], ClassDict):
                    self[key].update(value)
                else:
                    self[key] = ClassDict(value)
            else:
                self[key] = value
        for key, value in kwargs.items():
            if isinstance(value, dict):
                if key in self and isinstance(self[key], ClassDict):
                    self[key].update(value)
                else:
                    self[key] = ClassDict(value)
            else:
                self[key] = value

    def to_dict(self):
        result = {}
        for key, value in self.items():
            if isinstance(value, ClassDict):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
