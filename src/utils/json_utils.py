import json, re, os


def flatten_json(nested_json, parent_key='', sep='_'):
    """\n    Flatten a nested JSON object\n    """
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            value_c = sorted(value)
            for i, v in enumerate(value_c):
                new_item = flatten_json(v, f"{new_key}{sep}{i}", sep=sep)
                items.extend(new_item.items())
        else:
            items.append((new_key, value))
    return dict(items)


def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_json_file(data, filename, encoding="utf-8"):
    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name): os.makedirs(dir_name)

    with open(filename, "w", encoding=encoding) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)