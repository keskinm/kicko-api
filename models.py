import datetime

import jwt


def encode_auth_token(user_id, secret_key):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token, secret_key):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'
