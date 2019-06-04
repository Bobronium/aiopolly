import asyncio
from typing import Union, List

import botocore
from botocore.credentials import Credentials

from . import types
from .base import BasePolly
from .types.content_type import AUDIO_CONTENT_TYPES
from .utils.lexicon import LexiconTemplate
from .utils.payload import generate_params

TRUST_API_RESPONSES = True


class Methods:
    DeleteLexicon = types.Method(
        endpoint_template='lexicons/{LexiconName}',
        request_method='delete',
        no_data_on_success=True
    )
    DescribeVoices = types.Method(
        endpoint='voices',
        request_method='get',
        expected_content_types=types.ContentType.application_json
    )
    GetLexicon = types.Method(
        endpoint_template='lexicons/{LexiconName}',
        request_method='get',
        expected_keys='GetLexicon',
        expected_content_types=types.ContentType.application_json
    )
    GetSpeechSynthesisTask = types.Method(
        endpoint_template='synthesisTasks/{TaskId}',
        request_method='get',
        expected_keys='SynthesisTask',
        expected_content_types=types.ContentType.application_json
    )
    ListLexicons = types.Method(
        endpoint='lexicons',
        request_method='get',
        expected_content_types=types.ContentType.application_json
    )
    ListSpeechSynthesisTasks = types.Method(
        endpoint='synthesisTasks',
        request_method='get',
        expected_content_types=types.ContentType.application_json,
    )
    PutLexicon = types.Method(
        endpoint_template='lexicons/{LexiconName}',
        request_method='put',
        no_data_on_success=True
    )
    StartSpeechSynthesisTask = types.Method(
        endpoint='synthesisTasks',
        request_method='post',
        expected_keys='SynthesisTask',
        expected_content_types=types.ContentType.application_json
    )
    SynthesizeSpeech = types.Method(
        endpoint='speech',
        request_method='post',
        expected_content_types=AUDIO_CONTENT_TYPES
    )


