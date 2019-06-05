import re
from typing import ClassVar, Union

from aiohttp import ClientResponse

exception_pattern = re.compile(r'([A-Z][a-z0-9]+){2,}')

PolyExceptionType = ClassVar['PollyAPIException']


def get_exception(exception_header: str, response_code: int, message: str = None) -> PolyExceptionType:
    """
    Exception header example:
    'UnrecognizedClientException:http://internal.amazon.com/coral/com.amazon.coral.service/'
    'UnauthorizedException'
    """
    # Trying to find and return existing exception
    if message:
        match_exception = next((exc for exc in EXCEPTIONS if exc.msg in message), None)
        if match_exception:
            return match_exception

    # Creating new exception basing on response_code
    __bases__ = next((exc for exc in BASE_EXCEPTIONS if exc.http_code == response_code), PollyAPIException)
    exc_name = __bases__.__name__

    # Trying to resolve AWS exception name from exception header if it exists
    if exception_header:
        try:
            exc_name, _ = exception_header.split(':')
        except ValueError:
            match = exception_pattern.match(exception_header)
            exc_name = match.group() if match else exc_name

    return type(exc_name, (__bases__,), {'msg': message or __bases__.msg})


class BasePollyException(Exception):
    msg = 'Exception occurred'
    http_code = 400

    def __init__(self,
                 message: str = None,
                 url: str = None,
                 payload: dict = None,
                 response: ClientResponse = None,
                 result: Union[dict, str, bytes, ClientResponse] = None,
                 cause: ClassVar[Exception] = None):

        if not message:
            message = self.msg
        if cause is not None:
            message += f'\n\nCaused by: {cause.__class__.__name__}: {cause}'
        if url is not None:
            message += f'\n\nRequest url: {url}'
        if payload is not None:
            message += f'\n\nPayload: {payload}'
        if result is not None:
            message += f'\n\nResult: {result}'
        if response is not None:
            message += f'\n\nResponse: {response}'

        super().__init__(message)
        self.url = url
        self.payload = payload
        self.response = response
        self.cause = cause


class AioHTTPException(BasePollyException):
    msg = 'aiohttp throws exception:'


class JSONDecodeException(BasePollyException):
    msg = 'Unable to decode JSON'


class ResponseTypeException(BasePollyException):
    msg = 'Server returned response with unexpected content type'


class ResponseValueException(BasePollyException):
    msg = 'API send response with unexpected values'


class PollyAPIException(BasePollyException):
    msg = 'API returned exception'


class BadRequestException(PollyAPIException):
    http_code = 400


class AccessDeniedException(PollyAPIException):
    http_code = 403


class NotFoundException(PollyAPIException):
    http_code = 404


class ConflictException(PollyAPIException):
    http_code = 409


class LimitExceededException(PollyAPIException):
    http_code = 429


class TooManyRequestsException(PollyAPIException):
    http_code = 429


class ServiceFailureException(PollyAPIException):
    msg = 'An unknown condition has caused a service failure.'
    http_code: int = 500


class ServiceUnavailableException(PollyAPIException):
    http_code = 503


class BadGatewayException(PollyAPIException):
    http_code = 502


class EndpointRequestTimedOutException(PollyAPIException):
    http_code = 504


class InvalidS3BucketException(BadRequestException):
    msg = 'The provided Amazon S3 bucket name is invalid.'


class InvalidS3KeyException(BadRequestException):
    msg = 'The provided Amazon S3 key prefix is invalid. Please provide a valid S3 object key name.'


class InvalidSampleRateException(BadRequestException):
    msg = 'The specified sample rate is not valid.'


class InvalidSnsTopicArnException(BadRequestException):
    msg = 'The provided SNS topic ARN is invalid. Please provide a valid SNS topic ARN and try again.'


class InvalidSSMLException(BadRequestException):
    msg = 'The SSML you provided is invalid.'


class LanguageNotSupportedException(BadRequestException):
    msg = 'The language specified is not currently supported by Amazon Polly in this capacity.'


class LexiconNotFoundException(NotFoundException):
    msg = 'Amazon Polly can\'t find the specified lexicon.'


class MarksNotSupportedForFormatException(BadRequestException):
    msg = 'Speech marks are not supported for the OutputFormat selected.'


class SSMLMarksNotSupportedForTextTypeException(BadRequestException):
    msg = 'SSML speech marks are not supported for plain text-type input.'


class TextLengthExceededException(BadRequestException):
    msg = 'The value of the "Text" parameter is longer than the accepted limits.'


class InvalidTaskIdException(BadRequestException):
    msg = 'The provided Task ID is not valid. Please provide a valid Task ID and try again.'


class SynthesisTaskNotFoundException(BadRequestException):
    msg = 'The Speech Synthesis task with requested Task ID cannot be found.'


class InvalidNextTokenException(BadRequestException):
    msg = 'The NextToken is invalid. Verify that it\'s spelled correctly, and then try again.'


class InvalidLexiconException(BadRequestException):
    msg = 'Amazon Polly can\'t find the specified lexicon.'


class LexiconSizeExceededException(BadRequestException):
    msg = 'The maximum size of the specified lexicon would be exceeded by this operation.'


class MaxLexemeLengthExceededException(BadRequestException):
    msg = 'The maximum size of the lexeme would be exceeded by this operation.'


class MaxLexiconsNumberExceededException(BadRequestException):
    msg = 'The maximum number of lexicons would be exceeded by this operation.'


class UnsupportedPlsAlphabetException(BadRequestException):
    msg = 'The alphabet specified by the lexicon is not a supported alphabet. Valid values are x-sampa and ipa.'


class UnsupportedPlsLanguageException(BadRequestException):
    msg = 'The language specified in the lexicon is unsupported.'


class SignatureDoesNotMatchException(PollyAPIException):
    msg = 'The request signature we calculated does not match the signature you provided.'


class ValidationErrorExceptions(PollyAPIException):
    msg = 'validation error detected'


class MissingAuthTokenException(PollyAPIException):
    msg = 'Missing Authentication Token'


class InvalidPLSLexiconException(BadRequestException):
    msg = 'Invalid PLS Lexicon'


class UnsupportedPLSLanguageException(BadRequestException):
    msg = 'Unsupported PLS language'


class InvalidSSMLRequestException(BadRequestException):
    msg = 'Invalid SSML request'


EXCEPTIONS = set()
for k, v in dict(globals()).items():
    try:
        if issubclass(v, BasePollyException):
            EXCEPTIONS.add(v)
    except TypeError:
        pass

BASE_EXCEPTIONS = (
    BadRequestException,
    AccessDeniedException,
    NotFoundException,
    ConflictException,
    LimitExceededException,
    TooManyRequestsException,
    BadGatewayException,
    ServiceUnavailableException,
    EndpointRequestTimedOutException
)
