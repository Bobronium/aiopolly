from enum import Enum
from typing import Optional

__all__ = [
    'Alphabet',
    'AudioFormat',
    'ContentType',
    'Gender',
    'LanguageCode',
    'Region',
    'SpeechMarkTypes',
    'SynthesisTaskStatus',
    'TextType',
    'VoiceID',
]


class TextType(str, Enum):
    text = 'text'
    ssml = 'ssml'


class SpeechMarkTypes(str, Enum):
    ssml = 'ssml'
    sentence = 'sentence'
    viseme = 'viseme'
    word = 'word'


class SynthesisTaskStatus(str, Enum):
    scheduled = 'scheduled'
    in_progress = 'inProgress'
    completed = 'completed'
    failed = 'failed'


class Alphabet(str, Enum):
    ipa: str = 'ipa'
    x_sampa: str = 'x-sampa'
    x_amazon_pinyin: str = 'x-amazon-pinyin'


class Gender(Enum):
    female = 'Female'
    male = 'Male'


class AudioFormat(str, Enum):
    json = 'json'
    mp3 = 'mp3'
    pcm = 'pcm'
    ogg_vorbis = 'ogg_vorbis'


class ContentType(str, Enum):
    application_json = 'application/json'
    application_octet_stream = 'application/octet-stream'
    audio_json = 'application/x-json-stream'
    audio_mpeg = 'audio/mpeg'
    audio_pcm = 'audio/pcm'
    audio_ogg = 'audio/ogg'

    @property
    def audio_format(self) -> Optional[AudioFormat]:
        return AUDIO_CONTENT_TYPE_FORMAT_MAPPING.get(self)


class Region(str, Enum):
    us_east_2 = 'us-east-2'
    us_east_1 = 'us-east-1'
    us_west_1 = 'us-west-1'
    us_west_2 = 'us-west-2'
    ap_south_1 = 'ap-south-1'
    ap_northeast_2 = 'ap-northeast-2'
    ap_southeast_1 = 'ap-southeast-1'
    ap_southeast_2 = 'ap-southeast-2'
    ap_northeast_1 = 'ap-northeast-1'
    ca_central_1 = 'ca-central-1'
    cn_northwest_1 = 'cn-northwest-1'
    eu_central_1 = 'eu-central-1'
    eu_west_1 = 'eu-west-1'
    eu_west_2 = 'eu-west-2'
    eu_west_3 = 'eu-west-3'
    eu_north_1 = 'eu-north-1'
    sa_east_1 = 'sa-east-1'


class LanguageCode(str, Enum):
    arb = 'arb'
    cmn_CN = 'cmn-CN'
    cy_GB = 'cy-GB'
    da_DK = 'da-DK'
    de_DE = 'de-DE'
    en_AU = 'en-AU'
    en_GB = 'en-GB'
    en_GB_WLS = 'en-GB-WLS'
    en_IN = 'en-IN'
    en_US = 'en-US'
    es_ES = 'es-ES'
    es_MX = 'es-MX'
    es_US = 'es-US'
    fr_CA = 'fr-CA'
    fr_FR = 'fr-FR'
    is_IS = 'is-IS'
    it_IT = 'it-IT'
    ja_JP = 'ja-JP'
    hi_IN = 'hi-IN'
    ko_KR = 'ko-KR'
    nb_NO = 'nb-NO'
    nl_NL = 'nl-NL'
    pl_PL = 'pl-PL'
    pt_BR = 'pt-BR'
    pt_PT = 'pt-PT'
    ro_RO = 'ro-RO'
    ru_RU = 'ru-RU'
    sv_SE = 'sv-SE'
    tr_TR = 'tr-TR'


class VoiceID(str, Enum):
    Aditi = 'Aditi'
    Amy = 'Amy'
    Astrid = 'Astrid'
    Bianca = 'Bianca'
    Brian = 'Brian'
    Carla = 'Carla'
    Carmen = 'Carmen'
    Celine = 'Celine'
    Chantal = 'Chantal'
    Conchita = 'Conchita'
    Cristiano = 'Cristiano'
    Dora = 'Dora'
    Emma = 'Emma'
    Enrique = 'Enrique'
    Ewa = 'Ewa'
    Filiz = 'Filiz'
    Geraint = 'Geraint'
    Giorgio = 'Giorgio'
    Gwyneth = 'Gwyneth'
    Hans = 'Hans'
    Ines = 'Ines'
    Ivy = 'Ivy'
    Jacek = 'Jacek'
    Jan = 'Jan'
    Joanna = 'Joanna'
    Joey = 'Joey'
    Justin = 'Justin'
    Karl = 'Karl'
    Kendra = 'Kendra'
    Kimberly = 'Kimberly'
    Lea = 'Lea'
    Liv = 'Liv'
    Lotte = 'Lotte'
    Lucia = 'Lucia'
    Mads = 'Mads'
    Maja = 'Maja'
    Marlene = 'Marlene'
    Mathieu = 'Mathieu'
    Matthew = 'Matthew'
    Maxim = 'Maxim'
    Mia = 'Mia'
    Miguel = 'Miguel'
    Mizuki = 'Mizuki'
    Naja = 'Naja'
    Nicole = 'Nicole'
    Penelope = 'Penelope'
    Raveena = 'Raveena'
    Ricardo = 'Ricardo'
    Ruben = 'Ruben'
    Russell = 'Russell'
    Salli = 'Salli'
    Seoyeon = 'Seoyeon'
    Takumi = 'Takumi'
    Tatyana = 'Tatyana'
    Vicki = 'Vicki'
    Vitoria = 'Vitoria'
    Zeina = 'Zeina'
    Zhiyu = 'Zhiyu'


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
