import json


def json_dump(data: dict | list, max_depth=2, curr_depth=1, indent=0):
    indent_str = "  " * indent
    if isinstance(data, dict):
        if not data:
            return "{}"
        if curr_depth >= max_depth:
            return json.dumps(data, separators=(", ", ": "), ensure_ascii=False)
        items = []
        for key, value in data.items():
            value_str = json_dump(value, max_depth, curr_depth + 1, indent + 1)
            items.append(f"{'  ' * (indent + 1)}\"{key}\": {value_str}")
        return "{\n" + ",\n".join(items) + f"\n{indent_str}}}"
    elif isinstance(data, list):
        if not data:
            return "[]"
        if curr_depth >= max_depth:
            return json.dumps(data, separators=(", ", ": "), ensure_ascii=False)
        items = [json_dump(item, max_depth, curr_depth + 1, indent + 1) for item in data]
        return "[\n" + ",\n".join([f"{'  ' * (indent + 1)}{item}" for item in items]) + f"\n{indent_str}]"
    else:
        return json.dumps(data, ensure_ascii=False)
