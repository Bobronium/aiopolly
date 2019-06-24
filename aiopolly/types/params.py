from typing import Optional

from aiopolly.utils.case import to_lower_camel
from ..utils.strenum import StrEnum

__all__ = [
    'Alphabet',
    'AudioFormat',
    'ContentType',
    'Gender',
    'LanguageCode',
    'Region',
    'SpeechMarkTypes',
    'StrEnum',
    'SynthesisTaskStatus',
    'TextType',
    'VoiceID',
]


class TextType(StrEnum):
    text: str
    ssml: str


class SpeechMarkTypes(StrEnum):
    ssml: str
    sentence: str
    viseme: str
    word: str


class SynthesisTaskStatus(StrEnum, converter=to_lower_camel):
    scheduled: str
    in_progress: str
    completed: str
    failed: str


class Alphabet(StrEnum, sep='-'):
    ipa: str
    x_sampa: str
    x_amazon_pinyin: str


class Gender(StrEnum):
    Female: str
    Male: str


class AudioFormat(StrEnum):
    json: str
    mp3: str
    pcm: str
    ogg_vorbis: str


class ContentType(StrEnum, converter=lambda s: s.replace('_', '/', 1), sep='-'):
    application_json: str
    application_octet_stream: str
    application_x_json_stream: str
    audio_mpeg: str
    audio_pcm: str
    audio_ogg: str

    @property
    def audio_format(self) -> Optional[AudioFormat]:
        return AUDIO_CONTENT_TYPE_FORMAT_MAPPING.get(self)


class Region(StrEnum, sep='-'):
    us_east_2: str
    us_east_1: str
    us_west_1: str
    us_west_2: str
    ap_south_1: str
    ap_northeast_2: str
    ap_southeast_1: str
    ap_southeast_2: str
    ap_northeast_1: str
    ca_central_1: str
    cn_northwest_1: str
    eu_central_1: str
    eu_west_1: str
    eu_west_2: str
    eu_west_3: str
    eu_north_1: str
    sa_east_1: str


class LanguageCode(StrEnum, sep='-'):
    arb: str
    cmn_CN: str
    cy_GB: str
    da_DK: str
    de_DE: str
    en_AU: str
    en_GB: str
    en_GB_WLS: str
    en_IN: str
    en_US: str
    es_ES: str
    es_MX: str
    es_US: str
    fr_CA: str
    fr_FR: str
    is_IS: str
    it_IT: str
    ja_JP: str
    hi_IN: str
    ko_KR: str
    nb_NO: str
    nl_NL: str
    pl_PL: str
    pt_BR: str
    pt_PT: str
    ro_RO: str
    ru_RU: str
    sv_SE: str
    tr_TR: str


class VoiceID(StrEnum):
    Aditi: str
    Amy: str
    Astrid: str
    Bianca: str
    Brian: str
    Carla: str
    Carmen: str
    Celine: str
    Chantal: str
    Conchita: str
    Cristiano: str
    Dora: str
    Emma: str
    Enrique: str
    Ewa: str
    Filiz: str
    Geraint: str
    Giorgio: str
    Gwyneth: str
    Hans: str
    Ines: str
    Ivy: str
    Jacek: str
    Jan: str
    Joanna: str
    Joey: str
    Justin: str
    Karl: str
    Kendra: str
    Kimberly: str
    Lea: str
    Liv: str
    Lotte: str
    Lucia: str
    Mads: str
    Maja: str
    Marlene: str
    Mathieu: str
    Matthew: str
    Maxim: str
    Mia: str
    Miguel: str
    Mizuki: str
    Naja: str
    Nicole: str
    Penelope: str
    Raveena: str
    Ricardo: str
    Ruben: str
    Russell: str
    Salli: str
    Seoyeon: str
    Takumi: str
    Tatyana: str
    Vicki: str
    Vitoria: str
    Zeina: str
    Zhiyu: str


AUDIO_CONTENT_TYPES = (
    ContentType.audio_ogg,
    ContentType.audio_pcm,
    ContentType.application_x_json_stream,
    ContentType.audio_mpeg
)

AUDIO_CONTENT_TYPE_FORMAT_MAPPING = {
    ContentType.audio_mpeg: AudioFormat.mp3,
    ContentType.application_x_json_stream: AudioFormat.json,
    ContentType.audio_pcm: AudioFormat.pcm,
    ContentType.audio_ogg: AudioFormat.ogg_vorbis
}