class Polly(BasePolly):
    """
    You can init this class using one of three methods of authorisation:
        1) Provide prepared botocore.credentials.Credentials instance
        2) Use your access and secret keys with optional params,
        3) Create a .aws/credentials file in your system user Home directory with following data:
            '''
            [default]
                    aws_access_key_id = your_access_key
                    aws_secret_access_key = your_secret_key
            '''
    """

    methods = Methods
    trust_api_responses = TRUST_API_RESPONSES

    def __init__(self,
                 voice_id: str = None,
                 output_format: str = None,
                 sample_rate: str = None,
                 speech_mark_type: str = None,
                 text_type: Union[List[str], str] = None,
                 language_code: str = None,
                 lexicon_names: List[str] = None,
                 speech_mark_types: List[str] = None,
                 output_s3_key_prefix: str = None,
                 output_s3_bucket_name: str = None,
                 sns_topic_arn: str = None,
                 include_additional_language_codes: bool = False,
                 credentials: botocore.credentials.Credentials = None,
                 region: str = None,
                 access_key: str = None,
                 secret_key: str = None,
                 loop: asyncio.AbstractEventLoop = None,
                 **defaults):
        """
        Auth and AWS params:
            :param credentials: instance of botocore.credentials.Credentials class;
            :param access_key: AWS access key, requires :param secret_key;
            :param secret_key: AWS secret key, requires :param access_key;
            :param region: AWS server region, default is 'eu-central-1'. For available regions see:
                https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html

        Default API params, used when method params remain empty:
            For original docs see: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_Operations.html

            :param voice_id: speech voice_id;
            :param output_format: the format in which the returned output will be encoded;
            :param sample_rate: audio frequency specified in Hz;
            :param lexicon_names: list of one or more pronunciation lexicon names;
            :param text_type: specifies whether the input text is plain text or SSML;
            :param language_code: optional language code for the Synthesize Speech request.
            :param output_s3_key_prefix: the Amazon S3 key prefix for the output speech file;
            :param output_s3_bucket_name: amazon S3 bucket name to which the output file will be saved.
            :param sns_topic_arn: ARN for the SNS topic for providing status notification for a speech synthesis task.
            :param include_additional_language_codes: value indicating whether to return any bilingual voices that use
                the specified language as an additional language.
        """

        super().__init__(credentials, access_key, secret_key, region, loop)

        # Setting default params
        self.voice_id = voice_id
        self.output_format = output_format
        self.sample_rate = sample_rate
        self.speech_mark_type = speech_mark_type
        self.text_type = text_type
        self.language_code = language_code
        self.lexicon_names = lexicon_names
        self.speech_mark_types = speech_mark_types
        self.output_s3_key_prefix = output_s3_key_prefix
        self.output_s3_bucket_name = output_s3_bucket_name
        self.sns_topic_arn = sns_topic_arn
        self.include_additional_language_codes = include_additional_language_codes

        for k, v in defaults.items():
            setattr(self, k, v)

    async def delete_lexicon(self, lexicon_name: str) -> None:
        params = generate_params(lexicon_name=lexicon_name)

        await self.request(self.methods.DeleteLexicon, params=params)

    async def describe_voices(self, include_additional_language_codes: bool = None,
                              language_code: str = None, next_token: str = None) -> types.VoicesList:
        params = generate_params(**locals(), defaults=self.__dict__)
        result = await self.request(self.methods.DescribeVoices, params=params)

        return types.VoicesList(**result)

    async def get_lexicon(self, lexicon_name: str) -> types.Lexicon:
        method = self.methods.GetLexicon
        params = generate_params(lexicon_name=lexicon_name)
        result = await self.request(method, params=params)
        lexicon_attributes = result[method.lexicon_attributes_key]

        return types.Lexicon(**result[method.lexicon_key], attributes=lexicon_attributes)

    async def get_speech_synthesis_task(self, task_id: str) -> types.SynthesisTask:
        method = self.methods.GetSpeechSynthesisTask
        params = generate_params(task_id=task_id)
        result = await self.request(self.methods.GetSpeechSynthesisTask, params=params)

        return types.SynthesisTask(**result[method.synthesis_task_key])

    async def list_lexicons(self, next_token: str = None) -> types.LexiconsList:
        params = generate_params(next_token=next_token)
        result = await self.request(self.methods.ListLexicons, params=params)

        return types.LexiconsList(**result)

    async def list_speech_synthesis_tasks(self, max_results: int = None,
                                          next_token: str = None,
                                          status: str = None) -> types.SynthesisTasksList:
        params = generate_params(**locals())
        result = await self.request(self.methods.ListSpeechSynthesisTasks, params=params)

        return types.SynthesisTasksList(**result)

    async def put_lexicon(self, lexicon_name: str, content: Union[str, LexiconTemplate]):
        if hasattr(content, 'to_str'):
            content = content.to_str()

        params = generate_params(lexicon_name=lexicon_name)
        payload = generate_params(content=content)

        await self.request(self.methods.PutLexicon, payload=payload, params=params)

    async def start_speech_synthesis_task(self, text: str,
                                          output_s3_key_prefix: str = None,
                                          output_s3_bucket_name: str = None,
                                          voice_id: str = None,
                                          output_format: str = None,
                                          sample_rate: str = None,
                                          speech_mark_type: str = None,
                                          text_type: str = None,
                                          language_code: str = None,
                                          lexicon_names: str = None,
                                          ) -> types.SynthesisTask:
        payload = generate_params(**locals(), defaults=self.__dict__)
        result = await self.request(self.methods.StartSpeechSynthesisTask, payload=payload)
        return types.SynthesisTask(**result)

    async def synthesize_speech(self, text: str,
                                voice_id: str = None,
                                output_format: str = None,
                                sample_rate: str = None,
                                speech_mark_type: str = None,
                                text_type: str = None,
                                language_code: str = None,
                                lexicon_names: list = None,
                                ) -> types.Speech:
        payload = generate_params(**locals(), defaults=self.__dict__)
        result = await self.request(self.methods.SynthesizeSpeech, payload=payload)

        return types.Speech(**result)
