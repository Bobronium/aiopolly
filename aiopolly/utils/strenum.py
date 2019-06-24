import abc
from enum import Enum, EnumMeta, _EnumDict, auto
from typing import List, Callable, AnyStr, TypeVar, Union, Type, Any, Iterable

SEP_ATTR = "__sep__"
CONVERTER_ATTR = "__converter__"


def check_type_equals(type_to_check: Union[TypeVar, Type[Any]], allowed_type: Type[Any]):
    if isinstance(type_to_check, TypeVar):
        if len(type_to_check.__constraints__) > 1:
            raise TypeError(f'Only {allowed_type} is allowed, not {type_to_check} {type_to_check.__constraints__}')

        elif issubclass(type_to_check.__constraints__[0], allowed_type):
            raise TypeError(f'Unexpected type {type_to_check.__constraints__[0]}, allowed type: {allowed_type}')

    elif not isinstance(type_to_check, type) or not issubclass(type_to_check, allowed_type):
        raise TypeError(f'Unexpected type {type_to_check}, allowed type: {allowed_type}')


def resolve_mixin(types: Iterable[Type[Any]], expected_types: Iterable[Type[Any]]) -> Type[Any]:
    """
    :param types: types which we need to check for some parent class in them
    :param expected_types: classes which is expected to be parent class of one object in :param types
    :return first of expected_types which is found as subclass of any given types
    :raises TypeError if non of expected_types is subclass of any given types
    """
    for expected_type in expected_types:
        if any(obj for obj in types if issubclass(obj, expected_type)):
            return expected_type

    raise TypeError(f'None of expected mixins {expected_types} found in {types} bases')


def getattr_from_objects(objects: Iterable[Any], attr: str, *default: Any):
    """
    :param objects: objects to get attribute from
    :param attr: attribute to get
    :param default: value which will be returned in case when none of given objects have needed attr
    :return: value from getattr() on first object which has needed attr or default value if given
    :raises: AttributeError if none of objects has needed attr
    """
    for obj in objects:
        try:
            return getattr(obj, attr)
        except AttributeError:
            continue
    else:
        try:
            return default[0]
        except IndexError:
            raise AttributeError(f'None of objects in {objects} has attr "{attr}"')


class BaseItem(abc.ABC):
    @abc.abstractmethod
    def __call__(self, name: str, str_type: Type[AnyStr]) -> AnyStr:
        pass


class Item(BaseItem):

    def __init__(self, sep: AnyStr = None, converter: Callable[[AnyStr, type], AnyStr] = None):
        self.sep = sep
        self.converter = converter

    def __call__(self, name: str, str_type: Type[AnyStr]) -> AnyStr:
        return self.convert(name, str_type)

    def convert(self, name: str, str_type) -> AnyStr:
        if str_type is str:
            new_name = str(name)
        elif str_type is bytes:
            new_name = bytes(name, 'utf8')
        else:
            raise TypeError(f'Unexpected type of string: {str_type}, expected types: str, bytes')

        if self.converter:
            new_name = self.converter(new_name)
        if self.sep:
            old_sep = '_' if issubclass(str_type, str) else b'_'
            new_name = new_name.replace(old_sep, self.sep)

        return new_name


auto_str = Item


class StrEnumMeta(EnumMeta):

    # It's here to avoid 'got an unexpected keyword argument' TypeError
    @classmethod
    def __prepare__(mcs, *args, sep: AnyStr = None, converter: Callable[[AnyStr], AnyStr] = None, **kwargs):
        return super().__prepare__(*args, **kwargs)

    def __new__(mcs, cls, bases, class_dict, sep: AnyStr = None, converter: Callable[[AnyStr], AnyStr] = None):
        # Trying to get sep and converter from class dict and base classes
        if sep is None:
            sep = class_dict.get(SEP_ATTR) or getattr_from_objects(bases, SEP_ATTR, None)
        if converter is None:
            converter = class_dict.get(CONVERTER_ATTR) or getattr_from_objects(bases, CONVERTER_ATTR, None)

        str_type = resolve_mixin(bases, (str, bytes))
        str_converter = Item(sep=sep, converter=converter)

        new_class_dict = _EnumDict()
        for name, obj_type in class_dict.get('__annotations__', {}).items():
            if name.startswith('_') or name in class_dict:
                continue
            check_type_equals(obj_type, str_type)
            new_class_dict[name] = str_converter(name, str_type)

        for name, value in class_dict.items():
            if isinstance(value, BaseItem):
                value = value(name, str_type=str_type)
            elif isinstance(value, auto):
                value = str_converter(name, str_type=str_type)
            new_class_dict[name] = value

        new_class_dict[SEP_ATTR] = sep
        new_class_dict[CONVERTER_ATTR] = converter

        return super().__new__(mcs, cls, bases, new_class_dict)


class BaseStrEnum(Enum):
    def __str__(self):
        return self.value

    @classmethod
    def search(cls,
               contains: AnyStr = None,
               contained: AnyStr = None,
               startswith: AnyStr = None,
               endswith: AnyStr = None,
               case_sensitive: bool = False,
               intersection: bool = True,
               inverse: bool = False) -> List['StrEnum']:
        """
        :param contains: search all enum members which are contain some substring
        :param startswith: search all enum members which are start with some substring
        :param endswith: search all enum members which are end with some substring
        :param contained: search all enum members which are substrings of some string
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
        if contained:
            contained = prepare(contained)
            found_sets.append({e for e in cls if prepare(e) in contained})

        if not found_sets:
            return []

        if intersection:
            found = found_sets[0].intersection(*found_sets[1:])
        else:
            found = found_sets[0].union(*found_sets[1:])

        if inverse:
            return list({e for e in cls} - found)

        return list(found)


class StrEnum(str, BaseStrEnum, metaclass=StrEnumMeta):
    pass


class BytesEnum(bytes, BaseStrEnum, metaclass=StrEnumMeta):

    def __str__(self):
        return str(self.value)
