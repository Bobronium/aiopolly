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


def new_lexeme(grapheme: str, *, phoneme: str = None, alias: str = None):
    result = GRAPHEME_TEMPLATE % grapheme

    if phoneme is not None:
        result += PHONEME_TEMPLATE % phoneme
    if alias is not None:
        result += ALIAS_TEMPLATE % alias

    return LEXEME_TEMPLATE % result


def new_lexicon(alphabet: Alphabet, lang: LanguageCode,
                lexemes: Union[str, dict, List[Union[dict, str]]]):
    lexemes_xml = lexemes_to_xml(lexemes)

    if isinstance(alphabet, Alphabet):
        alphabet = alphabet.value
    if isinstance(lang, LanguageCode):
        lang = lang.value

    return LEXICON_TEMPLATE.format(alphabet=alphabet, lang=lang, lexemes=lexemes_xml)


def lexemes_to_xml(lexemes):
    if isinstance(lexemes, list):
        lexemes_xml = ''.join(lexemes_to_xml(l) for l in lexemes)
    elif isinstance(lexemes, dict):
        lexemes_xml = new_lexeme(**lexemes)
    elif hasattr(lexemes, 'to_str'):
        lexemes_xml = lexemes.to_str()
    elif isinstance(lexemes, str):
        lexemes_xml = lexemes
    else:
        raise ValueError(f'Unsupported lexemes type {type(lexemes)}')

    return lexemes_xml
