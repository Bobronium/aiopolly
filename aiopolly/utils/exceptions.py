from typing import ClassVar, Union


class BasePollyException(Exception):
    msg = 'Exception occurred'

    def __init__(self,
                 message: str = None,
                 url: str = None,
                 response: Union[dict, str] = None,
                 cause: ClassVar[Exception] = None):

        if not message:
            message = self.msg
        if url:
            message += f', request: {url}'
            if response:
                message += f', response: {response}'
        if cause:
            message += f'. Caused by {cause.__class__.__name__}: {cause}'

        super().__init__(message)
        self.url = url
        self.response = response
        self.cause = cause


class AioHTTPException(BasePollyException):
    pass


class PollyAPIException(BasePollyException):
    pass


class JSONDecodeException(BasePollyException):
    pass


class ResponseTypeException(BasePollyException):
    pass


class InvalidS3BucketException(BasePollyException):
    msg = 'The provided Amazon S3 bucket name is invalid.'
    http_code: int = 400


class InvalidS3KeyException(BasePollyException):
    msg = 'The provided Amazon S3 key prefix is invalid. Please provide a valid S3 object key name.'
    http_code: int = 400


class InvalidSampleRateException(BasePollyException):
    msg = 'The specified sample rate is not valid.'
    http_code: int = 400


class InvalidSnsTopicArnException(BasePollyException):
    msg = 'The provided SNS topic ARN is invalid. Please provide a valid SNS topic ARN and try again.'
    http_code: int = 400


class InvalidSSMLException(BasePollyException):
    msg = 'The SSML you provided is invalid.'
    http_code: int = 400


class LanguageNotSupportedException(BasePollyException):
    msg = 'The language specified is not currently supported by Amazon Polly in this capacity.'
    http_code: int = 400


class LexiconNotFoundException(BasePollyException):
    msg = 'Amazon Polly can\'t find the specified lexicon.'
    http_code: int = 404


class MarksNotSupportedForFormatException(BasePollyException):
    msg = 'Speech marks are not supported for the OutputFormat selected.'
    http_code: int = 400


class ServiceFailureException(BasePollyException):
    msg = 'An unknown condition has caused a service failure.'
    http_code: int = 500


class SSMLMarksNotSupportedForTextTypeException(BasePollyException):
    msg = 'SSML speech marks are not supported for plain text-type input.'
    http_code: int = 400


class TextLengthExceededException(BasePollyException):
    msg = 'The value of the "Text" parameter is longer than the accepted limits.'
    http_code: int = 400


class InvalidTaskIdException(BasePollyException):
    msg = 'The provided Task ID is not valid. Please provide a valid Task ID and try again.'
    http_code: int = 400


class SynthesisTaskNotFoundException(BasePollyException):
    msg = 'The Speech Synthesis task with requested Task ID cannot be found.'
    http_code: int = 400


class InvalidNextTokenException(BasePollyException):
    msg = 'The NextToken is invalid. Verify that it\'s spelled correctly, and then try again.'
    http_code: int = 400


class InvalidLexiconException(BasePollyException):
    msg = 'Amazon Polly can\'t find the specified lexicon.'
    http_code: int = 400


class LexiconSizeExceededException(BasePollyException):
    msg = 'The maximum size of the specified lexicon would be exceeded by this operation.'
    http_code: int = 400


class MaxLexemeLengthExceededException(BasePollyException):
    msg = 'The maximum size of the lexeme would be exceeded by this operation.'
    http_code: int = 400


class MaxLexiconsNumberExceededException(BasePollyException):
    msg = 'The maximum number of lexicons would be exceeded by this operation.'
    http_code: int = 400


class UnsupportedPlsAlphabetException(BasePollyException):
    msg = 'The alphabet specified by the lexicon is not a supported alphabet. Valid values are x-sampa and ipa.'
    http_code: int = 400


class UnsupportedPlsLanguageException(BasePollyException):
    msg = 'The language specified in the lexicon is unsupported.'
    http_code: int = 400


class SignatureDoesNotMatchException(BasePollyException):
    msg = 'The request signature we calculated does not match the signature you provided.'


class ValidationErrorExceptions(BasePollyException):
    msg = 'validation error detected'


class MissingAuthTokenException(BasePollyException):
    msg = 'Missing Authentication Token'


class InvalidPLSLexiconException(BasePollyException):
    msg = 'Invalid PLS Lexicon'
    http_code = 400


class UnsupportedPLSLanguageException(BasePollyException):
    msg = 'Unsupported PLS language'


class ResponseValueException(BasePollyException):
    msg = 'API send response with unexpected values'


EXCEPTIONS = set()
for k, v in dict(globals()).items():
    try:
        if issubclass(v, BasePollyException):
            EXCEPTIONS.add(v)
    except TypeError:
        pass
