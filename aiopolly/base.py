import asyncio
import logging
import ssl
from http import HTTPStatus
from typing import Union

import aiohttp
import certifi
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from aiopolly.utils import exceptions
from aiopolly.utils.exceptions import EXCEPTIONS
from .types.content_type import AUDIO_CONTENT_TYPES
from .types.method import ContentType, Method
from .utils import json, case
from .utils.credentials import get_credentials
from .utils.mixins import ContextInstanceMixin

SERVICE_NAME = 'polly'
DEFAULT_REGION = 'eu-central-1'
BASE_URL_TEMPLATE = 'https://{service_name}.{region}.amazonaws.com/v1'

CHARACTERS_HEADER = 'x-amzn-RequestCharacters'

log = logging.getLogger('aiopolly')


class BasePolly(ContextInstanceMixin):

    def __init__(self, credentials, access_key, secret_key, region, loop):
        self.region = region or DEFAULT_REGION
        self.service_name = SERVICE_NAME
        self.base_url = BASE_URL_TEMPLATE.format(service_name=self.service_name, region=self.region)

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
            async with self.session.request(method=request_method, url=url, data=payload_json,
                                            headers=headers) as response:
                result = await self.get_result(url, method, params, payload, response)
        except aiohttp.ClientError as e:
            raise exceptions.AioHTTPException(url=url, cause=e)

        return result

    @staticmethod
    async def get_result(url, method, params, payload, response):
        if response.content_type == ContentType.application_json:
            try:
                result = await response.json()
            except ValueError as e:
                raise exceptions.JSONDecodeException(url=url, response=await response.text(), cause=e)
            result = case.to_snake(result)

        elif response.content_type in AUDIO_CONTENT_TYPES:
            result = {
                'content_type': response.content_type,
                'request_characters': response.headers[CHARACTERS_HEADER],
                'audio_stream': await response.read()
            }
            result.update(case.to_snake(payload))

        elif method.no_data_on_success:
            result = None

        else:
            result = await response.text()

        log.debug('Response for "%s": [%d] "%r"', url, response.status, str(result)[:1000])

        if HTTPStatus.OK <= response.status <= HTTPStatus.IM_USED:
            if not method.no_data_on_success and response.content_type not in method.expected_content_types:
                raise exceptions.ResponseTypeException(url=url, response=result)

            return result

        if response.content_type == ContentType.application_json:
            error_message = result.get('message')
            match_exception = next((exc for exc in EXCEPTIONS if exc.msg in error_message), None) \
                if error_message else None

            if match_exception:
                raise match_exception(error_message, url=url)

        if result is None:
            try:
                result = await response.text()
            except ValueError:
                result = await response.read()

        raise exceptions.PollyAPIException(f'Bad API response [{response.status}]', url=url, response=result)
