import logging
import re
from asyncio import create_subprocess_shell, subprocess
from typing import Sequence

from .base import BaseConverter
from ...types import Speech

__all__ = ['OpusConverter']

INPUT_PARAMS = {
    'pcm': '-f s16le -ar 16000 -ac 1 ',
}

FILTERS = {
    'atempo': 'atempo',
    'volume': 'volume',
}

DEFAULT_BITRATE = {
    'mp3': 48,
    'ogg_vorbis': 35,
    'pcm': 128
}

DEFAULT_SAMPLE_RATE = {
    'mp3': 24000,
    'ogg_vorbis': 24000,
    'pcm': 16000
}

COMMAND_TEMPLATE = '''\
ffmpeg {in_params}-i pipe:0 {filters} -ar {out_sample_rate} -f opus -acodec libopus -b:a {out_bitrate}k pipe:1
'''


def check_ffmpeg():
    import subprocess
    try:
        proc = subprocess.Popen(
            ['ffmpeg', '-encoders'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        encoders = stdout.decode()
    except Exception as e:
        raise RuntimeError(f'Unable to access ffmpeg on your system: {e}')

    if 'libopus' not in encoders:
        raise RuntimeError(f'Unable to find libopus in ffmpeg encoders:\n{stderr.decode()}')


class OpusConverter(BaseConverter):
    """
    This is sample class which provide ability to convert your speech to ogg_opus
    You can create your own basing on BaseConverter and use it.

    To use this converter you need FFMpeg with libopus installed on your system

    Default encode params:
        :param out_bitrate: preferred out_bitrate
        :param speed:
        :param tempo:
        :param volume:
    """

    def __init__(self,
                 out_bitrate: int = None,
                 sample_rate: int = None,
                 auto_convert: bool = True,
                 keep_original: bool = False,
                 excluded_filters: Sequence[str] = (),
                 **default_filters):

        check_ffmpeg()

        self.auto_convert = auto_convert
        self.keep_original = keep_original

        self.defaults = dict(out_bitrate=out_bitrate, sample_rate=sample_rate)
        self.default_filters = default_filters
        self.excluded_filters = excluded_filters

    async def convert(self, speech: Speech, out_bitrate: str = None, sample_rate: int = None, **filters):
        out_bitrate = out_bitrate or self.defaults.get('out_bitrate')
        sample_rate = sample_rate or self.defaults.get('sample_rate')

        cmd_params = self._get_cmd_params(speech, out_bitrate, sample_rate, filters)
        cmd = COMMAND_TEMPLATE.format(**cmd_params)

        bytestream, info = await self._execute(cmd, speech.audio_stream)
        duration_in_seconds = self._find_duration(str(info))

        if not self.keep_original:
            speech.audio_stream = bytestream
        speech.converted_stream = bytestream

        speech.converted = True
        speech.converted_params = {'to_format': 'ogg_opus', 'duration_in_seconds': duration_in_seconds, **cmd_params}

        return speech

    def _get_cmd_params(self, speech: Speech, out_bitrate: int, sample_rate: int, filters):
        filters = ' '.join(f'{key}={value}'
                           for key, value in filters.items()
                           if key not in self.excluded_filters)
        return {
            'out_bitrate': out_bitrate or DEFAULT_BITRATE.get(speech.output_format),
            'out_sample_rate': sample_rate or DEFAULT_SAMPLE_RATE.get(speech.output_format),
            'in_params': INPUT_PARAMS.get(speech.output_format, ''),
            'filters': filters and '-filter:a ' + filters
        }

    @staticmethod
    async def _execute(cmd: str, bytestream: bytes):
        proc = await create_subprocess_shell(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate(bytestream)
        logging.debug(f'[{cmd!r} exited with {proc.returncode}]')

        if stderr and not stdout:
            raise RuntimeError(f'[{cmd!r} exited with {proc.returncode}]\n{stderr.decode()}')
        elif not stderr:
            raise RuntimeError(f'[{cmd!r} exited with {proc.returncode}]\n')

        logging.debug(f'[stderr]\n{stderr.decode()}')

        return stdout, stderr.decode()

    @staticmethod
    def _find_duration(s):
        try:
            time = re.findall(r'\d{1,3}:\d{1,3}:\d{1,3}', s)[0]
            hours, minutes, seconds = [i for i in time.split(':')]
            duration_in_seconds = int(hours) * 60 ** 2 + int(minutes) * 60 + round(float(seconds))
        except (ValueError, IndexError):
            duration_in_seconds = None

        return duration_in_seconds
