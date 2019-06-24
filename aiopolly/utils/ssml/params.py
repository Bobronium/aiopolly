"""
See documentation: https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html
"""

from ..strenum import StrEnum
from ...types import Alphabet

__all__ = [
    'Alphabet',
    'Frequency',
    'Duration',
    'Level',
    'Strength',
    'Volume',
    'Pitch',
    'Rate',
    'Interpretation',
    'DateFormat'
]


class DashParamEnum(StrEnum):
    __sep__ = '-'


class Level(DashParamEnum):
    """
    :enum Strong: Increases the volume and slows the speaking rate so that the speech is louder and slower.
    :enum Moderate: Increases the volume and slows the speaking rate, but less than strong. Moderate is the default.
    :enum Reduced: Decreases the volume and speeds up the speaking rate. Speech is softer and faster.
    """
    strong: str
    moderate: str
    reduced: str


class Strength(DashParamEnum):
    """
    :enum none: No pause. Use none to remove a normally occurring pause, such as after a period.
    :enum x-weak: Has the same strength as none, no pause.
    :enum weak: Sets a pause of the same duration as the pause after a comma.
    :enum medium: Has the same strength as weak.
    :enum strong: Sets a pause of the same duration as the pause after a sentence.
    :enum x-strong: Sets a pause of the same duration as the pause after a paragraph.
    """
    none: str
    x_weak: str
    weak: str
    medium: str
    strong: str
    x_strong: str


class Volume(DashParamEnum):
    """
    :enum default: Resets volume to the default level for the current voice.
    :enums: silent, x-soft, soft, medium, loud, x-loud: Sets the volume to a predefined value for the current voice.
    """
    default: str
    silent: str
    x_soft: str
    soft: str
    medium: str
    loud: str
    x_loud: str


class Rate(DashParamEnum):
    """
    :enums: x-slow, slow, medium, fast,x-fast. Sets the pitch to a predefined value for the selected voice.
    """
    x_slow: str
    slow: str
    medium: str
    fast: str
    x_fast: str


class Pitch(DashParamEnum):
    """
    :enum default: Resets pitch to the default level for the current voice.
    :enums x-low, low, medium, high, x-high: Sets the pitch to a predefined value for the current voice.
    """
    default: str
    x_low: str
    low: str
    medium: str
    high: str
    x_high: str


class Interpretation(DashParamEnum):
    """
    :enum characters or spell-out: Spells out each letter of the text, as in a-b-c.
    :enum cardinal or number: Interprets the numerical text as a cardinal number, as in 1,234.
    :enum ordinal: Interprets the numerical text as an ordinal number, as in 1,234th.
    :enum digits: Spells out each digit individually, as in 1-2-3-4.
    :enum fraction: Interprets the numerical text as a fraction.
    :enum unit: Interprets a numerical text as a measurement.
    :enum date: Interprets the text as a date. The format of the date must be specified with the format attribute.
    :enum time: Interprets the numerical text as duration, in minutes and seconds, as in 1'21".
    :enum address: Interprets the text as part of a street address.
    :enum expletive: "Beeps out" the content included within the tag.
    :enum telephone: Interprets the numerical text as a 7-digit or 10-digit telephone number, as in 2025551212.
    """
    characters: str
    spell_out: str
    cardinal: str
    number: str
    ordinal: str
    digits: str
    fraction: str
    unit: str
    date: str
    time: str
    address: str
    expletive: str
    telephone: str


class DateFormat(DashParamEnum):
    """
    :enum mdy: Month-day-year.
    :enum dmy: Day-month-year.
    :enum ymd: Year-month-day.
    :enum md: Month-day.
    :enum dm: Day-month.
    :enum ym: Year-month.
    :enum my: Month-year.
    :enum d: Day.
    :enum m: Month.
    :enum y: Year.
    :enum yyyymmdd: Year-month-day.
    """

    mdy: str
    dmy: str
    ymd: str
    md: str
    dm: str
    ym: str
    my: str
    d: str
    m: str
    y: str
    yyyymmdd: str


class Frequency(DashParamEnum):
    """Controls how often breathing sounds occur in the text."""
    default: str
    x_low: str
    low: str
    medium: str
    high: str
    x_high: str


class Duration(DashParamEnum):
    """Controls the length of the breath."""
    default: str
    x_short: str
    short: str
    medium: str
    long: str
    x_long: str


class SpeechPart(StrEnum, converter=lambda name: f'amazon:{name}'):
    """
    :enum amazon:VB: interprets the word as a verb (present simple).
    :enum: amazon:VBD: interprets the word as past tense or as a past participle.
    :enum amazon:SENSE_1: uses the non-default sense of the word when present.
        For example, the noun "bass" is pronounced differently depending on its meaning.
        The default meaning is the lowest part of the musical range.
        The alternate meaning is a species of freshwater fish,
        also called "bass" but pronounced differently.
        Using <w role="amazon:SENSE_1">bass</w> renders the non-default pronunciation
        (freshwater fish) for the audio text.

    """
    VB: str
    VBD: str
    SENSE_1: str
