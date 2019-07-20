import datetime
import functools
import logging

from pydantic import BaseModel, Extra
from pydantic.json import timedelta_isoformat

from ..utils import json
from ..utils.case import to_camel

__all__ = ['BasePollyObject']

log = logging.getLogger('aiopolly')


class BasePollyObject(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow
        validate_assignment = True
        allow_population_by_alias = True
        alias_generator = to_camel

        json_encoders = {
            datetime.datetime: lambda v: (v.replace(tzinfo=None) - datetime.datetime(1970, 1, 1)).total_seconds(),
            datetime.timedelta: timedelta_isoformat,
        }

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

    def raw_dict(self):
        """
        :return: raw data that we get from AWS Polly API
        """
        return json.loads(self.dict(by_alias=True))

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
