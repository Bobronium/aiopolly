import datetime
from typing import List, Union

from .base import BasePollyObject
from .enums import LanguageCode, Alphabet, SpeechMarkTypes
from .speech import SpeechMarksList, Speech

__all__ = ['LexiconAttribute', 'Lexicon', 'LexiconsList']


class LexiconAttribute(BasePollyObject):
    alphabet: Alphabet
    language_code: LanguageCode
    last_modified: datetime.datetime
    lexemes_count: int
    lexicon_arn: str
    size: int


class Lexicon(BasePollyObject):
    name: str = None
    content: str = None
    attributes: LexiconAttribute

    async def synthesize_speech(self, text: str,
                                voice_id: str = None,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_types: List[Union[SpeechMarkTypes, str]] = None,
                                text_type: str = None,
                                language_code: str = None,
                                auto_convert: bool = None,
                                **convert_params
                                ) -> Union[List[Speech], List[SpeechMarksList]]:
        """
        Synthesizes speech with self.name in lexicon_names
        """
        return self.polly.synthesize_speech(text=text,
                                            voice_id=voice_id,
                                            output_format=output_format,
                                            sample_rate=sample_rate,
                                            speech_mark_types=speech_mark_types,
                                            text_type=text_type,
                                            language_code=language_code,
                                            lexicon_names=[self.name],
                                            auto_convert=auto_convert,
                                            **convert_params)


class LexiconsList(BasePollyObject):
    lexicons: List[Lexicon]
    next_token: str = None

    async def synthesize_speech(self, text: str,
                                voice_id: str = None,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_types: List[Union[SpeechMarkTypes, str]] = None,
                                text_type: str = None,
                                language_code: str = None,
                                auto_convert: bool = None,
                                **convert_params
                                ) -> Union[List[Speech], List[SpeechMarksList]]:
        """
        Synthesizes speech with self.lexicon_names in lexicon_names
        """

        return self.polly.synthesize_speech(text=text,
                                            voice_id=voice_id,
                                            output_format=output_format,
                                            sample_rate=sample_rate,
                                            speech_mark_types=speech_mark_types,
                                            text_type=text_type,
                                            language_code=language_code,
                                            lexicon_names=self.lexicons_names,
                                            auto_convert=auto_convert,
                                            **convert_params)

    @property
    def lexicon_names(self) -> list:
        return [lexicon['name'] for lexicon in self.lexicons]

    def __iter__(self):
        return iter(self.lexicons)

    def __getitem__(self, item):
        return self.lexicons[item]
