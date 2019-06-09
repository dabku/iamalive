import secrets
import hashlib
from collections import OrderedDict


def create_token(byte_length=24):
    return secrets.token_urlsafe(byte_length)


def hash_string(string_to_hash):
    h = hashlib.sha256()
    h.update(string_to_hash.encode('utf-8'))
    return h.digest()


def extract_properties_from_dict(current_dict, paths=None, current_path=None):
    if paths is None:
        paths = []
    if current_path is None:
        current_path = []

    for item in current_dict:
        current_path.append(item)
        if isinstance(current_dict[item], dict) or isinstance(current_dict[item], OrderedDict):
            extract_properties_from_dict(current_dict[item], paths, current_path)
        else:
            current_path.pop()
            paths.append((current_path[:], current_dict))

            break
    try:
        current_path.pop()
    except IndexError:
        pass
    return paths
