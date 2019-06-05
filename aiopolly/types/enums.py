from enum import Enum
from typing import Optional

__all__ = [
    'Alphabet',
    'AudioFormat',
    'ContentType',
    'Gender',
    'LanguageCode',
    'SpeechMarkTypes',
    'SynthesisTaskStatus',
    'TextType',
    'VoiceID',
    'AUDIO_CONTENT_TYPES',
    'AUDIO_CONTENT_TYPE_FORMAT_MAPPING',
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


class LanguageCode(str, Enum):
    arb = 'arb'
    cmn_cn = 'cmn-CN'
    cy_gb = 'cy-GB'
    da_dk = 'da-DK'
    de_de = 'de-DE'
    en_au = 'en-AU'
    en_gb = 'en-GB'
    en_gb_wls = 'en-GB-WLS'
    en_in = 'en-IN'
    en_us = 'en-US'
    es_es = 'es-ES'
    es_mx = 'es-MX'
    es_us = 'es-US'
    fr_ca = 'fr-CA'
    fr_fr = 'fr-FR'
    is_is = 'is-IS'
    it_it = 'it-IT'
    ja_jp = 'ja-JP'
    hi_in = 'hi-IN'
    ko_kr = 'ko-KR'
    nb_no = 'nb-NO'
    nl_nl = 'nl-NL'
    pl_pl = 'pl-PL'
    pt_br = 'pt-BR'
    pt_pt = 'pt-PT'
    ro_ro = 'ro-RO'
    ru_ru = 'ru-RU'
    sv_se = 'sv-SE'
    tr_tr = 'tr-TR'


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
