import asyncio
from typing import List, Union

from .base import BasePollyObject
from .enums import Gender, VoiceID, LanguageCode, SpeechMarkTypes
from .speech import Speech, SpeechMarksList

__all__ = ['Voice', 'VoicesList']


class Voice(BasePollyObject):
    additional_language_codes: List[str] = None
    gender: Gender
    id: VoiceID
    language_code: LanguageCode
    language_name: str
    name: str

    async def synthesize_speech(self, text: str,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_types: str = None,
                                text_type: str = None,
                                language_code: str = None,
                                lexicon_names: str = None,
                                auto_convert: bool = None,
                                **convert_params
                                ) -> Union[Speech, SpeechMarksList]:
        return await self.polly.synthesize_speech(text=text,
                                                  voice_id=self.id,
                                                  output_format=output_format,
                                                  sample_rate=sample_rate,
                                                  speech_mark_types=speech_mark_types,
                                                  text_type=text_type,
                                                  language_code=language_code,
                                                  lexicon_names=lexicon_names,
                                                  auto_convert=auto_convert,
                                                  **convert_params)


class VoicesList(BasePollyObject):
    next_token: str = None
    voices: List[Voice]

    def __iter__(self):
        return iter(self.voices)

    def __getitem__(self, item):
        return self.voices[item]

    async def synthesize_speech(self, text: str,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_types: List[Union[SpeechMarkTypes, str]] = None,
                                text_type: str = None,
                                language_code: str = None,
                                lexicon_names: str = None,
                                auto_convert: bool = None,
                                **convert_params
                                ) -> Union[List[Speech], List[SpeechMarksList]]:
        return await asyncio.gather(
            *(
                voice.synthesize_speech(text=text,
                                        output_format=output_format,
                                        sample_rate=sample_rate,
                                        speech_mark_types=speech_mark_types,
                                        text_type=text_type,
                                        language_code=language_code,
                                        lexicon_names=lexicon_names,
                                        auto_convert=auto_convert,
                                        **convert_params)
                for voice in self.voices
            )
        )
