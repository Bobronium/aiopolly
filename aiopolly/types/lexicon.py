import datetime
from typing import List

from .base import BasePollyObject
from .enums import LanguageCode, Alphabet

__all__ = ['LexiconAttribute', 'Lexicon', 'LexiconsList']


class LexiconAttribute(BasePollyObject):
    alphabet: Alphabet
    language_code: LanguageCode
    last_modified: datetime.datetime
    lexemes_count: int
    lexicon_arn: str
    size: int


class Lexicon(BasePollyObject):
    content: str = None
    name: str = None
    attributes: LexiconAttribute


class LexiconsList(BasePollyObject):
    lexicons: List[Lexicon]
    next_token: str = None

    def __iter__(self):
        for lexicon in self.lexicons:
            yield lexicon

    def __getitem__(self, item):
        return self.lexicons[item]
