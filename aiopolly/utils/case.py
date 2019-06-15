import functools
import re
from typing import Union, Callable


def string_to_camel(string: str):
    return ''.join(x[:1].upper() + x[1:] for x in string.split('_'))


def string_to_snake(string: str):
    result = re.sub('([A-Z]+)', r'_\1', string).lower()
    if result.startswith('_'):
        return result[1:]
    return result


def to_case(obj: Union[str, dict, list],
            ignore_string=False,
            no_exception=False,
            str_case_converter: Callable = string_to_snake) -> Union[str, dict, list]:
    if isinstance(obj, str):
        return obj if ignore_string else str_case_converter(obj)
    elif isinstance(obj, dict):
        return {str_case_converter(key): to_case(value, ignore_string=True, no_exception=True,
                                                 str_case_converter=str_case_converter)
                for key, value in obj.items()}
    elif isinstance(obj, list):
        return [to_case(element, ignore_string=True, no_exception=True, str_case_converter=str_case_converter)
                for element in obj]
    elif no_exception:
        return obj

    raise ValueError(f'Unexpected type {type(obj)}. Supported types: str, dict, list')


to_snake = functools.partial(to_case, str_case_converter=string_to_snake)
to_camel = functools.partial(to_case, str_case_converter=string_to_camel)
