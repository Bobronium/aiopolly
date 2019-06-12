import functools
import logging
from typing import TYPE_CHECKING, Dict, Set, Optional, Callable

from pydantic import BaseModel, Extra, Any
from pydantic.main import validate_model

from ..utils.case import to_camel

__all__ = ['BasePollyObject']

log = logging.getLogger('aiopolly')


class BasePollyObject(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow
        use_enum_values = True
        validate_assignment = True

    # need to suppress unwanted validation exceptions
    # noinspection PyMissingConstructor
    def __init__(self, **data: Any) -> None:
        if TYPE_CHECKING:  # pragma: no cover
            self.__values__: Dict[str, Any] = {}
            self.__fields_set__: Set[str] = set()
        values, fields_set, error = validate_model(self, data, raise_exc=False)
        object.__setattr__(self, '__values__', values)
        object.__setattr__(self, '__fields_set__', fields_set)

        if error:
            try:
                trust_api_responses = self.polly._trust_api_responses
            except RuntimeError:
                trust_api_responses = True

            if trust_api_responses:
                log.exception('Got unexpected params in API response:', exc_info=error)
            else:
                raise error

    def dict(self, *,
             use_camel_case: bool = False,
             include: Set[str] = None,
             exclude: Set[str] = None,
             by_alias: bool = False,
             skip_defaults: bool = False
             ) -> dict:

        result = BaseModel.dict(self, include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults)

        if use_camel_case:
            return to_camel(result)
        return result

    def json(self, *,
             use_camel_case: bool = False,
             include: Set[str] = None,
             exclude: Set[str] = None,
             by_alias: bool = False,
             skip_defaults: bool = False,
             encoder: Optional[Callable[[Any], Any]] = None,
             **dumps_kwargs: Any,
             ) -> str:

        return BaseModel.json(self, use_camel_case=use_camel_case, include=include,
                              exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults)

    @property
    @functools.lru_cache()
    def polly(self):
        """
        :rtype: aiopolly.polly.Polly
        """
        from .. import Polly
        polly = Polly.get_current()
        if polly is None:
            raise RuntimeError("Can't get polly instance from context. "
                               "You can fix it with setting current instance: "
                               "'Polly.set_current(polly_instance)'")
        return polly

    def __hash__(self):
        def _hash(obj):
            buf = 0
            if isinstance(obj, list):
                for item in obj:
                    buf += _hash(item)
            elif isinstance(obj, dict):
                for dict_key, dict_value in obj.items():
                    buf += hash(dict_key) + _hash(dict_value)
            else:
                try:
                    buf += hash(obj)
                except TypeError:  # Skip unhashable objects
                    pass
            return buf

        result = 0
        for key, value in sorted(self.fields.items()):
            result += hash(key) + _hash(value)

        return result
