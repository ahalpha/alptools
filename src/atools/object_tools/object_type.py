import typing


class Object:
    def __init__(self, data: typing.Optional[dict]=None):
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError("data must be dict")
        annotations = typing.get_type_hints(type(self))
        for key, value in data.items():
            field_type = annotations.get(key)
            if field_type is None:
                continue
            setattr(self, key, self.convert(field_type, value))

    @classmethod
    def convert(cls, field_type, value):
        origin = typing.get_origin(field_type)
        args = typing.get_args(field_type)
        if isinstance(field_type, type) and issubclass(field_type, Object):
            if isinstance(value, dict):
                return field_type(value)
            return value
        if origin is list:
            item_type = args[0] if args else object
            return [cls.convert(item_type, item) for item in value]
        if origin is tuple:
            if len(args) == 2 and args[1] is Ellipsis:
                item_type = args[0]
                return tuple(cls.convert(item_type, item) for item in value)
            return tuple(cls.convert(arg_type, item) for arg_type, item in zip(args, value))
        if origin is dict:
            key_type, value_type = args if len(args) == 2 else (object, object)
            return {cls.convert(key_type, k): cls.convert(value_type, v) for k, v in value.items()}
        return value

    def __iter__(self: "Object"):
        for attr in self.__dict__:
            if attr.startswith("_") or attr in ("raw",):
                continue
            value = getattr(self, attr)
            if value is None:
                continue
            yield attr, Object.default(value)

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, Object):
            return dict(obj)
        elif isinstance(obj, list):
            return [Object.default(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(Object.default(item) for item in obj)
        elif isinstance(obj, dict):
            return {k: Object.default(v) for k, v in obj.items()}
        elif isinstance(obj, typing.Match):
            return repr(obj)
        else:
            return obj

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, ", ".join(f"{attr}={repr(getattr(self, attr))}" for attr in filter(lambda x: not x.startswith("_"), self.__dict__) if getattr(self, attr) is not None))
