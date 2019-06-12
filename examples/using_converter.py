import asyncio

from aiopolly import Polly
from aiopolly.types import AudioFormat, TextType, VoiceID
from aiopolly.utils.converter import OpusConverter
from aiopolly.utils.ssml import ssml_text, pause, Strength


async def main():
    converter = OpusConverter(auto_convert=True, keep_original=True)
    polly = Polly(output_format=AudioFormat.mp3, converter=converter)

    text = ssml_text(f'''
sendVoice

Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. 
For this to work, your audio must be in an {pause(Strength.none)}.ogg file encoded with OPUS 
(other formats may be sent as Audio or Document)
''')

    # Synthesizing speech with lexicon we just created
    # (we don't need to specify required param "output_format", as we using mp3 by default)
    speech = await polly.synthesize_speech(
        text,
        voice_id=VoiceID.Matthew,
        lexicon_names=['PythonML'],
        text_type=TextType.ssml
    )

    # Saving speech on disk with default name
    await speech.save_on_disc(directory='speech')
    await speech.save_on_disc(directory='speech', converted=False)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
