"""
See documentation: https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html
"""

import re
from enum import Enum
from typing import Union

from .params import Level, Strength, Volume, Rate, Pitch, Interpretation, DateFormat, Frequency, Duration, SpeechPart
from ...types import LanguageCode, Alphabet

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

DEFAULT_EXCLUDE = ('tag', 'text', 'sep')


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


def ssml_text(*text: str, sep=' '):
    """
    Function witch wraps all positional arguments in <speak></speak> tags

    The <speak> tag is the root element of all Amazon Polly SSML text.
    All SSML-enhanced text must be enclosed within a pair of <speak> tags.

    :param text:
    :param sep:
    :return:
    """
    return f'<speak>{sep.join(text)}</speak>'


def pause(strength: Union[Strength, str] = None,
          seconds: Union[int, float] = None,
          milliseconds: Union[int, float] = None):
    """
    You can set a pause based on strength (equivalent to the pause after a comma, a sentence, or a paragraph),
    or you can set it to a specific length of time in seconds or milliseconds.

    Example:
        code_block python3
            ssml_text(
                f'Mary had a little lamb {pause(seconds=3)}Whose fleece was white as snow.'
            )

    :param strength: affects on break time
    :param seconds: break time in seconds
    :param milliseconds: break time in milliseconds
    """
    tag = '<break {params}/>'

    milliseconds = milliseconds and f'{milliseconds}ms'
    seconds = seconds and f'{seconds}s'

    mapping = {
        'seconds': 'time',
        'milliseconds': 'time'
    }

    return tag.format(params=make_params(**locals()))


def emphasis(*text: str, level: Union[Level, str] = None, sep=' ') -> str:
    """
    To emphasize words, use the <emphasis> tag. Emphasizing words changes the speaking rate and volume.
    More emphasis makes Amazon Polly speak the text louder and slower.
    Less emphasis makes it speak quieter and faster. To specify the degree of emphasis, use the level attribute.

    :param text: text which will be emphasized
    :param level: degree of emphasis
    :param sep: sep between text if more than one given
    """

    tag = '<emphasis {params}>{text}</emphasis>'

    return tag.format(text=sep.join(text), params=make_params(**locals()))


def lang(*text: str, language_code: Union[LanguageCode, str], sep=' ') -> str:
    """
    Specify another language for a specific word, phrase, or sentence with the <lang> tag.
    Foreign language words and phrases are generally spoken better when they are enclosed within a pair of <lang> tags.

    :param text: foreign text
    :param language_code: text language
    :param sep:
    """
    if isinstance(language_code, Enum):
        language_code = language_code.value

    return f'<lang xml:lang="{language_code}">{sep.join(text)}</lang>.'


def mark(name: str) -> str:
    """
    To put a custom tag within the text, use the <mark> tag.
    Amazon Polly takes no action on the tag, but returns the location of the tag in the SSML metadata.

    :param name: name of your mark
    """
    return f'<mark name="{name}"/>'


def paragraph(*paragraphs: str, sep='\n') -> str:
    """
    Provides a longer pause than native speakers usually place at commas or the end of a sentence.

    :param paragraphs: paragraphs
    :param sep:
    :return:
    """

    return sep.join(f'<p>{p}</p>' for p in paragraphs)


def sentence(*sentences: str, sep=' ') -> str:
    """
    Adds a pause between lines or sentences in your text. Using this has the same effect as:
        Ending a sentence with a period (.)
        Specifying a pause with pause(strength='strong')

    :param sentences: sentences
    :param sep:
    :return:
    """
    return sep.join(f'<s>{s}</s>' for s in sentences)


def phoneme(text: str, alphabet: Union[Alphabet, str], ph: str) -> str:
    if isinstance(alphabet, Enum):
        alphabet = alphabet.value
    return f'<phoneme alphabet="{alphabet}" ph="{ph}">{text}</phoneme>'


def prosody(*text: str,
            volume: Union[Volume, str, int] = None,
            rate: Union[Rate, str, int] = None,
            pitch: Union[Pitch, str, int] = None,
            max_duration_s: Union[int, float] = None,
            max_duration_ms: Union[int, float] = None,
            sep=' ') -> str:
    """
    Controls the volume, rate, or pitch of your selected voice.
    Volume, speech rate, and pitch are dependent on the specific voice selected.
    In addition to differences between voices for different languages,
    there are differences between individual voices speaking the same language.
    Because of this, while attributes are similar across all languages,
    there are clear variations from language to language and no absolute value is available.

    :param text: text which will be combined together with :param sep in between
    :param volume: see Volume enum
    :param rate: see Rate enum
    :param pitch: see Pitch enum
    :param max_duration_s: controls how long speech will take when it is synthesized in seconds
    :param max_duration_ms: controls how long speech will take when it is synthesized in milliseconds
    :param sep:
    :return:
    """

    tag = '<prosody {params}>{text}</prosody>'

    if volume and isinstance(volume, int):
        volume = f'{volume}dB'
    if rate and isinstance(rate, int):
        rate = f'{rate}%'
    if pitch and isinstance(pitch, int):
        pitch = f'{pitch}%'

    max_duration_s = max_duration_s and f'{max_duration_s}s'
    max_duration_ms = max_duration_ms and f'{max_duration_ms}ms'

    mapping = {
        'max_duration_s': 'amazon:max-duration',
        'max_duration_ms': 'amazon:max-duration'
    }

    return tag.format(text=sep.join(text), params=make_params(**locals()))


