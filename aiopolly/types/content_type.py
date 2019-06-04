from enum import Enum
from typing import Optional

__all__ = ['AudioFormat', 'ContentType', 'AUDIO_CONTENT_TYPES']


class AudioFormat(Enum):
    json = 'json'
    mp3 = 'mp3'
    pcm = 'pcm'
    ogg_vorbis = 'ogg_vorbis'


class ContentType(str, Enum):
    application_json = 'application/json'
    application_octet_stream = 'application/octet-stream'
    audio_json = 'audio/json'
    audio_mpeg = 'audio/mpeg'
    audio_pcm = 'audio/pcm'
    audio_ogg = 'audio/ogg'

    @property
    def audio_format(self) -> Optional[AudioFormat]:
        return AUDIO_CONTENT_TYPE_FORMAT_MAPPING.get(self)


AUDIO_CONTENT_TYPES = (
    ContentType.audio_ogg,
    ContentType.audio_pcm,
    ContentType.audio_json,
    ContentType.audio_mpeg
)

AUDIO_CONTENT_TYPE_FORMAT_MAPPING = {
    ContentType.audio_mpeg: AudioFormat.mp3,
    ContentType.audio_json: AudioFormat.json,
    ContentType.audio_pcm: AudioFormat.pcm,
    ContentType.audio_ogg: AudioFormat.ogg_vorbis
}
