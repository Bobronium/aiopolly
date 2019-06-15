import abc

from ...types import Speech

__all__ = ['BaseConverter']


class BaseConverter(abc.ABC):
    auto_convert: bool
    keep_original: bool

    @abc.abstractmethod
    async def convert(self, speech: Speech, **kwargs) -> Speech:
        """
        Example:
            async def convert(self, speech: Speech, to_format=None, out_bitrate=None) -> Speech:
                converted_audio, duration, info = self._convert_audio(speech.audio_stream, to_format, out_bitrate)

                if not self.keep_original:
                    speech.audio_stream = converted_audio
                speech.converted_stream = converted_audio

                speech.converted = True
                speech.converted_params = {
                    'to_format': to_format or self.to_format
                    'out_bitrate': out_bitrate or self.bitrate
                    'duration_in_seconds': duration
                    'info': info
                }
                return speech

        :param speech: speech which needs to be converted
        :param kwargs: any convert params
        :return: Speech with additional params and converted audio
        """
        pass
