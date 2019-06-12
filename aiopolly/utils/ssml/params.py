"""
See documentation: https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html
"""
from enum import Enum

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


class Level(str, Enum):
    """
    :enum Strong: Increases the volume and slows the speaking rate so that the speech is louder and slower.
    :enum Moderate: Increases the volume and slows the speaking rate, but less than strong. Moderate is the default.
    :enum Reduced: Decreases the volume and speeds up the speaking rate. Speech is softer and faster.
    """
    strong = 'strong'
    moderate = 'moderate'
    reduced = 'reduced'


class Strength(str, Enum):
    """
    :enum none: No pause. Use none to remove a normally occurring pause, such as after a period.
    :enum x-weak: Has the same strength as none, no pause.
    :enum weak: Sets a pause of the same duration as the pause after a comma.
    :enum medium: Has the same strength as weak.
    :enum strong: Sets a pause of the same duration as the pause after a sentence.
    :enum x-strong: Sets a pause of the same duration as the pause after a paragraph.
    """
    none = 'none'
    x_weak = 'x-weak'
    weak = 'weak'
    medium = 'medium'
    strong = 'strong'
    x_strong = 'x-strong'


class Volume(str, Enum):
    """
    :enum default: Resets volume to the default level for the current voice.
    :enums: silent, x-soft, soft, medium, loud, x-loud: Sets the volume to a predefined value for the current voice.
    """
    default = 'default'
    silent = 'silent'
    x_soft = 'x-soft'
    soft = 'soft'
    medium = 'medium'
    loud = 'loud'
    x_loud = 'x-loud'


class Rate(str, Enum):
    """
    :enums: x-slow, slow, medium, fast,x-fast. Sets the pitch to a predefined value for the selected voice.
    """
    x_slow = 'x-slow'
    slow = 'slow'
    medium = 'medium'
    fast = 'fast'
    x_fast = 'x-fast'


class Pitch(str, Enum):
    """
    :enum default: Resets pitch to the default level for the current voice.
    :enums x-low, low, medium, high, x-high: Sets the pitch to a predefined value for the current voice.
    """
    default = 'default'
    x_low = 'x-low'
    low = 'low'
    medium = 'medium'
    high = 'high'
    x_high = 'x-high'


class Interpretation(str, Enum):
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
    characters = 'characters'
    spell_out = 'spell-out'
    cardinal = 'cardinal'
    number = 'number'
    ordinal = 'ordinal'
    digits = 'digits'
    fraction = 'fraction'
    unit = 'unit'
    date = 'date'
    time = 'time'
    address = 'address'
    expletive = 'expletive'
    telephone = 'telephone'


class DateFormat(str, Enum):
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

    mdy = 'mdy'
    dmy = 'dmy'
    ymd = 'ymd'
    md = 'md'
    dm = 'dm'
    ym = 'ym'
    my = 'my'
    d = 'd'
    m = 'm'
    y = 'y'
    yyyymmdd = 'yyyymmdd'


class Frequency(str, Enum):
    """Controls how often breathing sounds occur in the text."""
    default = 'default'
    x_low = 'x-low'
    low = 'low'
    medium = 'medium'
    high = 'high'
    x_high = 'x-high'


class Duration(str, Enum):
    """Controls the length of the breath."""
    default = 'default'
    x_low = 'x-short'
    low = 'short'
    medium = 'medium'
    high = 'long'
    x_high = 'x-long'


class SpeechPart(str, Enum):
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
    VB = 'amazon:VB'
    VBD = 'amazon:VBD'
    SENSE_1 = 'amazon:SENSE_1'