def say_as(*text: str,
           interpret_as: Union[Interpretation, str],
           date_format: Union[DateFormat, str] = None,
           sep=' ') -> str:
    """
    Tells Amazon Polly how to say certain characters, words, and numbers.
    This enables you to provide additional context to eliminate any ambiguity on how Polly should render the text.

    :param text:
    :param interpret_as: see Interpretation enum
    :param date_format: see DateFormat enum
    :param sep:
    :return:
    """
    tag = '<say-as {params}>{text}</say-as>'

    if isinstance(interpret_as, Enum):
        interpret_as = interpret_as.value

    mapping = {
        'date_format': 'format',
        'interpret_as': 'interpret-as'
    }

    return tag.format(text=sep.join(text), params=make_params(**locals()))


def sub(abbreviation: str, alias: str) -> str:
    """
    Substitute a different word (or pronunciation) for selected text such as an acronym or abbreviation.

    :param abbreviation:
    :param alias:
    :return:
    """
    return f'<sub alias="{alias}">{abbreviation}</sub>'


def w(word: str, role: Union[SpeechPart, str]):
    """
    Customizes the pronunciation of words by specifying the word’s part of speech or alternate meaning.

    :param word: word to Customizes
    :param role: see SpeechPart enum
    :return:
    """
    return f'<w role="{role.value if isinstance(role, Enum) else role}">{word}</w>.'


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
    else:
        tag = '<amazon:breath {params}/>'

        return tag.format(params=make_params(**locals()))


def drc(*text: str, sep=' ') -> str:
    """
    Dynamic Range Compression

    Sets a midrange "loudness" threshold for your audio,
    and increases the volume (the gain) of the sounds around that threshold.
    It applies the greatest gain increase closest to the threshold,
    and the gain increase is lessened farther away from the threshold.

    :param text:
    :param sep:
    :return:
    """
    return f'<amazon:effect name="drc">{sep.join(text)}</amazon:effect>.'


def soft(*text: str, sep=' ') -> str:
    """
    Specifies that input text should be spoken in a softer-than-normal voice.

    :param text:
    :param sep:
    :return:
    """

    return f'<amazon:effect phonation="soft">{sep.join(text)}</amazon:effect>'


def timbre(*text: str, adjust: int = None, absolute: int = None, sep=' ') -> str:
    """
    Timbre is the tonal quality of a voice that helps you tell the difference between voices,
    even when they have the same pitch and loudness. One of the most important physiological
    features that contributes to speech timbre is the length of the vocal tract.
    The vocal tract is a cavity of air that spans from the top of the vocal folds up to the edge of the lips.

    :param text: text to adjust
    :param adjust:
        Adjusts the vocal tract length by a relative percentage change in the current voice.
        For example, +4% or -2%. Valid values range from +100% to -50%. Values outside this range are clipped.
        For example, +111% sounds like +100% and -60% sounds like -50%.
    :param absolute:
        Changes the vocal tract length to an absolute percentage of the tract length of the current voice.
        For example, 110% or 75%. An absolute value of 110% is equivalent to a relative value of +10%.
        An absolute value of 100% is the same as the default value for the current voice.
    :param sep:
    :return:
    """

    if adjust is not None:
        value = f'+{adjust}%' if adjust >= 0 else f'{adjust}%'
    elif absolute is not None:
        value = f'{absolute}%'
    else:
        raise ValueError('Both adjust and absolute cannot be None')

    return f'<amazon:effect vocal-tract-length="{value}">{sep.join(text)}</amazon:effect>'


def whisper(*text: str, sep=' '):
    """
    Indicates that the input text should be spoken in a whispered voice rather than as normal speech.
    This can be used with any of the voices in the Amazon Polly Text-to-Speech portfolio.

    :param text:
    :param sep:
    :return:
    """
    return f'<amazon:effect name=”whispered”>{sep.join(text)}</amazon:effect>'
