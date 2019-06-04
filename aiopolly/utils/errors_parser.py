text = '''
InvalidS3BucketException
The provided Amazon S3 bucket name is invalid.

HTTP Status Code: 400

InvalidS3KeyException
The provided Amazon S3 key prefix is invalid. Please provide a valid S3 object key name.

HTTP Status Code: 400

InvalidSampleRateException
The specified sample rate is not valid.

HTTP Status Code: 400

InvalidSnsTopicArnException
The provided SNS topic ARN is invalid. Please provide a valid SNS topic ARN and try again.

HTTP Status Code: 400

InvalidSsmlException
The SSML you provided is invalid.

HTTP Status Code: 400

LanguageNotSupportedException
The language specified is not currently supported by Amazon Polly in this capacity.

HTTP Status Code: 400

LexiconNotFoundException
Amazon Polly can't find the specified lexicon.

HTTP Status Code: 404

MarksNotSupportedForFormatException
Speech marks are not supported for the OutputFormat selected.

HTTP Status Code: 400

ServiceFailureException
An unknown condition has caused a service failure.

HTTP Status Code: 500

SsmlMarksNotSupportedForTextTypeException
SSML speech marks are not supported for plain text-type input.

HTTP Status Code: 400

TextLengthExceededException
The value of the "Text" parameter is longer than the accepted limits. 

HTTP Status Code: 400\
'''
t = text.replace('\'', '\\\'').split('\n\n')
for n, s in enumerate(t):
    try:
        exception, message = s.strip().split('\n')
        print(f"class {exception}(BasePollyException):\n    msg: str = '{message}'")
    except ValueError:
        print('    http_code: int = ' + s[-3:])
        print('\n')
