import io

import aiofiles

from .base import BasePollyObject
from .content_type import ContentType

__all__ = ['Speech']


class Speech(BasePollyObject):
    content_type: ContentType
    request_characters: int
    audio_stream: bytes
    text: str
    voice_id: str
    output_format: str
    sample_rate: str = None
    speech_mark_type: str = None
    text_type: str = None
    language_code: str = None
    lexicon_names: list = None

    @property
    def format(self):
        return self.output_format.split('_')[0].strip()

    @property
    def bytes_io(self):
        return io.BytesIO(self.audio_stream)

    async def save_on_disc(self, filename=None, directory=None):
        if filename is None:
            text = self.text if len(self.text) < 30 else f'{self.text[:30]}...'
            filename = f'{self.voice_id} - {text}.{self.format}'
        if directory is not None:
            filename = '/'.join((directory, filename))

        async with aiofiles.open(filename, mode='wb') as file:
            await file.write(self.audio_stream)
