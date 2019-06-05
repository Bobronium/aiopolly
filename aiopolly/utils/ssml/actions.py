"""
See documentation: https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html
"""

import re
from enum import Enum
from typing import Union

from .enums import Level, Strength, Volume, Rate, Pitch, Interpretations, DateFormat, Frequency, Duration
from ...types import LanguageCode, Alphabet

DEFAULT_EXCLUDE = ('tag', 'text', 'sep')

__all__ = [
    'breath',
    'clean_text_from_ssml_tags',
    'drc',
    'emphasis',
    'lang',
    'mark',
    'paragraph',
    'pause',
    'phoneme',
    'prosody',
    'say_as',
    'sentence',
    'soft',
    'ssml_text',
    'sub',
    'timbre',
    'whisper',
]


def make_params(mapping: dict = None,
                exclude: Union[set, list, tuple] = DEFAULT_EXCLUDE,
                allowed: Union[set, list, tuple] = None,
                **params) -> str:
    if isinstance(exclude, set):
        exclude.update(DEFAULT_EXCLUDE)
    elif isinstance(exclude, list):
        exclude.extend(DEFAULT_EXCLUDE)

    if allowed is None:
        allowed = params

    if mapping is None:
        mapping = {}

    return ' '.join(
        f'{mapping.get(key, key)}="{value.value if isinstance(value, Enum) else value}"'
        for key, value in params.items()
        if value is not None
        and key not in exclude
        and key in allowed
    )


def clean_text_from_ssml_tags(text):
    return re.sub('<[^<]+>', '', text)


def ssml_text(*parts, sep=' '):
    return f'<speak>{sep.join(parts)}</speak>'


def pause(strength: Union[Strength, str] = None,
          seconds: Union[int, float] = None,
          milliseconds: Union[int, float] = None):
    tag = '<break {params}/>'

    milliseconds = milliseconds and f'{milliseconds}ms'
    seconds = seconds and f'{seconds}s'

    mapping = {
        'seconds': 'time',
        'milliseconds': 'time'
    }

    return tag.format(params=make_params(**locals()))


def emphasis(text: str, level: Union[Level, str] = None) -> str:
    tag = '<emphasis {params}>{text}</emphasis>'

    return tag.format(text=text, params=make_params(**locals()))


def lang(text: str, language_code: Union[LanguageCode, str]) -> str:
    if isinstance(language_code, Enum):
        language_code = language_code.value

    return f'<lang xml:lang="{language_code}">{text}</lang>.'


def mark(tag_name: str) -> str:
    return f'<mark name="{tag_name}"/>'


def paragraph(text: str) -> str:
    return f'<p>{text}</p>'


def sentence(text: str) -> str:
    return f'<s>{text}</s>'


def phoneme(text: str, alphabet: Union[Alphabet, str], ph: str) -> str:
    if isinstance(alphabet, Enum):
        alphabet = alphabet.value
    return f'<phoneme alphabet="{alphabet}" ph="{ph}">{text}</phoneme>'


def prosody(*text: str,
            volume: Union[Volume, str, int] = None,
            rate: Union[Rate, str, int] = None,
            pitch: Union[Pitch, str, int] = None,
            max_duration_seconds: Union[int, float] = None,
            max_duration_milliseconds: Union[int, float] = None,
            sep=' ') -> str:
    tag = '<prosody {params}>{text}</prosody>'

    if volume and isinstance(volume, int):
        volume = f'{volume}dB'
    if rate and isinstance(rate, int):
        rate = f'{rate}%'
    if pitch and isinstance(pitch, int):
        pitch = f'{pitch}%'

    max_duration_seconds = max_duration_seconds and f'{max_duration_seconds}s'
    max_duration_milliseconds = max_duration_milliseconds and f'{max_duration_milliseconds}ms'

    mapping = {
        'max_duration_seconds': 'amazon:max-duration',
        'max_duration_milliseconds': 'amazon:max-duration'
    }

    return tag.format(text=sep.join(text), params=make_params(**locals()))


def say_as(text: str, interpret_as: Union[Interpretations, str], date_format: Union[DateFormat, str] = None) -> str:
    tag = '<say-as {params}>{text}</say-as>'

    if isinstance(interpret_as, Enum):
        interpret_as = interpret_as.value

    mapping = {
        'date_format': 'format',
        'interpret_as': 'interpret-as'
    }

    return tag.format(text=text, params=make_params(**locals()))


def sub(abbreviation: str, alias: str) -> str:
    return f'<sub alias="{alias}">{abbreviation}</sub>'


def breath(*text: str,
           duration: Union[Duration, str] = None,
           frequency: Union[Frequency, str] = None,
           volume: Union[Volume, str] = None,
           sep=' ') -> str:
    """
    Adding the Sound of Breathing
    https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html#breath-tag

    Natural-sounding speech includes both correctly spoken words and breathing sounds.
    By adding breathing sounds to synthesized speech, you can make it sound more natural.
    The <amazon:breath> and <amazon:auto-breaths> tags provide breaths.

    You have the following options:
        Manual mode: you set the location, length, and volume of a breath sound within the text
        Automated mode: Amazon Polly automatically inserts breathing sounds into the speech output
        Mixed mode: both you and Amazon Polly add breathing sounds

    Examples:

    Single breath:
    .. code_block python3:

        ssml_text(
            f'Sometimes you want to insert only {breath(volume=Volume.x_loud)} a single breath.'
        )

    .. code_block python3

        ssml_text(
            'Sometimes you need',
            breath('to insert one or more average breathes'),
            'so that the text sounds correct.'
        )


    :param text: text parts for automated breath
    :param duration: Controls how loud the breathing sounds. Valid values are listed in Duration enum
    :param frequency: Controls how often breathing sounds occur in the text. Valid values are listed in Frequency enum
    :param volume: Controls how loud the breathing sounds. Valid values are listed in Volume enum
    :param sep: separator for text parts
    """
    if text:
        if duration or frequency or volume:
            raise ValueError('You can\'t any params with auto-breath')
        return f'<amazon:auto-breaths>{sep.join(text)}</amazon:auto-breaths>'

    tag = '<amazon:breath {params}/>'

    return tag.format(params=make_params(**locals()))


def drc(*text: str, sep=' ') -> str:
    return f'<amazon:effect name="drc">{sep.join(text)}</amazon:effect>.'


def soft(*text: str, sep=' ') -> str:
    return f'<amazon:effect phonation="soft">{sep.join(text)}</amazon:effect>'


def timbre(*text: str, adjust: int = None, absolute: int = None, sep=' ') -> str:
    if adjust is not None:
        value = f'+{adjust}%' if adjust >= 0 else f'{adjust}%'
    elif absolute is not None:
        value = f'{absolute}%'
    else:
        raise ValueError('Both adjust and absolute cannot be None')

    return f'<amazon:effect vocal-tract-length="{value}">{sep.join(text)}</amazon:effect>'


def whisper(*text: str, sep=' '):
    return f'<amazon:effect name=”whispered”>{sep.join(text)}</amazon:effect>'
