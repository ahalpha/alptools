import yaml


class ayaml:
    class Dumper(yaml.Dumper):
        pass

    class Loader(yaml.Loader):
        pass

    @staticmethod
    def dump(data, stream=None, sort_keys=False, **params):
        return yaml.dump(data, stream=stream, Dumper=ayaml.Dumper, encoding="utf-8", sort_keys=sort_keys, width=99999, **params)

    @staticmethod
    def load(stream, **params):
        return yaml.load(stream, Loader=ayaml.Loader, **params)


def _represent_bytes(dumper, data):
    hex_str = " ".join(f"{byte:02X}" for byte in data)
    return dumper.represent_scalar("!binary", hex_str)


def _construct_bytes(loader, node):
    value = loader.construct_scalar(node)
    try:
        byte_data = bytes.fromhex(value.replace(" ", ""))
    except ValueError:
        raise yaml.constructor.ConstructorError(None, None, f"Invalid hex byte string: {value}", node.start_mark)
    return byte_data


ayaml.Dumper.add_representer(bytes, _represent_bytes)
ayaml.Loader.add_constructor("!binary", _construct_bytes)
