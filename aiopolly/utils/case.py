import functools
import re
from typing import Union, Callable, Any


def string_to_camel(string: str):
    return ''.join(x[:1].upper() + x[1:] for x in string.split('_'))


def string_to_lower_camel(string: str):
    in_camel = string_to_camel(string)
    if len(in_camel) > 1:
        return in_camel[0].lower() + in_camel[1:]
    elif string:
        return in_camel.lower()


def string_to_snake(string: str):
    result = re.sub('([A-Z]+)', r'_\1', string).lower()
    if result.startswith('_'):
        return result[1:]
    return result


def to_case(
        obj: Union[str, dict, list, Any],
        ignore_string=False,
        any_type=False,
        str_converter: Callable = string_to_snake
) -> Union[str, dict, list, Any]:
    if isinstance(obj, str):
        return obj if ignore_string else str_converter(obj)
    elif isinstance(obj, dict):
        return {
            str_converter(key):
            to_case(value, ignore_string=True, any_type=True, str_converter=str_converter)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [
            to_case(element, ignore_string=True, any_type=True, str_converter=str_converter)
            for element in obj
        ]
    elif any_type:
        return obj

    raise ValueError(f'Unexpected type {type(obj)}. Supported types: str, dict, list')


to_snake = functools.partial(to_case, str_converter=string_to_snake)
to_camel = functools.partial(to_case, str_converter=string_to_camel)
to_lower_camel = functools.partial(to_case, str_converter=string_to_lower_camel)
