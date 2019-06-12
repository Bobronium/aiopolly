from botocore.credentials import Credentials
from botocore.session import Session


def get_credentials(access_key: str = None, secret_key: str = None, ):
    if access_key and secret_key:
        return Credentials(access_key, secret_key)

    return Session().get_credentials()
