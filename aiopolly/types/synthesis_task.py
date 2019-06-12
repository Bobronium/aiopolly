import datetime
from typing import List

from .base import BasePollyObject
from .enums import AudioFormat

__all__ = ['SynthesisTask', 'SynthesisTasksList']


class SynthesisTask(BasePollyObject):
    creation_time: datetime.datetime
    language_code: str
    lexicon_names: List[str]
    output_format: AudioFormat
    output_uri: str
    request_characters: int
    sample_rate: str
    sns_topic_arn: str
    speech_mark_types: List[str]
    task_id: str
    task_status: str
    task_status_reason: str
    text_type: str
    voice_id: str


class SynthesisTasksList(BasePollyObject):
    synthesis_tasks: List[SynthesisTask]
    next_token: str = None

    def __iter__(self):
        return iter(self.synthesis_tasks)

    def __getitem__(self, item):
        return self.synthesis_tasks[item]
