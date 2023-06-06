import json


def reader(path):
    with open(path, encoding='utf-8') as handler:
        return json.load(handler)

