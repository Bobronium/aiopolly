import datetime
import functools
import io
import logging
import os
from typing import List, Union

import aiofiles

from .base import BasePollyObject
from .enums import LanguageCode, AudioFormat, ContentType, TextType, SpeechMarkTypes

__all__ = ['Speech', 'SpeechMarks', 'SpeechMarksList']


class ConvertParams(BasePollyObject):
    to_format: str
    out_bitrate: int = None
    duration_in_seconds: int = None
    info: str = None


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

    converted: bool = False
    converted_stream: bytes = None
    converted_params: ConvertParams = None

    async def convert(self, **kwargs):
        converter = self.polly.converter
        if converter:
            return await self.polly.converter.convert(self, **kwargs)
        raise RuntimeError('Cannot find converter in Polly instance, to use it please specify one')

    @property
    def format(self):
        if self.converted and self.audio_stream == self.converted_stream:
            return self.converted_format
        return self.output_format.split('_')[0].strip()

    @property
    def converted_format(self):
        return self.converted_params.to_format.split('_')[0].strip()

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

    def filename(self, converted=True):
        if converted and self.converted:
            extension = self.converted_format
        else:
            extension = self.format

        name = self.clean_text
        if len(name) > 100:
            name = ' '.join(name[:100].split()[:-1]) + '...'
        name = f'{self.voice_id} - {name}.{extension}'

        return name

    async def save_on_disc(self, filename=None, directory=None, converted=True, overwrite=False):
        if converted and self.converted:
            stream = self.converted_stream
        else:
            stream = self.audio_stream

        if filename is None:
            filename = self.filename(converted=converted)
        if directory is not None:
            filename = '/'.join((directory, filename))

        while not overwrite and os.path.exists(filename):
            name, extension = filename.rsplit('.', maxsplit=1)
            now = datetime.datetime.now().strftime('%S.%f')
            filename = name + f' ({now[:-3]}).' + extension

        logging.debug('Saving %s on disc' % filename)

        async with aiofiles.open(filename, mode='wb') as file:
            await file.write(stream)


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

    def __iter__(self):
        return iter(self.speech_marks)

    def __getitem__(self, item):
        return self.speech_marks[item]
