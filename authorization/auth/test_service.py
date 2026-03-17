from datetime import timedelta

import pytest
from jwt import exceptions as jwtExceptions

from auth.service import create_access_token, decode_token


@pytest.fixture
def user_data() -> dict:
    return {"name": "Zaka"}


def test_create_access_token_successful(user_data):
    access_token = create_access_token(user_data=user_data)
    assert access_token is not None
    assert len(access_token) <= 255


def test_decode_access_token_successful(user_data):

    access_token = create_access_token(user_data=user_data)

    decoded_token = decode_token(access_token)

    assert decoded_token is not None
    assert decoded_token["user"] == user_data


def test_invalid_token_raises_invalid_exception():

    access_token = "fjsalfjdshfñosaf"  # Jiberrish token

    with pytest.raises(jwtExceptions.InvalidTokenError):
        decode_token(access_token)


def test_expired_token_raises_expired_signature_error(user_data):

    access_token = create_access_token(
        user_data=user_data, expiry=timedelta(seconds=-10)
    )

    with pytest.raises(jwtExceptions.ExpiredSignatureError):
        decode_token(access_token)
