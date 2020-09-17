import json


def read_json_dict(pth):
    with open(pth) as f:
        config = json.load(f)
    return config
