import asyncio
from typing import Union, List

from . import api
from .. import config
from .. import types
from ..utils import case, json
from ..utils.converter.base import BaseConverter
from ..utils.payload import generate_params


class Methods:
    DeleteLexicon = types.Method(
        endpoint_template='/v1/lexicons/{LexiconName}',
        request_method='DELETE',
        no_data_on_success=True
    )
    DescribeVoices = types.Method(
        endpoint='/v1/voices',
        request_method='GET',
        expected_content_types=types.ContentType.application_json
    )
    GetLexicon = types.Method(
        endpoint_template='/v1/lexicons/{LexiconName}',
        request_method='GET',
        expected_keys='GetLexicon',
        expected_content_types=types.ContentType.application_json
    )
    GetSpeechSynthesisTask = types.Method(
        endpoint_template='/v1/synthesisTasks/{TaskId}',
        request_method='GET',
        expected_keys='SynthesisTask',
        expected_content_types=types.ContentType.application_json
    )
    ListLexicons = types.Method(
        endpoint='/v1/lexicons',
        request_method='GET',
        expected_content_types=types.ContentType.application_json
    )
    ListSpeechSynthesisTasks = types.Method(
        endpoint='/v1/synthesisTasks',
        request_method='GET',
        expected_content_types=types.ContentType.application_json,
    )
    PutLexicon = types.Method(
        endpoint_template='/v1/lexicons/{LexiconName}',
        request_method='PUT',
        no_data_on_success=True
    )
    StartSpeechSynthesisTask = types.Method(
        endpoint='/v1/synthesisTasks',
        request_method='POST',
        expected_keys='SynthesisTask',
        expected_content_types=types.ContentType.application_json
    )
    SynthesizeSpeech = types.Method(
        endpoint='/v1/speech',
        request_method='POST',
        expected_content_types=types.enums.AUDIO_CONTENT_TYPES
    )


