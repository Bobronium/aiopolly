import asyncio
from enum import Enum
from typing import List

from .base import BasePollyObject
from .language_code import LanguageCode
from .speech import Speech

__all__ = ['Gender', 'Voice', 'VoicesList']


class Gender(Enum):
    female = 'Female'
    male = 'Male'


class Voice(BasePollyObject):
    additional_language_codes: List[str] = None
    gender: Gender
    id: str
    language_code: LanguageCode
    language_name: str
    name: str

    async def synthesize_speech(self, text: str,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_type: str = None,
                                text_type: str = None,
                                language_code: str = None,
                                lexicon_names: str = None,
                                ) -> Speech:
        return await self.polly.synthesize_speech(text=text,
                                                  voice_id=self.id,
                                                  output_format=output_format,
                                                  sample_rate=sample_rate,
                                                  speech_mark_type=speech_mark_type,
                                                  text_type=text_type,
                                                  language_code=language_code,
                                                  lexicon_names=lexicon_names)


class VoicesList(BasePollyObject):
    next_token: str = None
    voices: List[Voice]

    def __iter__(self):
        for voice in self.voices:
            yield voice

    def __getitem__(self, item):
        return self.voices[item]

    async def synthesize_speech(self, text: str,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_type: str = None,
                                text_type: str = None,
                                language_code: str = None,
                                lexicon_names: str = None,
                                ) -> List[Speech]:
        return await asyncio.gather(
            *(
                voice.synthesize_speech(text=text,
                                        output_format=output_format,
                                        sample_rate=sample_rate,
                                        speech_mark_type=speech_mark_type,
                                        text_type=text_type,
                                        language_code=language_code,
                                        lexicon_names=lexicon_names)
                for voice in self.voices
            )
        )
