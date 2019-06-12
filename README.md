# aiopolly
[![Python 3.7](https://img.shields.io/badge/Python%203.7-blue.svg)](https://python.org) 
[![Amazon Polly API](https://img.shields.io/badge/-Amazon%20Polly%20API-orange.svg?logo=amazon&labelColor=gray)](https://docs.aws.amazon.com/en_us/polly/latest/dg/what-is.html)

Asynchronous client for Amazon Polly API which is written with asyncio and aiohttp and uses pydantic models
 
# Features
- Asynchronous
- Respects PEP-8 (no camelCase args and vars)
- Provides easy way to work with SSML tags and lexicons
- Has a audio convert support and built-in async opus converter
- Has mapped and classified AWS API exceptions

# Installation
```bash
$ pip install aiopolly
```

# Getting started
To work with AWS Polly you need AWS account, IAM User and it's credentials, [here's the instructions](https://docs.aws.amazon.com/en_us/polly/latest/dg/setting-up.html) how to get it

Then you can init this class using one of two methods:

1) Provide your access and secret keys directly:
    ```python
   from aiopolly import Polly
    
   polly = Polly(access_key='your_access_key', secret_key='your_secret_key')
    ```


2) Create a ~/.aws/credentials file with following data:
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


# Examples

## Many voices
```python
import asyncio
import time

from aiopolly import Polly, types


async def main():
    time_start = time.time()
    # Initializing AWS Polly client with default output_format
    polly = Polly(output_format=types.AudioFormat.mp3)

    voices = await polly.describe_voices()

    text = 'Whatever you can do I can override it, got a million ways to synthesize it'
    
    # Asynchronously synthesizing text with all available voices
    synthesized = await voices.synthesize_speech(text, language_code=types.LanguageCode.en_us)

    # Asynchronously saving each synthesized audio on disk
    await asyncio.gather(
        *(speech.save_on_disc(directory='examples') for speech in synthesized)
    )

    # Counting how many characters were synthesized
    characters_synthesized = sum(speech.request_characters for speech in synthesized)

    print(f'{characters_synthesized} characters are synthesized on {len(synthesized)}speech'
          f'and saved on disc in {time.time() - time_start} seconds!')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Managing lexicons
```python
import asyncio

from aiopolly import Polly
from aiopolly.types import Alphabet, AudioFormat, LanguageCode, VoiceID
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
    # Creating a new lexicon with 'ipa' alphabet and 'en_US' language code
    lexicon = new_lexicon(alphabet=Alphabet.ipa, lang=LanguageCode.en_us, lexemes=python_lexemes)

    # Putting lexicon on Amazon server
    lexicon_name = 'PythonML'
    await polly.put_lexicon(lexicon_name=lexicon_name, content=lexicon)

    text = 'Python is a beautiful programming language which is commonly used for web backend and ML. ' \
           'It also has cool style guides listed in PEP-8, and many community libraries like aiopolly or aiogram.'

    # Synthesizing speech with lexicon we just created 
    # (we don't need to specify required param "output_format", as we using it by default)
    speech = await polly.synthesize_speech(text, voice_id=VoiceID.Matthew, lexicon_names=[lexicon_name])
    
    # Saving speech on disk with default name
    await speech.save_on_disc()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Using SSML Text
aiopolly got built-in ssml-text factory which you can use to manage your ssml text:
```python
import asyncio

from aiopolly import Polly
from aiopolly.types import AudioFormat, VoiceID, TextType
from aiopolly.utils.ssml import ssml_text, prosody
from aiopolly.utils.ssml.params import Volume, Pitch, Rate

super_fast = prosody(f'''\
Uh, sama lamaa duma lamaa you assuming I'm a human\
What I gotta do to get it through to you I'm superhuman\
Innovative and I'm made of rubber\
So that anything you say is ricocheting off of me and it'll glue to you\
I'm devastating more than ever demonstrating\
How to give a motherfuckin' audience a feeling like it's levitating\
Never fading and I know that the haters are forever waiting\
For the day that they can say I fell off they'd be  celebrating\
'Cause I know the way to get 'em motivated
''',
    rate=Rate.x_fast, volume=Volume.x_loud, pitch=Pitch.high
)


async def main():
    # Creating a new Polly instance with default output format 'mp3'
    polly = Polly(output_format=AudioFormat.mp3)

    text = ssml_text(super_fast)

    speech = await polly.synthesize_speech(text, voice_id=VoiceID.Matthew, text_type=TextType.ssml)

    await speech.save_on_disc(directory='speech')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Using default params
You can init Polly client with any default params.
Those will be used when same params in API methods remain empty.
```python
from aiopolly import Polly, types

polly = Polly(
    voice_id=types.VoiceID.Joanna,
    output_format=types.AudioFormat.ogg_vorbis,
    sample_rate='16000',
    speech_mark_types=['ssml'],
    text_type=types.TextType.ssml,
    language_code=types.LanguageCode.en_us,
    lexicon_names=['myLexicon', 'alsoMyLexicon'],
    output_s3_key_prefix='s3_key_prefix',
    output_s3_bucket_name='s3_bucket_name',
    include_additional_language_codes=True,
    **{'other_default_param': 'value'}
)
```

# To-Do:
- Test Synthesis tasks (not tested yet)
- Write tests
- Get rid of botocore (built-in request signer needed)
- More docs?


###### Inspired by Alex Root Junior's [aiogram](https://github.com/aiogram/aiogram)