import functools
import io
from typing import List, Union

import aiofiles

from .base import BasePollyObject
from .enums import LanguageCode, AudioFormat, ContentType, TextType, SpeechMarkTypes

__all__ = ['Speech', 'SpeechMarks', 'SpeechMarksList']

SPEECH_CONTENT_TYPE_KEY = 'content_type'
SPEECH_REQUEST_CHARACTERS_KEY = 'request_characters'
SPEECH_AUDIO_STREAM_KEY = 'audio_stream'


class Speech(BasePollyObject):
    content_type: ContentType
    request_characters: int
    audio_stream: bytes
    text: str
    voice_id: str
    output_format: AudioFormat
    sample_rate: str = None
    speech_mark_types: SpeechMarkTypes = None
    text_type: TextType = None
    language_code: LanguageCode = None
    lexicon_names: List[str] = None

    @property
    def format(self):
        return self.output_format.split('_')[0].strip()

    @property
    @functools.lru_cache()
    def clean_text(self):
        if self.text_type == 'text':
            return self.text

        from ..utils.ssml import clean_text_from_ssml_tags
        return clean_text_from_ssml_tags(self.text)

    @property
    def bytes_io(self):
        return io.BytesIO(self.audio_stream)

    async def save_on_disc(self, filename=None, directory=None):
        if filename is None:
            text = self.clean_text
            text = text if len(text) < 50 else f'{text[:50]}...'
            filename = f'{self.voice_id} - {text}.{self.format}'
        if directory is not None:
            filename = '/'.join((directory, filename))

        async with aiofiles.open(filename, mode='wb') as file:
            await file.write(self.audio_stream)


class SpeechMarks(BasePollyObject):
    time: int
    type: SpeechMarkTypes
    value: str
    start: int = None
    end: int = None


class SpeechMarksList(BasePollyObject):
    speech_marks: List[SpeechMarks]

    @property
    def vesemes(self):
        return self.get_marks(SpeechMarkTypes.viseme)

    @property
    def sentences(self):
        return self.get_marks(SpeechMarkTypes.sentence)

    @property
    def words(self):
        return self.get_marks(SpeechMarkTypes.word)

    @property
    def ssml(self):
        return self.get_marks(SpeechMarkTypes.ssml)

    def get_marks(self, mark_type: Union[SpeechMarkTypes, str]):
        return [mark for mark in self.speech_marks if mark.type == mark_type]

    def get_marks_values(self, mark_type: Union[SpeechMarkTypes, str]):
        return [mark.value for mark in self.get_marks(mark_type)]

    @property
    def total_time(self):
        return self.speech_marks[-1].time
