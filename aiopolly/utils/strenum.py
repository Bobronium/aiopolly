"""
Based on: https://github.com/MrMrRobat/AnyStrEnum
"""

from enum import Enum, EnumMeta, _EnumDict, auto
from types import FunctionType
from typing import List, Callable, AnyStr, Set, TypeVar, Type, Any

SEP_ATTR = "__sep__"
CONVERTER_ATTR = "__converter__"

TYPE_BLACKLIST = FunctionType, property, type, classmethod, staticmethod

class StrItem:
    # https://youtrack.jetbrains.com/issue/PY-24426
    # noinspection PyMissingConstructor
    def __init__(self, sep: AnyStr = None, converter: Callable[[str], str] = None):
        self.sep = sep
        self.converter = converter

    def generate_value(self, name: str) -> str:
        if self.converter:
            name = self.converter(name)
        if self.sep:
            name = name.replace('_', self.sep)

        return name


class BaseStrEnum(str, Enum):
    __sep__: str = None
    __converter__: Callable[[str], str] = None

    def _generate_next_value_(*_):
        return auto()

    @classmethod
    def filter(cls,
               contains: AnyStr = None, *,
               contained_in: AnyStr = None,
               startswith: AnyStr = None,
               endswith: AnyStr = None,
               case_sensitive: bool = False,
               intersection: bool = True,
               inverse: bool = False) -> Set['StrEnum']:
        """
        :param contains: filter all enum members which are contain some substring
        :param startswith: filter all enum members which are start with some substring
        :param endswith: filter all enum members which are end with some substring
        :param contained_in: filter all enum members which are substrings of some string
        :param case_sensitive: defines whether found values must match case of given string
        :param inverse: if True, all enum members except found will be returned
        :param intersection: indicates whether function should return all found objects or their interception
        :return: all found enums
        """

        def prepare(value):
            if case_sensitive:
                return value
            return value.lower()

        found_sets: List[set] = []
        if contains:
            contains = prepare(contains)
            found_sets.append({e for e in cls if contains in prepare(e)})
        if startswith:
            startswith = prepare(startswith)
            found_sets.append({e for e in cls if prepare(e).startswith(startswith)})
        if endswith:
            endswith = prepare(endswith)
            found_sets.append({e for e in cls if prepare(e).endswith(endswith)})
        if contained_in:
            contained_in = prepare(contained_in)
            found_sets.append({e for e in cls if prepare(e) in contained_in})

        if not found_sets:
            return set()

        if intersection:
            found = found_sets[0].intersection(*found_sets[1:])
        else:
            found = found_sets[0].union(*found_sets[1:])

        if inverse:
            return {e for e in cls} - found

        return found

    def __str__(self):
        return self.value


class StrEnumMeta(EnumMeta):
    # It's here to avoid 'got an unexpected keyword argument' TypeError
    @classmethod
    def __prepare__(mcs, *args, sep: AnyStr = None, converter: Callable[[str], str] = None, **kwargs):
        return super().__prepare__(*args, **kwargs)

    def __new__(mcs, cls, bases, class_dict, sep: AnyStr = None, converter: Callable[[str], str] = None):
        mixin_type, base_enum = mcs._get_mixins_(bases)
        if not issubclass(base_enum, BaseStrEnum):
            raise TypeError(f'Unexpected Enum type \'{base_enum.__name__}\'. '
                            f'Only {BaseStrEnum.__name__} and its subclasses are allowed')
        if not issubclass(mixin_type, (str, bytes)):
            raise TypeError(f'Unexpected mixin type \'{mixin_type.__name__}\'. '
                            f'Only str, bytes and their subclasses are allowed')

        # Trying to get sep and converter from class dict and base enum class
        if sep is None:
            sep = class_dict.get(SEP_ATTR) or base_enum.__sep__
        if converter is None:
            converter = class_dict.get(CONVERTER_ATTR) or base_enum.__converter__

        item = StrItem(sep=sep, converter=converter)
        new_class_dict = _EnumDict()
        for name, type_hint in class_dict.get('__annotations__', {}).items():
            if name.startswith('_') or name in class_dict:
                continue
            mcs.check_type_equals(type_hint, mixin_type)
            value = item.generate_value(name)
            new_class_dict[name] = value
            mcs.check_type_equals(type(value), mixin_type)

        for name, value in class_dict.items():
            if isinstance(value, StrItem):
                value = value.generate_value(name)
            if not (name.startswith('_') or isinstance(value, TYPE_BLACKLIST)):
                mcs.check_type_equals(type(value), mixin_type)

            new_class_dict[name] = value

        new_class_dict[SEP_ATTR] = sep
        new_class_dict[CONVERTER_ATTR] = converter

        return super().__new__(mcs, cls, bases, new_class_dict)

    @staticmethod
    def check_type_equals(type_to_check: Any, allowed_type: Type[Any]):
        if type_to_check is not allowed_type:
            raise TypeError(f'Unexpected type {getattr(type_to_check, "__name__", type_to_check)}'
                            f', allowed type: {allowed_type.__name__}')


class StrEnum(BaseStrEnum, metaclass=StrEnumMeta):
    ...
