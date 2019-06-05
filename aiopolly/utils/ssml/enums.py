"""
See documentation: https://docs.aws.amazon.com/en_us/polly/latest/dg/supported-ssml.html
"""
from enum import Enum

__all__ = [
    'Frequency',
    'Duration',
    'Level',
    'Strength',
    'Volume',
    'Pitch',
    'Rate',
    'Interpretations',
    'DateFormat'
]


class Level(str, Enum):
    strong = 'strong'
    moderate = 'moderate'
    reduced = 'reduced'


class Strength(str, Enum):
    none = 'none'
    x_weak = 'x-weak'
    weak = 'weak'
    medium = 'medium'
    strong = 'strong'
    x_strong = 'x-strong'


class Volume(str, Enum):
    default = 'default'
    silent = 'silent'
    x_soft = 'x-soft'
    soft = 'soft'
    medium = 'medium'
    loud = 'loud'
    x_loud = 'x-loud'


class Rate(str, Enum):
    x_slow = 'x-slow'
    slow = 'slow'
    medium = 'medium'
    fast = 'fast'
    x_fast = 'x-fast'


class Pitch(str, Enum):
    default = 'default'
    x_low = 'x-low'
    low = 'low'
    medium = 'medium'
    high = 'high'
    x_high = 'x-high'


class Interpretations(str, Enum):
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
    default = 'default'
    x_low = 'x-low'
    low = 'low'
    medium = 'medium'
    high = 'high'
    x_high = 'x-high'


class Duration(str, Enum):
    default = 'default'
    x_low = 'x-short'
    low = 'short'
    medium = 'medium'
    high = 'long'
    x_high = 'x-long'
