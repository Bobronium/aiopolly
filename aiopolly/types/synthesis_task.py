import datetime
from enum import Enum
from typing import List

from .base import BasePollyObject
from .content_type import AudioFormat

__all__ = ['SynthesisTask', 'SynthesisTasksList', 'SynthesisTaskStatus']


class SynthesisTaskStatus(str, Enum):
    scheduled = 'scheduled'
    in_progress = 'inProgress'
    completed = 'completed'
    failed = 'failed'


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
        for synthesis_task in self.synthesis_tasks:
            yield synthesis_task

    def __getitem__(self, item):
        return self.synthesis_tasks[item]
