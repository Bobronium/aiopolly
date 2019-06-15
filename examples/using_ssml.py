import asyncio

from aiopolly import Polly
from aiopolly.types import AudioFormat, VoiceID, TextType
from aiopolly.types import LanguageCode
from aiopolly.utils.ssml import ssml_text, prosody, emphasis, pause, lang, paragraph, phoneme, sentence
from aiopolly.utils.ssml.params import Level, Volume, Pitch, Alphabet, Rate, Strength

with_pause = f'Mary had a little lamb {pause(seconds=3)}Whose fleece was white as snow.'

with_emphasis = f'I already told you I {emphasis("really like", level=Level.strong)} that person.'

with_foreign_text = lang('Je ne parle pas français', language_code=LanguageCode.fr_FR)

paragraphs = paragraph('This is the first paragraph. There should be a pause after this text is spoken.',
                       'This is the second paragraph')

with_phonemes = (f'You say, {phoneme("pecan", alphabet=Alphabet.ipa, ph="pɪˈkɑːn")}. '
                 f'I say, {phoneme("pecan", alphabet=Alphabet.ipa, ph="ˈpi.kæn")}.')

with_prosody = (f'Each morning when I wake up, {prosody("I speak quite slowly", volume="loud", rate="x-slow")}'
                ' and deliberately until I have my coffee')

sentences = sentence(
    'Mary had a little lamb',
    'Whose fleece was white as snow,',
    'And everywhere that Mary went, the lamb was sure to go.'
)

super_fast = prosody(
    f'''
Uh, sama lamaa duma lamaa you assuming I'm a human\
What I gotta do to get it through to you I'm superhuman\
Innovative and I'm made of rubber\
So that anything you say is ricocheting off of me and it'll glue to you\
I'm devastating more than ever demonstrating\
How to give a motherfuckin' audience a feeling like it's levitating\
Never fading and I know that the haters are forever waiting\
For the day that they can say I fell off they'd be  celebrating\
'Cause I know the way to get 'em motivated, ''',
    rate=Rate.x_fast, volume=Volume.x_loud, pitch=Pitch.high
)


async def main():
    # Creating a new Polly instance with default output format 'mp3'
    polly = Polly(output_format=AudioFormat.mp3)

    text = ssml_text(
        with_pause,
        with_emphasis,
        with_foreign_text,
        with_phonemes,
        with_prosody,
        paragraphs,
        sentences,
        super_fast,
        sep=pause(Strength.x_strong)
    )

    # Synthesizing speech with lexicon we just created
    # (we don't need to specify required param "output_format", as we using mp3 by default)
    speech = await polly.synthesize_speech(text, voice_id=VoiceID.Matthew, text_type=TextType.ssml)

    # Saving speech on disk with default name
    await speech.save_on_disc(directory='speech')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
