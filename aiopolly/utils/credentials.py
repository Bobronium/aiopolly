from botocore.credentials import Credentials
from botocore.session import Session as BotoSession


def get_credentials(credentials=None, access_key=None, secret_key=None):
    if credentials:
        if not isinstance(credentials, Credentials):
            raise ValueError(f'Credentials must be botocore.credentials.Credentials type, not {type(credentials)}')
        return credentials

    elif access_key and secret_key:
        return Credentials(access_key, secret_key)

    else:
        return BotoSession().get_credentials()
