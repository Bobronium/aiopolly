# aiopolly
![Python 3.7](https://img.shields.io/badge/Python%203.7-blue.svg) 

Asynchronous client for Amazon Polly API which respects PEP-8 and has type-hinting

# Installation
```bash
$ pip install "https://github.com/MrMrRozbat/aiopolly/archive/master.zip"
```

# Examples

## Quick demonstration
```python
import asyncio
import time

from aiopolly import Polly, types


async def main():
    time_start = time.time()
    # Initializing AWS Polly client
    polly = Polly(voice_id='Joanna', output_format='mp3')

    # Getting all available voices
    voices = await polly.describe_voices()

    text = 'Whatever you can do I can override it, got a million ways to synthesize it'
    
    # Asynchronously synthesizing text with all received voices
    synthesized = await voices.synthesize_speech(text, language_code=types.LanguageCode.en_us)

    # Asynchronously saving each synthesized audio on disk
    await asyncio.gather(
        *(speech.save_on_disc(directory='examples') for speech in synthesized)
    )

    # Counting how many characters were synthesized
    characters_synthesized = sum(speech.request_characters for speech in synthesized)

    print(f'{characters_synthesized} characters are synthesized on {len(synthesized)} voices '
          f'and saved on disc in {time.time() - time_start} seconds!')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


## Dealing with credentials
You can init this class using one of three methods of authorisation:

1) Provide prepared botocore Credentials instance:
    ```python
   from aiopolly import Polly
   from botocore.credentials import Credentials
    
   credentials = Credentials(access_key='access_key', secret_key='your_secret_key')
   polly = Polly(credentials=credentials)
    ```
3) Provide your access and secret keys directly:
    ```python
   from aiopolly import Polly
    
   polly = Polly(access_key='access_key', secret_key='your_secret_key')
    ```

3) Create a ~/.aws/credentials file with following data:
    ```
    [default]
        aws_access_key_id = your_access_key
        aws_secret_access_key = your_secret_key
    ```
    And init class without any auth params:
    ```python
   from aiopolly import Polly
    
   polly = Polly()
    ```

## Using default params
You can init Polly client with any default param listed bellow. 
Those will be used when same params in API methods remain empty.
```python
from aiopolly import Polly, types

polly = Polly(
    voice_id='Joanna',
    output_format='ogg_vorbis',
    sample_rate='16000',
    speech_mark_type='ssml',
    text_type='ssml',
    language_code=types.LanguageCode.en_us,
    lexicon_names=['myLexicon', 'alsoMyLexicon'],
    output_s3_key_prefix='s3_key_prefix',
    output_s3_bucket_name='s3_bucket_name',
    include_additional_language_codes=True
)
```
## Managing lexicons
```python
import asyncio

from aiopolly import Polly
from aiopolly.types import Alphabet, LanguageCode
from aiopolly.utils.lexicon import LexiconTemplate, Lexeme

async def main():
    # Creating a new Polly instance with default output format 'mp3'
    polly = Polly(output_format='mp3')

    # Creating a new lexicon template with 'ipa' alphabet and 'en_US' language code
    lexicon = LexiconTemplate(alphabet=Alphabet.ipa, lang=LanguageCode.en_us)

    # Creating some lexemes
    python_lexemes = [
        Lexeme(grapheme='PEP', alias='Python Enhancement Proposals'),
        Lexeme(grapheme='ML', alias='Machine Learning'),
        Lexeme(grapheme='aiopolly', phoneme='eɪˈaɪoʊˈpɑli'),
        Lexeme(grapheme='aiogram', phoneme='eɪˈaɪoʊˌgræm')
    ]

    # Adding lexemes to lexicon
    lexicon.add_lexemes(*python_lexemes)

    # Putting lexicon on Amazon server (LexiconTemplate will be converted to a valid xml string automatically)
    await polly.put_lexicon(lexicon_name='PythonML', content=lexicon)

    text = 'Python is a beautiful programming language which is commonly used for web backend and ML. ' \
           'It also has cool style guides listed in PEP-8, and many community libraries like aiopolly or aiogram.'

    # Synthesizing speech with lexicon we just created 
    # (we don't need to specify required param "output_format", as we using it by default)
    speech = await polly.synthesize_speech(text, voice_id='Matthew', lexicon_names=['PythonML'])
    
    # Saving speech on disk with default name
    await speech.save_on_disc()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


###### Inspired by Alex Root Junior's [aiogram](https://github.com/aiogram/aiogram)