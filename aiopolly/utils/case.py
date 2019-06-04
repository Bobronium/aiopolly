import re
from typing import Union


def string_to_camel(string: str):
    return ''.join(x.capitalize() for x in string.split('_'))


def string_to_snake(string: str):
    result = re.sub('([A-Z]+)', r'_\1', string).lower()
    if result.startswith('_'):
        return result[1:]
    return result


def to_snake(obj: Union[str, dict, list], ignore_string=False, no_exception=False):
    if isinstance(obj, str):
        return obj if ignore_string else string_to_snake(obj)
    elif isinstance(obj, dict):
        return {string_to_snake(k): to_snake(v, ignore_string=True, no_exception=True)
                for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_snake(element, ignore_string=True, no_exception=True)
                for element in obj]
    elif no_exception:
        return obj

    raise ValueError(f'Unexpected type {type(obj)}. Supported types: str, dict, list')


def to_camel(obj: Union[str, dict, list], ignore_string=False, no_exception=False):
    if isinstance(obj, str):
        return obj if ignore_string else string_to_camel(obj)
    elif isinstance(obj, dict):
        return {string_to_camel(k): to_camel(v, ignore_string=True, no_exception=True)
                for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_camel(element, ignore_string=True, no_exception=True)
                for element in obj]
    elif no_exception:
        return obj

    raise ValueError(f'Unexpected type {type(obj)}. Supported types: str, dict, list')
