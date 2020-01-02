import json
import os
from pathlib import Path
import yaml


def get_data_file(path):
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    patch = Path(path).suffix
    if patch == '.json':
        return json.load(open(path))
    return yaml.load(open(path), Loader=yaml.Loader)


def get_diff_data(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    removed = d1_keys - d2_keys
    added = d2_keys - d1_keys
    modified_dict = \
        {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    modified = {}
    for key in modified_dict:
        value_1, value_2 = modified_dict[key]
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            modified[key] = get_diff_data(value_1, value_2)
        else:
            return {'add': added, 'removed': removed,
                    'modified': modified_dict, 'same': same}
    return {'add': added, 'removed': removed, 'modified': modified,
            'same': same}