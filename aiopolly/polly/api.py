import asyncio
import logging
import ssl
from http import HTTPStatus
from typing import Union, Tuple, Optional

import aiohttp
import certifi
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from .. import config
from ..types import ContentType
from ..types.method import Method
from ..utils import json, case
from ..utils.credentials import get_credentials
from ..utils.exceptions import get_exception, ResponseTypeException, JSONDecodeException, AioHTTPException
from ..utils.mixins import ContextInstanceMixin

log = logging.getLogger('aiopolly')


class AmazonAPIClient(ContextInstanceMixin):
    _service_name = config.SERVICE_NAME
    _base_url_template = config.BASE_URL_TEMPLATE

    _exception_header = config.EXCEPTION_HEADER

    _trust_api_responses = config.TRUST_API_RESPONSES
    _convert_to_snake = config.CONVERT_TO_SNAKE_CASE

    def __init__(self, region: str,
                 access_key: Optional[str],
                 secret_key: Optional[str],
                 loop: Optional[asyncio.AbstractEventLoop]):

        self.region = region

        self.base_url = self._base_url_template.format(
            service_name=self._service_name,
            region=self.region,
        )

        self.__signer = SigV4Auth(
            credentials=get_credentials(access_key, secret_key),
            service_name=self._service_name,
            region_name=self.region
        )

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

    async def request(self, method: Method, payload: dict = None, params: dict = None
                      ) -> Tuple[Union[dict, bytes, None], aiohttp.ClientResponse]:

        log.debug('Preparing request to API. method: %s, paylod: %s, params: %s', method, payload, params)

        url = method.get_url(self.base_url, params)
        request_method = method.request_method

        if payload is not None:
            payload_json = json.dumps(payload)
        else:
            payload_json = None

        headers = self.__get_signed_headers(url, request_method, payload_json)

        try:
            log.debug('Sending request to API "%s": [%s]', url, payload_json)
            async with self.session.request(method=request_method,
                                            url=url,
                                            data=payload_json,
                                            headers=headers) as response:
                content = await self.get_content(url, method, payload, response)
        except aiohttp.ClientError as e:
            raise AioHTTPException(url=url, payload=payload, cause=e)

        return content, response

    async def get_content(self, url: str, method: Method, payload: dict, response: aiohttp.ClientResponse):
        log.debug('Getting content for "%s": [%d]', url, response.status)

        if response.content_type == ContentType.application_json:
            content = await self.get_json(url, payload, response)
        elif response.content_type == ContentType.audio_json:
            content = await response.content.read()
        else:
            content = await response.read()

        log.debug('Content for "%s": [%d] "%r"', url, response.status, content)

        if response.status not in range(HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            await self.raise_api_exception(url, payload, response, content)
        if method.no_data_on_success:
            return content
        elif response.content_type not in method.expected_content_types:
            raise ResponseTypeException(url=url, payload=payload, response=response, content=content)

        return content

    async def raise_api_exception(self, url: str, payload: Union[dict, None], response: aiohttp.ClientResponse,
                                  content):
        if response.content_type == ContentType.application_json:
            error_message = content.get('message')
        elif content:
            error_message = content
        else:
            try:
                error_message = await response.text()
            except ValueError:
                error_message = await response.read()

        api_exception = get_exception(
            response.headers.get(self._exception_header),
            response.status,
            error_message
        )
        raise api_exception(url=url, payload=payload, content=content, response=response)

    async def get_json(self, url: str, payload: Union[dict, None], response: aiohttp.ClientResponse) -> dict:
        try:
            result = await response.json()
        except ValueError as e:
            raise JSONDecodeException(url=url, payload=payload, response=response, cause=e)
        if self._convert_to_snake:
            return case.to_snake(result)