class Polly(api.AmazonAPIClient):
    """
    You can init this class using one of three methods of authorisation:
        1) Provide prepared botocore.credentials.Credentials instance
        2) Use your access and secret keys with optional params,
        3) Provide active botocore.session.Session with credential in it
        4) Create a .aws/credentials file in your system user Home directory with following data
           and init Polly without auth params:
:
            '''
            [default]
                    aws_access_key_id = your_access_key
                    aws_secret_access_key = your_secret_key
            '''
    """

    methods = Methods
    _requested_characters_header = config.CHARACTERS_HEADER

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
                 region: Union[types.Region, str] = types.Region.eu_central_1.value,
                 access_key: str = None,
                 secret_key: str = None,
                 converter: BaseConverter = None,
                 loop: asyncio.AbstractEventLoop = None,
                 **defaults):
        """
        Auth and AWS params:
            :param credentials: instance of botocore.credentials.Credentials class;
            :param session: instance of botocore.session.Session with credentials
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
            :param include_additional_language_codes: value indicating whether to return any bilingual speech that use
                the specified language as an additional language.
        """

        super().__init__(
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            loop=loop
        )

        self.converter = converter

        # Setting default params
        self.defaults = dict(
            voice_id=voice_id,
            output_format=output_format,
            sample_rate=sample_rate,
            speech_mark_type=speech_mark_type,
            text_type=text_type,
            language_code=language_code,
            lexicon_names=lexicon_names,
            speech_mark_types=speech_mark_types,
            output_s3_key_prefix=output_s3_key_prefix,
            output_s3_bucket_name=output_s3_bucket_name,
            sns_topic_arn=sns_topic_arn,
            include_additional_language_codes=include_additional_language_codes
        )
        self.defaults.update(defaults)
        self.defaults = {key: value for key, value in self.defaults.items() if value is not None}

    async def delete_lexicon(self, lexicon_name: str) -> None:
        """
        Deletes the specified pronunciation lexicon stored in an AWS Region.
        A lexicon which has been deleted is not available for speech synthesis,
        nor is it possible to retrieve it using either the GetLexicon or ListLexicon APIs.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_DeleteLexicon.html

        :param lexicon_name: The name of the lexicon to delete. Must be an existing lexicon in the region.
        """
        params = generate_params(lexicon_name=lexicon_name)

        await self.request(self.methods.DeleteLexicon, params=params)

    async def describe_voices(self, include_additional_language_codes: bool = None,
                              language_code: str = None, next_token: str = None) -> types.VoicesList:
        """
        Returns the list of speech that are available for use when requesting speech synthesis.
        Each voice speaks a specified language, is either male or female, and is identified by an ID,
        which is the ASCII version of the voice name.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_DescribeVoices.html

        :param include_additional_language_codes: Boolean value indicating whether to return any bilingual speech
               that use the specified language as an additional language.
        :param language_code: The language identification tag for filtering the list of speech returned.
        :param next_token: An opaque pagination token returned from the previous DescribeVoices operation.
        """
        params = generate_params(**locals(), defaults=self.defaults)
        result, response = await self.request(self.methods.DescribeVoices, params=params)

        return types.VoicesList(**result)

    async def get_lexicon(self, lexicon_name: str) -> types.Lexicon:
        """
        Returns the content of the specified pronunciation lexicon stored in an AWS Region.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_GetLexicon.html

        :param lexicon_name: Name of the lexicon.
        """

        method = self.methods.GetLexicon
        params = generate_params(lexicon_name=lexicon_name)
        result, response = await self.request(method, params=params)
        lexicon_attributes = result[method.lexicon_attributes_key]

        return types.Lexicon(**result[method.lexicon_key], attributes=lexicon_attributes)

    async def get_speech_synthesis_task(self, task_id: str) -> types.SynthesisTask:
        """
        Retrieves a specific SpeechSynthesisTask object based on its TaskID.
        This object contains information about the given speech synthesis task,
        including the status of the task, and a link to the S3 bucket containing the output of the task.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_GetSpeechSynthesisTask.html

        :param task_id: The Amazon Polly generated identifier for a speech synthesis task.
        """

        method = self.methods.GetSpeechSynthesisTask
        params = generate_params(task_id=task_id)
        result, response = await self.request(self.methods.GetSpeechSynthesisTask, params=params)

        return types.SynthesisTask(**result[method.synthesis_task_key])

    async def list_lexicons(self, next_token: str = None) -> types.LexiconsList:
        """
        Returns a list of pronunciation lexicons stored in an AWS Region.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_ListLexicons.html

        :param next_token: An opaque pagination token returned from previous ListLexicons operation.
               If present, indicates where to continue the list of lexicons.
        """

        params = generate_params(next_token=next_token)
        result, response = await self.request(self.methods.ListLexicons, params=params)

        return types.LexiconsList(**result)

    async def list_speech_synthesis_tasks(self, max_results: int = None,
                                          next_token: str = None,
                                          status: str = None) -> types.SynthesisTasksList:
        """
        Returns a list of SpeechSynthesisTask objects ordered by their creation date.
        This operation can filter the tasks by their status, for example,
        allowing users to list only tasks that are completed.

        See: https://docs.aws.amazon.com/en_us/polly/latest/dg/API_ListSpeechSynthesisTasks.html

        :param max_results: Maximum number of speech synthesis tasks returned in a List operation. (1-100)
        :param next_token: The pagination token to use in the next request to continue the listing
        :param status: Status of the speech synthesis tasks returned in a List operation
        """

        params = generate_params(**locals())
        result, response = await self.request(self.methods.ListSpeechSynthesisTasks, params=params)

        return types.SynthesisTasksList(**result)

    async def put_lexicon(self, lexicon_name: str, content: str):
        """
        Stores a pronunciation lexicon in an AWS Region.
        If a lexicon with the same name already exists in the region, it is overwritten by the new lexicon.
        Lexicon operations have eventual consistency, therefore, it might take some time
        before the lexicon is available to the SynthesizeSpeech operation.

        :param lexicon_name: Name of the lexicon. The name must follow the regular express format [0-9A-Za-z]{1,20}.
               That is, the name is a case-sensitive alphanumeric string up to 20 characters long.
        :param content: Content of the PLS lexicon as string data.
        """

        params = generate_params(lexicon_name=lexicon_name)
        payload = generate_params(content=content)

        await self.request(self.methods.PutLexicon, payload=payload, params=params)

    async def start_speech_synthesis_task(self, text: str,
                                          output_s3_key_prefix: str = None,
                                          output_s3_bucket_name: str = None,
                                          voice_id: str = None,
                                          output_format: str = None,
                                          sample_rate: str = None,
                                          speech_mark_types: str = None,
                                          text_type: str = None,
                                          language_code: str = None,
                                          lexicon_names: str = None,
                                          ) -> types.SynthesisTask:
        """
        Allows the creation of an asynchronous synthesis task, by starting a new SpeechSynthesisTask.
        This operation requires all the standard information needed for speech synthesis,
        plus the name of an Amazon S3 bucket for the service to store the output of the synthesis task
        and two optional parameters (OutputS3KeyPrefix and SnsTopicArn). Once the synthesis task is created,
        this operation will return a SpeechSynthesisTask object, which will include an identifier of this task
        as well as the current status.

        :param text: The input text to synthesize.
        :param output_s3_key_prefix: The Amazon S3 key prefix for the output speech file.
        :param output_s3_bucket_name: Amazon S3 bucket name to which the output file will be saved.
        :param voice_id: Voice ID to use for the synthesis.
        :param output_format: The format in which the returned output will be encoded.
        :param sample_rate: The audio frequency specified in Hz.
        :param speech_mark_types: The type of speech marks returned for the input text.
        :param text_type: Specifies whether the input text is plain text or SSML. The default value is plain text.
        :param language_code: Optional language code for the Synthesize Speech request.
        :param lexicon_names: List of one or more pronunciation lexicon names to apply during synthesis
        :return:
        """

        payload = generate_params(**locals(), defaults=self.defaults)
        result, response = await self.request(self.methods.StartSpeechSynthesisTask, payload=payload)
        return types.SynthesisTask(**result)

    async def synthesize_speech(self, text: str,
                                voice_id: str = None,
                                output_format: Union[types.AudioFormat, str] = None,
                                sample_rate: str = None,
                                speech_mark_types: List[Union[types.SpeechMarkTypes, str]] = None,
                                text_type: Union[types.TextType, str] = None,
                                language_code: Union[types.LanguageCode, str] = None,
                                lexicon_names: list = None,
                                auto_convert: bool = None,
                                **converter_params
                                ) -> Union[types.Speech, types.SpeechMarksList]:
        """
        Synthesizes UTF-8 input, plain text or SSML, to a stream of bytes. SSML input must be valid, well-formed SSML.
        Some alphabets might not be available with all the speech
        (for example, Cyrillic might not be read at all by English speech) unless phoneme mapping is used.

        :param text: Input text to synthesize.
        :param voice_id: Voice ID to use for the synthesis.
        :param output_format: The format in which the returned output will be encoded.
        :param sample_rate: The audio frequency specified in Hz.
        :param speech_mark_types: The type of speech marks returned for the input text.
        :param text_type: Specifies whether the input text is plain text or SSML. The default value is plain text.
        :param language_code: Optional language code for the Synthesize Speech request.
        :param lexicon_names: List of one or more pronunciation lexicon names to apply during synthesis

        :param auto_convert: param indicate whether speech will be auto converted after synthesis
        :param converter_params: params which will be placed in self.converter.convert method
        """
        payload = generate_params(**locals(), defaults=self.defaults, use_camel=False,
                                  exclude={'auto_convert', 'converter_params'})

        content, response = await self.request(self.methods.SynthesizeSpeech, payload=case.to_camel(payload))

        if response.content_type == types.ContentType.audio_json:
            return types.SpeechMarksList(
                speech_marks=[json.loads(line) for line in content.split(b'\n')[:-1]]
            )

        speech = types.Speech(
            content_type=response.content_type,
            request_characters=response.headers[self._requested_characters_header],
            audio_stream=content,
            **payload
        )

        if self.converter and (auto_convert or self.converter.auto_convert and auto_convert is not False):
            return await self.converter.convert(speech, **converter_params)
        elif auto_convert or converter_params:
            raise RuntimeError(f'Cannot find converter in {self}, to use it please specify one')

        return speech
