import asyncio

from aiopolly import Polly
from aiopolly.types import Alphabet, AudioFormat, VoiceID, LanguageCode
from aiopolly.utils.lexicon import new_lexicon, new_lexeme


async def main():
    # Creating a new Polly instance with default output format 'mp3'
    polly = Polly(output_format=AudioFormat.mp3)

    # Creating some lexemes
    python_lexemes = [
        new_lexeme(grapheme='PEP', alias='Python Enhancement Proposals'),
        new_lexeme(grapheme='ML', alias='Machine Learning'),
        new_lexeme(grapheme='aiopolly', phoneme='eɪˈaɪoʊˈpɑli'),
        new_lexeme(grapheme='aiogram', phoneme='eɪˈaɪoʊˌgræm')
    ]

    # Adding lexemes to lexicon
    lexicon = new_lexicon(alphabet=Alphabet.ipa, lang=LanguageCode.en_US, lexemes=python_lexemes)

    # Putting lexicon on Amazon server (LexiconTemplate will be converted to a valid xml string automatically)
    await polly.put_lexicon(lexicon_name='PythonML', content=lexicon)

    text = 'Python is a beautiful programming language which is commonly used for web backend and ML. ' \
           'It also has cool style guides listed in PEP-8, and many community libraries like aiopolly or aiogram.'

    # Synthesizing speech with lexicon we just created
    # (we don't need to specify required param "output_format", as we using mp3 by default)
    speech = await polly.synthesize_speech(text, voice_id=VoiceID.Matthew, lexicon_names=['PythonML'])

    # Saving speech on disk with default name
    await speech.save_on_disc(directory='speech')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
