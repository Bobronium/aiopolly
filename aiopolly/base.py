import asyncio
import logging
import ssl
from http import HTTPStatus
from typing import Union

import aiohttp
import certifi
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from .types import ContentType
from .types.enums import AUDIO_CONTENT_TYPES
from .types.method import Method
from .types.speech import SPEECH_CONTENT_TYPE_KEY, SPEECH_REQUEST_CHARACTERS_KEY, SPEECH_AUDIO_STREAM_KEY
from .utils import json, case
from .utils.credentials import get_credentials
from .utils.exceptions import get_exception, ResponseTypeException, JSONDecodeException, AioHTTPException
from .utils.mixins import ContextInstanceMixin

log = logging.getLogger('aiopolly')

SERVICE_NAME = 'polly'
DEFAULT_REGION = 'eu-central-1'
BASE_URL_TEMPLATE = 'https://{service_name}.{region}.amazonaws.com/v1'

CHARACTERS_HEADER = 'x-amzn-RequestCharacters'
EXCEPTION_HEADER = 'x-amzn-ErrorType'

TRUST_API_RESPONSES = False
RETURN_RAW_RESPONSE = False
LOAD_STREAM_ENABLED = True


class BaseApiClient(ContextInstanceMixin):
    _service_name = SERVICE_NAME
    _default_region = DEFAULT_REGION
    _base_url_template = BASE_URL_TEMPLATE

    _trust_api_responses = TRUST_API_RESPONSES
    _return_raw_response = RETURN_RAW_RESPONSE
    _load_stream_enabled = LOAD_STREAM_ENABLED

    def __init__(self, credentials, access_key, secret_key, region, loop):
        self.region = region or self._default_region
        self.base_url = self._base_url_template.format(service_name=self._service_name, region=self.region)

        self.__credentials = get_credentials(credentials, access_key, secret_key)
        self.__signer = SigV4Auth(credentials=self.__credentials, service_name=SERVICE_NAME, region_name=self.region)

        if not loop:
            loop = asyncio.get_event_loop()
        self.loop = loop

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context, loop=self.loop)
        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop, json_serialize=json.dumps)

        self.set_current(self)

    def __get_signed_headers(self, url: str, request_method: str = None, payload: str = None):
        request = AWSRequest(method=request_method, url=url, data=payload)
        self.__signer.add_auth(request)

        return dict(request.headers.items())

    async def request(self, method: Method, payload: dict = None, params: dict = None) -> Union[dict, str, None]:
        url = method.get_url(self.base_url, params)
        request_method = method.request_method

        if payload is not None:
            payload_json = json.dumps(payload)
        else:
            payload_json = None

        headers = self.__get_signed_headers(url, request_method, payload_json)

        try:
            async with self.session.request(
                    method=request_method, url=url, data=payload_json, headers=headers) as response:
                result = await self.get_result(url, method, payload, response)
        except aiohttp.ClientError as e:
            raise AioHTTPException(url=url, payload=payload, cause=e)

        return result

    async def get_result(self, url: str, method: Method, payload: dict, response: aiohttp.ClientResponse):
        if self._return_raw_response:
            return response

        if response.content_type == ContentType.application_json:
            result = self.get_json(url, payload, response)

        elif response.content_type == ContentType.audio_json:
            result = self.get_speech_marks(response)

        elif response.content_type in AUDIO_CONTENT_TYPES:
            result = self.get_speech(response, payload)

        else:
            result = response

        log.debug('Response for "%s": [%d] "%r"', url, response.status, str(result)[:3000])

        if response.status not in range(HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            self.raise_api_exception(url, payload, response, result)

        if not method.no_data_on_success and response.content_type not in method.expected_content_types:
            raise ResponseTypeException(url=url, payload=payload, response=response, result=result)

        return result

    def get_speech(self, response, payload):
        result = {
            SPEECH_CONTENT_TYPE_KEY: response.content_type,
            SPEECH_REQUEST_CHARACTERS_KEY: response.headers[CHARACTERS_HEADER],
            SPEECH_AUDIO_STREAM_KEY: await response.read() if self._load_stream_enabled else response
        }
        result.update(case.to_snake(payload))
        return result

    @staticmethod
    def get_speech_marks(response):
        result = await response.content.read()
        return [json.loads(line) for line in result.split(b'\n')[:-1]]

    @staticmethod
    def raise_api_exception(url, payload, response, result):
        if response.content_type == ContentType.application_json:
            error_message = result.get('message')
        elif result:
            error_message = result
        else:
            try:
                error_message = await response.text()
            except ValueError:
                error_message = await response.read()

        api_exception = get_exception(
            response.headers.get(EXCEPTION_HEADER),
            response.status,
            error_message
        )
        raise api_exception(url=url, payload=payload, result=result, response=response)

    @staticmethod
    def get_json(url, payload, response):
        try:
            result = await response.json()
        except ValueError as e:
            raise JSONDecodeException(url=url, payload=payload, response=await response.text(), cause=e)
        return case.to_snake(result)
