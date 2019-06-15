import re
from typing import ClassVar, Union

from aiohttp import ClientResponse

exception_pattern = re.compile(r'([A-Z][a-z0-9]+){2,}')

PolyExceptionType = ClassVar['PollyAPIException']


class BasePollyException(Exception):
    msg = 'Exception occurred'
    match = None

    def __init__(self,
                 message: str = None,
                 url: str = None,
                 payload: dict = None,
                 response: ClientResponse = None,
                 content: Union[dict, str, bytes, ClientResponse] = None,
                 cause: ClassVar[Exception] = None):

        if not message:
            message = self.msg
        if cause is not None:
            message += f'\n\nCaused by: {cause.__class__.__name__}: {cause}'
        if url is not None:
            message += f'\n\nRequest url: {url}'
        if payload is not None:
            message += f'\n\nPayload: {payload}'
        if response is not None:
            message += f'\n\nResponse: {response}'
        if content is not None:
            message += f'\n\nContent: {content}'

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
    msg = match = 'API send response with unexpected values'


class PollyAPIException(BasePollyException):
    msg = 'API returned exception'


class BadRequestException(PollyAPIException):
    http_code = 400
    retry = False


class AccessDeniedException(PollyAPIException):
    http_code = 403
    retry = False


class NotFoundException(PollyAPIException):
    http_code = 404
    retry = False


class ConflictException(PollyAPIException):
    http_code = 409
    retry = False


class LimitExceededException(PollyAPIException):
    http_code = 429
    retry = False


class TooManyRequestsException(PollyAPIException):
    http_code = 429
    retry = False


class ServiceFailureException(PollyAPIException):
    msg = match = 'An unknown condition has caused a service failure.'
    http_code: int = 500
    retry = True


class ServiceUnavailableException(PollyAPIException):
    http_code = 503
    retry = True


class BadGatewayException(PollyAPIException):
    http_code = 502
    retry = True


class EndpointRequestTimedOutException(PollyAPIException):
    http_code = 504
    retry = True


class InvalidS3BucketException(BadRequestException):
    msg = match = 'The provided Amazon S3 bucket name is invalid.'


class InvalidS3KeyException(BadRequestException):
    msg = match = 'The provided Amazon S3 key prefix is invalid. Please provide a valid S3 object key name.'


class InvalidSampleRateException(BadRequestException):
    msg = match = 'The specified sample rate is not valid.'


class InvalidSnsTopicArnException(BadRequestException):
    msg = match = 'The provided SNS topic ARN is invalid. Please provide a valid SNS topic ARN and try again.'


class InvalidSSMLException(BadRequestException):
    msg = match = 'The SSML you provided is invalid.'


class LanguageNotSupportedException(BadRequestException):
    msg = match = 'The language specified is not currently supported by Amazon Polly in this capacity.'


class LexiconNotFoundException(NotFoundException):
    msg = match = 'Amazon Polly can\'t find the specified lexicon.'


class MarksNotSupportedForFormatException(BadRequestException):
    msg = match = 'Speech marks are not supported for the OutputFormat selected.'


class SSMLMarksNotSupportedForTextTypeException(BadRequestException):
    msg = match = 'SSML speech marks are not supported for plain text-type input.'


class TextLengthExceededException(BadRequestException):
    msg = match = 'Maximum text length has been exceeded'


class InvalidTaskIdException(BadRequestException):
    msg = match = 'The provided Task ID is not valid. Please provide a valid Task ID and try again.'


class SynthesisTaskNotFoundException(BadRequestException):
    msg = match = 'The Speech Synthesis task with requested Task ID cannot be found.'


class InvalidNextTokenException(BadRequestException):
    msg = match = 'The NextToken is invalid. Verify that it\'s spelled correctly, and then try again.'


class InvalidLexiconException(BadRequestException):
    msg = match = 'Amazon Polly can\'t find the specified lexicon.'


class LexiconSizeExceededException(BadRequestException):
    msg = match = 'The maximum size of the specified lexicon would be exceeded by this operation.'


class MaxLexemeLengthExceededException(BadRequestException):
    msg = match = 'The maximum size of the lexeme would be exceeded by this operation.'


class MaxLexiconsNumberExceededException(BadRequestException):
    msg = match = 'The maximum number of lexicons would be exceeded by this operation.'


class UnsupportedPLSAlphabetException(BadRequestException):
    msg = match = 'The alphabet specified by the lexicon is not a supported alphabet. Valid values are x-sampa and ipa.'


class UnsupportedPLSLanguageException(BadRequestException):
    msg = match = 'Unsupported PLS language'


class SignatureDoesNotMatchException(PollyAPIException):
    msg = match = 'The request signature we calculated does not match the signature you provided.'


class ValidationErrorExceptions(PollyAPIException):
    msg = match = 'validation error detected'


class MissingAuthTokenException(PollyAPIException):
    msg = match = 'Missing Authentication Token'


class InvalidPLSLexiconException(BadRequestException):
    msg = match = 'Invalid PLS Lexicon'


class InvalidSSMLRequestException(BadRequestException):
    msg = match = 'Invalid SSML request'


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


def get_exception(exception_header: str, response_code: int, message: str = None) -> PolyExceptionType:
    """
    Exception header example:
    'UnrecognizedClientException:http://internal.amazon.com/coral/com.amazon.coral.service/'
    'UnauthorizedException'
    """
    # Trying to find and return existing exception
    if message:
        match_exception = next((exc for exc in EXCEPTIONS if exc.match and exc.match in message), None)
        if match_exception:
            return match_exception

    # Trying to resolve AWS exception name from exception header if it exists
    exc_name = None
    if exception_header:
        match = exception_pattern.match(exception_header)
        if match:
            exc_name = match.group()

            # Last try to find existing exception by its name (in case match text has been changed)
            match_exception = next((exc for exc in EXCEPTIONS if exc.__name__.lower() == exc_name.lower()), None)
            if match_exception:
                return match_exception

    # If exception not found, creating new one basing on response_code
    __bases__ = next((exc for exc in BASE_EXCEPTIONS if exc.http_code == response_code), PollyAPIException)

    return type(
        exc_name or __bases__.__name__,
        (__bases__,),
        {'msg': message or __bases__.msg}
    )
