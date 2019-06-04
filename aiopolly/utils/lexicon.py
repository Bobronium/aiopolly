from dataclasses import dataclass
from typing import Union, List

from ..types import LanguageCode, Alphabet

LEXICON_TEMPLATE = '''\
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0" 
      xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon 
        http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
      alphabet="{alphabet}" 
      xml:lang="{lang}">
  {lexemes}
</lexicon>
'''

LEXEME_TEMPLATE = '<lexeme>%s\n  </lexeme>'
GRAPHEME_TEMPLATE = '\n     <grapheme>%s</grapheme>'
PHONEME_TEMPLATE = '\n     <phoneme>%s</phoneme>'
ALIAS_TEMPLATE = '\n     <alias>%s</alias>'


def lexemes_to_xml(lexemes):
    if isinstance(lexemes, list):
        lexemes_xml = ''.join(lexemes_to_xml(lexeme) for lexeme in lexemes)
    elif isinstance(lexemes, dict):
        lexemes_xml = create_lexeme(**lexemes)
    elif hasattr(lexemes, 'to_str'):
        lexemes_xml = lexemes.to_str()
    elif isinstance(lexemes, str):
        lexemes_xml = lexemes
    else:
        raise ValueError(f'Unsupported lexemes type {type(lexemes)}')

    return lexemes_xml


def create_lexicon(alphabet: Alphabet, lang: LanguageCode,
                   lexemes: Union[str, dict, List[dict], 'LexiconTemplate', List['LexiconTemplate']]):
    lexemes_xml = lexemes_to_xml(lexemes)

    if isinstance(alphabet, Alphabet):
        alphabet = alphabet.value
    if isinstance(lang, LanguageCode):
        lang = lang.value

    return LEXICON_TEMPLATE.format(alphabet=alphabet, lang=lang, lexemes=lexemes_xml)


def create_lexeme(grapheme: str, *, phoneme: str = None, alias: str = None):
    lexeme = GRAPHEME_TEMPLATE % grapheme
    if phoneme is not None:
        lexeme += PHONEME_TEMPLATE % phoneme
    if alias is not None:
        lexeme += ALIAS_TEMPLATE % alias

    return LEXEME_TEMPLATE % lexeme


@dataclass
class Lexeme:
    grapheme: str
    phoneme: str = None
    alias: str = None

    def to_str(self):
        if not (self.alias or self.phoneme):
            raise ValueError('Lexeme must have an alias or phoneme')
        return create_lexeme(self.grapheme, phoneme=self.phoneme, alias=self.alias)


@dataclass
class LexiconTemplate:
    alphabet: Union[Alphabet, str]
    lang: Union[LanguageCode, str]
    lexemes: Union[List[Lexeme], List[dict]] = None

    def to_str(self):
        if not self.lexemes:
            raise ValueError('Lexicon must contain at least one lexeme')
        return create_lexicon(self.alphabet, self.lang, self.lexemes)

    def add_lexemes(self, *lexemes):
        if self.lexemes:
            self.lexemes.extend(lexemes)
        else:
            self.lexemes = list(lexemes)
