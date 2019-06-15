import asyncio
import time

from aiopolly import Polly, types


async def main():
    time_start = time.time()
    # Initializing AWS Polly client
    polly = Polly(voice_id=types.VoiceID.Joanna, output_format=types.AudioFormat.mp3)

    # Getting all available voices
    voices = await polly.describe_voices()

    text = 'Whatever you can do I can override it, got a million ways to synthesize it'

    # Asynchronously synthesizing text with all received voices
    synthesized = await voices.synthesize_speech(text, language_code=types.LanguageCode.en_US)

    # Asynchronously saving each synthesized audio on disk
    await asyncio.gather(
        *(speech.save_on_disc(directory='speech') for speech in synthesized)
    )

    # Counting how many characters were synthesized
    characters_synthesized = sum(speech.request_characters for speech in synthesized)

    print(f'{characters_synthesized} characters are synthesized on {len(synthesized)} voices '
          f'and saved on disc in {time.time() - time_start} seconds!')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
