import re, json, os, copy, traceback


def read_jsonl_file(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def save_to_jsonl_file(data, filename):
    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name): os.makedirs(dir_name)

    with open(filename, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

