"""
Based on: https://github.com/MrMrRobat/AnyStrEnum
"""

from enum import Enum, EnumMeta, _EnumDict, auto
from inspect import signature
from types import FunctionType
from typing import List, Callable, AnyStr, Set, TypeVar, Type, Any

SEP_ATTR = "__sep__"
CONVERTER_ATTR = "__converter__"

TYPE_BLACKLIST = FunctionType, property, type, classmethod, staticmethod


class StrItem:
    __slots__ = 'sep', 'converter'

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
    __return_missing__: bool = False

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
        # In Python 3.8 the signature of 'EnumMeta._get_mixins_' was changed from (bases) to (class_name, bases)
        # However, 'class_name' is unneccessary and only used to print an exception
        # So we examine the signature accordingly and pick the right one
        if len(signature(mcs._get_mixins_).parameters) == 2:  # (class_name, bases)
            mixin_type, base_enum = mcs._get_mixins_(cls, bases)
        else:  # Fallback to (bases) signature
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

    def __call__(cls, value, **kwargs):
        """
        For ability to check values by 'isinstance'
        (only if their type same as enums base type)

        >>> class MyEnum(StrEnum):
        ...     __return_missing__ = True
        ...     member1: str
        ...     member2: str
        ...
        >>> value_to_check = 'invalid_member'
        >>> if not isinstance(MyEnum(value_to_check), MyEnum):
        ...     print(f'{value_to_check} is not a valid MyEnum')
        invalid_member is not a valid MyEnum

        :param value: value to check
        :param kwargs: named args for EnumMeta
        """

        try:
            return super().__call__(value, **kwargs)
        except ValueError:
            if not kwargs and cls.__return_missing__ and type(value) is cls._member_type_:
                return value
            raise

    @staticmethod
    def check_type_equals(type_to_check: Any, allowed_type: Type[Any]):
        if type_to_check is not allowed_type:
            raise TypeError(f'Unexpected type {getattr(type_to_check, "__name__", type_to_check)}'
                            f', allowed type: {allowed_type.__name__}')


class StrEnum(BaseStrEnum, metaclass=StrEnumMeta):
    __return_missing__ = True
